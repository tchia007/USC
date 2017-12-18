import sys
from pyspark import SparkContext
from itertools import combinations
import operator

inputTxt = sys.argv[1]
outputTxt = sys.argv[2]
sc = SparkContext(appName="inf553")

def sigMatrixFunc(line):
	hashVal = 0
	counter = 0
	hashMatrix1 = []
	tempArr = []
	for value in line:
		if isinstance(value, list):
			for i in range(0,20):
				hashVal = 100
				for x in value:
					hashFunc = (3*x + 13*i) % 100
					if hashFunc < hashVal:
						hashVal = hashFunc
				tempArr.append(hashVal)
		else:
			#hashMatrix1.append(value) #this is the user
			tempArr.append(value)
	hashMatrix1.append(tempArr)
	return hashMatrix1


def banding(line):
	band = "band"
	bandCounter = 1
	tempArr = []
	counter = 0
	return_arr = []
	user = ""
	tempBand = ""
	temp_Dictionary = {}
	curBand = ""
	for values in line: 
		for hashedVals in values:
			if counter == 0: #obtaining the user 
				user = hashedVals
			if counter == 1: #need to append user and first hash
				curBand = band + str(bandCounter)
				tempBand = str(hashedVals) + ","
				bandCounter += 1
			elif counter <= 4 and counter != 0: 
				tempBand = tempBand + str(hashedVals) + ","
			counter += 1
			if counter > 4:
				#reached 4 item limit, need to create key value pair now 
				#key value will be ((band, hash), user) with tuples
				tup = (curBand, tempBand)
				tup2 = (tup, user)
				return_arr.append(tup2)
				counter = 1 #reset counter
	return return_arr

def genPairs(line):
	comb = []
	returnArr = []
	for values in line: 
		if(isinstance(values, list)): #grabbing the arrays of users
			if len(values) >= 3:
				comb = list(combinations(values, 2))
				for tuples in comb: #adding combinations to returnArray
					returnArr.append(tuples)
					reverse = tuples[::-1]
					returnArr.append(reverse)
			elif len(values) == 2:
				returnArr.append(tuple(values)) #append to return array
				reverse2 = values[::-1]
				returnArr.append(tuple(reverse2))
	return returnArr

def filterTop5(arr, compareVal):
	finalArr = []
	tempArr = []
	for value in arr:
		if isinstance(value, tuple):
			if value[1] == compareVal:
				tempArr.append(value)
			else:
				finalArr.append(value)
                else:
                    finalArr.append(value)
	sortTemp = sorted(tempArr, key = lambda x: x[0])
	for values in sortTemp:
		finalArr.append(values)
		if len(finalArr) > 5:
			return finalArr


def jaccard(line):
	intersectCount = 0
	unionCount = 0
	firstUserData = ""
	firstUser =""
	tempArr = []
	tempDict = {}
	for value in line: #calculating jaccard in similarity 
		if isinstance(value, list):
			for users in value:
				curUser = dataMatrix[users]
				for values in firstUserData:
					if values in curUser:
						intersectCount += 1
				mySet = set(firstUserData + curUser)
				unionCount = len(mySet)
				jacSim = float(intersectCount) / unionCount
				tempArr.append((users, jacSim))
				intersectCount = 0
		else:
			firstUserData = dataMatrix[value]
			firstUser = value
			tempArr.append(value)
	#filtering the results to only have top 5 
	if len(tempArr) > 6:
		previousVal = 100
		jacCounter = 0
		simJac = []
		prevJac = 0
		counter = 0
		top5counter = 0
		top5arr = []
		prevTup = ""
		finalRet = []
		finalRet.append(tempArr[0])
		top5arr.append(tempArr[0]) #adding the user to new array 
		candidates = tempArr[1:]
		#sortedCandidates is sorted based on jaccard similarity desc. 
		sortedCandidates = sorted(candidates, key = lambda x: x[1], reverse=True)
		for values in sortedCandidates:
			if isinstance(values, tuple):
				if counter < 5:
					top5arr.append(values)
					if values[1] != previousVal:
						previousVal = values[1]
				elif counter >= 5 and previousVal == values[1]:
					#if fifth element has same jaccard as 6th element, keep checking
					top5arr.append(values)
				elif counter >= 5 and previousVal != values[1]:
					#top5sorted = sorted(top5arr, key= lambda x: x[0])
					return filterTop5(top5arr, previousVal)
				counter += 1
	else:
	#	sortedTempArr = sorted(tempArr, key = lambda x: x[0]j)
		return tempArr

def sortJac(line):
	tempArr = []
	returnArr = []
	user = ""
	for values in line:
		if isinstance(values, tuple):
			tempArr.append(values)
		else:
			returnArr.append(values)
	returnArr.append(sorted(tempArr))
	return returnArr

#getting input file to put into RDD
inputData = sc.textFile(inputTxt) \
			   .map(lambda line: line.split(',')) \
			   .map(lambda line: (int(line[0][1:]), [int(line[x]) for x in range(1, len(line))])) \

#collecting the input file and storing into dictionary
dataMatrix = {}
user = ""
for values in inputData.collect(): 
	for elements in values:
		if isinstance(elements, list):
			dataMatrix[user] = elements
		else:
			user = elements

sigMatrix = inputData.map(sigMatrixFunc)

bands = sigMatrix.flatMap(banding).groupByKey() \
				 .map(lambda x: (x[0], list(x[1])))


#testing
pairs = bands.flatMap(genPairs) \
			 .filter(lambda x: len(x) > 1) \
			 .map(lambda x: tuple(map(int,x))) \
			 .groupByKey() \
			 .flatMap(lambda x:[ (x[0], v) for v in set(x[1])]) \
			 .groupByKey() \
			 .map(lambda x: (x[0], list(x[1])))


calcJac = pairs.map(jaccard) \
			   .filter(lambda x: x != None) \
			   .sortByKey() \
                           .map(sortJac) \
			   .collect()

# writing the results to output file
document = open(outputTxt, 'w')
for values in calcJac:
	temp = ""
	for elements in values:
		if isinstance(elements, list): #suggested users
			for tup in elements:
				temp = temp + 'U' + str(tup[0]) + ','
		else:
			temp = 'U'+str(elements) + ':'
	document.write(temp[:-1] + "\n")
document.close()
