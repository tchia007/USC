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
	tempVector.append( (x[0] , x[1],  x[2]) )
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
for i in range(1, a+1):
	tempSum = 0
	for tuples in tempVector:
		if(i == tuples[0]):
			tempSum += (tuples[2] ** 2)
	documentLenTemp[i] = tempSum

#calculating tf*idf/sum
tfidf = [] #doc, word, tf * idf
for tuples in tempVector:
	numerator = tuples[2] * idf[tuples[1]]
	tfidf.append( (tuples[0], tuples[1], numerator / documentLenTemp[tuples[0]]))

print "-------------------------------finished calculating tfidf/ sum-------"

#storing values into 2d vector
for t in tfidf:
	vector[t[0]-1][t[1]-1] = t[2]

print "------------------------------filled vector --------------"
#calculating cosine numerator then dividing it by denominator immediately
#then creating and populating heap h. 
#value in heap is ( similarity, (doca, docb) )
h = []
for i in range(0, a):
	for j in range(i+1, a): 
		heapVal = scipy.spatial.distance.cosine(vector[i], vector[j])
		if heapVal < 1:
			heapq.heappush( h, (heapVal, (i, j)))

print "Len of heap: " + str(len(h))

for i in range(44):
	print h[i]
clustersDic = {}

def cleanClustersDic(docTuple):
	keysToBeDeleted = set()
	for key in clustersDic:
		for item in docTuple:
			if item in key:
				keysToBeDeleted.add(key)
	for values in keysToBeDeleted:
		del clustersDic[values]


def calculateCentroid(docTuple, val):
	#cleanClustersDic(docTuple)
	mySum = 0
	arr = []
	numDocs = len(docTuple) -1
	for i in range(0, b):
		tempSum = 0
		for j in range(0, numDocs):
			tempSum += vector[docTuple[j]][i]
		arr.append( tempSum / numDocs )
	clustersDic[docTuple] = arr

def calculateCosine(newCentroid):
	do = True
	for i in range(0, a):
		do = True
		for docs in newCentroid:
			if docs == i:
				do = False
				break
		if do == True:
			heapVal = scipy.spatial.distance.cosine(vector[i], clustersDic[newCentroid])
			heapq.heappush(h, (1-heapVal, (i,) + newCentroid))

def checkPoppedItem(item):
	if not clustersDic:
		return False
	for key in clustersDic:
		for val in key:
			for doc in item[1]:
				if doc == val:
					return False
	return True
#popping and creating clusers 

while tempDocNums > k:
	poppedItem = "" 
	continuePop = True
	while continuePop == True:
		poppedItem = heapq.heappop(h)
		continuePop = checkPoppedItem(poppedItem)
	calculateCentroid(poppedItem[1], poppedItem[0])
	calculateCosine(poppedItem[1])
	tempDocNums = tempDocNums - 1 

for keys in clustersDic:
	print keys








	
