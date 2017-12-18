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

docwords = open(docwordsFile, 'r')
head = list(islice(docwords, 3))
a = int(head[0])
tempDocNums = a
b = int(head[1])
c = int(head[2])

#document vector with row = document#, column = document id 
vector = np.zeros( (a, b))
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


#calculating tf*idf
tfidf = [] #doc, word, tf * idf
for tuples in tempVector:
	numerator = tuples[2] * idf[tuples[1] +1]
	tfidf.append( (tuples[0], tuples[1], numerator))

#calculating document sum 
newtfidf = []
tempSum = 0
documentLenTemp = {} # document : sum 
for i in range(0, a):
	tempSum = 0
	for tuples in tfidf:
		if(i == tuples[0]):
			tempSum += tuples[2] ** 2
	# documentLenTemp[i] = tempSum ** (.5)
	documentLenTemp[i] = np.sqrt(tempSum)

for i in documentLenTemp:
	print i, documentLenTemp[i]

for tuples in tfidf:
	newtfidf.append( (tuples[0], tuples[1], (tuples[2] / documentLenTemp[tuples[0]] )))

#storing values into 2d vector
for t in newtfidf:
	vector[t[0]][t[1]] = t[2]

for i in vector:
	print i
	
#calculating cosine numerator then dividing it by denominator immediately
#then creating and populating heap h. 
#value in heap is ( similarity, (doca, docb) )
h = []
for i in range(0, a):
	for j in range(i+1, a): 
		if i != j:
			heapVal = scipy.spatial.distance.cosine(vector[i], vector[j])
			# if heapVal < 1:
			if heapVal != 1:
				heapq.heappush( h, (heapVal, (i, j) ) )

clustersDic = {}
checked = []
clusters = list(range(0,a))

def mergeClusters(centroid): #merges clusters and adds to checked list
	# print "Merging clusters", centroid
	counter = 0
	mergedCentroid = tuple()
	toBeRemoved = []
	for item in centroid:
		for cluster in clusters:
			if item == cluster:
				toBeRemoved.append(item)

	for items in toBeRemoved:
		clusters.remove(items)

	if isinstance(centroid[0], int):
		# clusters.remove(centroid[0])
		if isinstance(centroid[1], int): # (int, int)
			mergedCentroid = centroid
			checked.append(centroid[0])
			checked.append(centroid[1])
		else: #(int, tuple)
			checked.append(centroid[0])
			checked.append(tuple(sorted(centroid[1])))
			mergedCentroid += (centroid[0],) + centroid[1]
	if isinstance(centroid[0], tuple): # (tuple, tuple)
		if isinstance(centroid[1], tuple):
			checked.append(centroid[0])
			checked.append(centroid[1])
			mergedCentroid += centroid[0] + centroid[1]
	clusters.append(tuple(sorted(mergedCentroid)))
	return tuple(sorted(mergedCentroid))

def calculateCentroid(mergedCentroid): #merging step
	# print "In calculating centroid ", mergedCentroid 
	updatedCentroid = mergeClusters(mergedCentroid)
	arr = []
	numDocs = len(updatedCentroid)
	tempSum = np.zeros( b, dtype=np.float)
	for j in range(0, numDocs):
		#print "LSKDFJLKSDFJLKSDJFLKDSJF ", vector[ updatedCentroid[j]]
		tempSum += vector[ updatedCentroid[j] ]
	arr.append( tempSum / numDocs )
	# print "clustersdic at ", updatedCentroid, "get: ",  arr
	clustersDic[updatedCentroid] = arr
	return updatedCentroid

def calculateCosine(newCentroid):
	# print "Calc cosine: ", newCentroid
	for i in range(0, a):
		do = True
		for docs in newCentroid:
			if docs == i:
				do = False
				break
		if do == True:
			heapVal = scipy.spatial.distance.cosine(vector[i], clustersDic[newCentroid])
			if heapVal != 1:
				# print "Val and newcentroid ", i, newCentroid, heapVal
				heapq.heappush(h, (heapVal, (i, newCentroid)))

	for val in clusters:
		if val in clustersDic and val != newCentroid:
			heapVal2 = scipy.spatial.distance.cosine( clustersDic[val], clustersDic[newCentroid])
			if heapVal2 != 1:
				# print "Val and newcentroid ", val, newCentroid, heapVal2
				heapq.heappush(h, (heapVal2, (val, newCentroid)))

def checkPoppedItem(item):
	if not checked:
		return False
	similarCounter = 0
	if isinstance(item[1][1], tuple):
		for t in checked:
			if isinstance(t, tuple):
				similarCounter = 0
				for doc1 in t:
					for doc2 in item[1][1]:
						if doc1 == doc2:
							similarCounter += 1
		if similarCounter == len(item[1][1]):
			return True
	if item[1][0] in checked:
		return True
	if item[1][1] in checked: 
		return True
	return False

#popping and creating clusers 
poppedItem = ""
while len(clusters)> k:
	continuePop = True
	while continuePop == True:
		poppedItem = heapq.heappop(h)
		continuePop = checkPoppedItem(poppedItem)
	# newCentroid = mergeCentroid(poppedItem[1])
	newCentroid = calculateCentroid(poppedItem[1])
	calculateCosine(newCentroid)
	tempDocNums = tempDocNums - 1 		

#printing out values with + 1 to adjust 
tempString = ""
for values in clusters:
	if isinstance(values, int):
		print values + 1
	else:
		tempString = ""
		for docs in values:
			tempString += str(docs+1) + ", "
		print tempString[:-2]


