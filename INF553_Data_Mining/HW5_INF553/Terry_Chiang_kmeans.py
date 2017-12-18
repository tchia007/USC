from __future__ import print_function
from itertools import islice
import numpy as np
import scipy
from scipy import spatial
from scipy import sparse
from pyspark.sql import SparkSession
import sys

spark = SparkSession\
    .builder\
    .appName("PythonKMeans")\
    .getOrCreate()
#from ec2
#----------------------BEGIN  OF COPY ----------------------------------
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
            tempSum += (tuples[2] ** 2)
    documentLenTemp[i] = tempSum ** (.5)

for tuples in tfidf:
    newtfidf.append( (tuples[0], tuples[1], tuples[2] / documentLenTemp[tuples[0]] ))

#storing values into 2d vector
for t in newtfidf:
    vector[t[0]][t[1]] = t[2]
#----------------------END OF COPY ------------------------

sc = spark.sparkContext
#need to convert our matrix into sparse matrix 
mySparse = sparse.csr_matrix(vector)
# data = [(i,mySparse [i,:]) for i in xrange(mySparse.shape[0])]
data =[mySparse [i,:] for i in xrange(mySparse.shape[0])]
sparseRDD = sc.parallelize(data)

convergeDist = float(sys.argv[3])
outputFile = sys.argv[4]

kPoints = sparseRDD.repartition(1).takeSample(False, k, 1)
tempDist = 1.0

def closestPoint(p, centers):
    i = 0
    bestIndex = 0
    closest = float("+inf")
    for item in centers:
        cosineVal = spatial.distance.cosine(p.toarray(), item.toarray())
        if cosineVal != 1 and cosineVal < closest:
            closest = cosineVal
            bestIndex = i
        i += 1
    return bestIndex

while tempDist > convergeDist:
    #assign point to closest cluster
    #change to calculate cosine 
    closest = sparseRDD.map(
        lambda p: (closestPoint(p, kPoints), (p, 1)))
    #count points in the cluster and sum them 
    pointStats = closest.reduceByKey(
        lambda p1_c1, p2_c2: (p1_c1[0] + p2_c2[0], p1_c1[1] + p2_c2[1]))
    #calculating new centroid
    newPoints = pointStats.map(
        lambda st: (st[0], st[1][0] / st[1][1])).collect()
    tempDist = sum(np.sum((kPoints[iK].toarray() - p.toarray()) ** 2) for (iK, p) in newPoints)
    for (iK, p) in newPoints:
        kPoints[iK] = p

output = open(outputFile, 'w')
for i in kPoints:
    counter = 0
    for j in i.toarray():
        for x in j:
            if x > 0:
                counter += 1
    output.write(str(counter)+ "\n")
sc.stop()
