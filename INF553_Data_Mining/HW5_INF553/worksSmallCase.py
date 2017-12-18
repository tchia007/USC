import sys
import heapq
from itertools import islice
import numpy as np
import scipy
from scipy import spatial


docwordsFile = sys.argv[1]
k = int(sys.argv[2]) #num of desired clusters

counter = 0
a = 0 # num of documents
b = 0 # num of words 
c = 0 # num words that appear in at least one document 

df = {} #dictionary of document frequenies. word : count
idf = {} #idf value for each word. word: idf

# document id, word id, tf, 1 118 1 

docwords = open(docwordsFile, 'r')
head = list(islice(docwords, 3))
a = int(head[0])
tempDocNums = a
b = int(head[1])
c = int(head[2])


#document vector with row = document#, column = document id 
vector = np.zeros( (a, b), dtype=np.float)
tempVector = [] # contains (doc, word, tf) 

#appending each line into tempVector as a tuple
for line in docwords:
	x = map(int, line.split())
	tempVector.append( (x[0] -1 , x[1]-1,  x[2]) )
	#creating df and idf dictionaries
	if x[1] in df:
		df[ x[1] ] = df[ x[1] ] + 1
		idf[x[1]] = 0
	else:
		df[ x[1] ] = 1
		idf[x[1] ] = 0
docwords.close()

#filling idf dictionary with values. 
for key in idf:
	idfVal =  np.log2( (float(a) + 1) / (df[key] + 1 ) ) 
	idf[key] = idfVal

#calculating document sum 
tempSum = 0
documentLenTemp = {} # document : sum 
for i in range(0, a):
	tempSum = 0
	for tuples in tempVector:
		if(i == tuples[0]):
			tempSum += (tuples[2] ** 2)
	documentLenTemp[i] = tempSum

#calculating tf*idf/sum
tfidf = [] #doc, word, tf * idf
for tuples in tempVector:
	numerator = tuples[2] * idf[tuples[1] +1]
	tfidf.append( (tuples[0], tuples[1], numerator / documentLenTemp[tuples[0]]))

print "-------------------------------finished calculating tfidf/ sum-------"

#storing values into 2d vector
for t in tfidf:
	vector[t[0]][t[1]] = t[2]

print "------------------------------filled vector --------------"
#calculating cosine numerator then dividing it by denominator immediately
#then creating and populating heap h. 
#value in heap is ( similarity, (doca, docb) )
h = []
for i in range(0, a):
	for j in range(i+1, a): 
		if i != j:
			heapVal = 1-(1-scipy.spatial.distance.cosine(vector[i], vector[j]))
			# if heapVal < 1:
			if heapVal != 1:
				heapq.heappush( h, (heapVal, (i, j) ) )

print "Len of heap: " + str(len(h))

clustersDic = {}
checked = []
clusters = list(range(0,a))

def cleanClustersDic(docTuple):
	print "cleaning : ", docTuple
	keysToBeDeleted = set()
	for key in clustersDic:
		for item in docTuple:
			if item in key:
				keysToBeDeleted.add(key)
	for values in keysToBeDeleted:
		print "deleting----------------", values
		del clustersDic[values]


def mergeCentroid(centroid):
	print "Merging and deleting", centroid
	print "Clusters array---------------- ", clusters

	for item in centroid:
		for values in clusters:
			if item == values:
				clusters.remove(values)

	if isinstance(centroid[1], tuple):
		newCentroid = (centroid[0],) + centroid[1]
		print "Merged centroid : ", newCentroid
		clusters.append(newCentroid)
		print "Updated clusters :", clusters
		return newCentroid
	else:
		print "Merged centroid : ", centroid
		clusters.append(centroid)
		print "Updated clusters :", clusters
		return centroid

def cleanClusters(tuple1, tuple2):
	print "Merging and deleting", tuple1, tuple2
	print "Clusters array---------------- ", clusters
	tobeRemoved = []
	for values in clusters:
		print "Checking these two: ", tuple1, tuple2, "with", values
		if tuple1 == values:
			print "Removing : ", values
			tobeRemoved.append(values)
		if tuple2 == values:
			print "Removing : ", values
			tobeRemoved.append(values)
	for item in tobeRemoved:
		clusters.remove(item)
	clusters.append(tuple1 + tuple2)
	print "Updated clusters :", clusters

def calculateCentroid(mergedCentroid): #merging step
	print "In calculating centroid ", mergedCentroid 
	if isinstance(mergedCentroid[0], tuple):
		checked.append(mergedCentroid[0] + mergedCentroid[1])
		updatedCentroid = mergedCentroid[0] + mergedCentroid[1]
		cleanClusters(mergedCentroid[0], mergedCentroid[1])
	else:
		checked.append(mergedCentroid[0])
		checked.append(mergedCentroid[1])
		updatedCentroid = mergeCentroid(mergedCentroid)
	print "Updated centroid : ", updatedCentroid
	mySum = 0
	arr = []
	numDocs = len(updatedCentroid) 
	for i in range(0, b):
		tempSum = 0
		for j in range(0, numDocs):
			tempSum += vector[ updatedCentroid[j] ][i]
		arr.append( tempSum / numDocs )
	# print "clustersdic at ", updatedCentroid, "get: ",  arr
	clustersDic[updatedCentroid] = arr
	return updatedCentroid


def calculateCosine(newCentroid):
	print "Calc cosine: ", newCentroid

	for i in range(0, a):
		do = True
		for docs in newCentroid:
			if docs == i:
				do = False
				break
		if do == True:
			heapVal = 1-(1-scipy.spatial.distance.cosine(vector[i], clustersDic[newCentroid]))
			if heapVal != 1:
				heapq.heappush(h, (heapVal, (i, newCentroid)))


	for val in clusters:
		if val in clustersDic and val != newCentroid:
			heapVal2 = 1-(1-scipy.spatial.distance.cosine(clustersDic[val], clustersDic[newCentroid]))
			if heapVal2 != 1:
				heapq.heappush(h, (heapVal2, (val, newCentroid)))

def checkPoppedItem(item):
	print "\n"

	if not checked:
		return False
	print "Checking: ", checked, "with ", item
	if item[1][0] in checked:
		print "Key matches with something in item[1]---"
		return True
	if item[1][1] in checked: 
		print "Key matches with something in item[1]---"
		return True
	print "Key doesn't match with something in item[1]---"
	return False


#popping and creating clusers 
poppedItem = ""
while tempDocNums > k:
	continuePop = True
	while continuePop == True:
		poppedItem = heapq.heappop(h)
		continuePop = checkPoppedItem(poppedItem)
	# newCentroid = mergeCentroid(poppedItem[1])
	newCentroid = calculateCentroid(poppedItem[1])
	calculateCosine(newCentroid)
	tempDocNums = tempDocNums - 1 

print "Clusters"
# finalOutput = ""
# for values in clusters:
# 	finalOutput = ""
# 	for items in values:
# 		finalOutput += str(items+1) + ", "
# 	print finalOutput[:-2]
	

for values in clusters:
	print values




