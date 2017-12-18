from pyspark import SparkContext
from operator import add 
from itertools import chain, combinations
import sys

sc = SparkContext(appName="inf553")

basketsTxt = sys.argv[1]
support = float(sys.argv[2])
outputTxt = sys.argv[3]

def myApriori(baskets): 
    counts = {}
    basketCount = 0
    itemArr= set() #frequent items set 
    rows = []
    for line in baskets:
        basketCount += 1
        rows.append(line)
        for elements in line:
            if elements in counts: #creating counts table for 1-item
                counts[elements] = counts[elements] + 1
            else:
                itemArr.add(elements)
                counts[elements] = 1

    for element, count in counts.items(): #removing single item supports 
        if(count / float(basketCount)) < support:
            del counts[element]
            itemArr.remove(element)

    # this part does the combinations of the items in itemArr and stores it into combStorage
    combinationArr = chain(*[combinations(itemArr, i+2) for i, a in enumerate(itemArr)])
    combStorage = set()
    for values in combinationArr:
        combStorage.add(values)

    #creating counts for all the items 
    for values in rows:
        for tuples in combStorage:
            combinationOk = True
            for elements in tuples:
                if elements not in values:  
                    combinationOk = False
            if combinationOk:
                if tuples in counts:
                    counts[tuples] = counts[tuples] + 1 
                else:
                    itemArr.add(tuples)
                    counts[tuples] = 1

    for element, count in counts.items(): #eliminating supports 
        if (count / float(basketCount)) < support:
            del counts[element]
            itemArr.remove(element)

    for element in counts: #removing counts to create candidates 
        counts[element] = 1
        #print str(element) + " : " + str(counts[element])
    return counts


#map partitions to invoke myApriori function
rdd_phase1 = sc.textFile(basketsTxt, 2) \
        .map(lambda line: line.split(',')) \
        .map(lambda line: [int(x) for x in line]) \
        .mapPartitions(myApriori).distinct() \

allBasketsLen = sc.textFile(basketsTxt) \
            .map(lambda line:line.split(',')) \
            .map(lambda line:[int(x) for x in line]) \
            .count()

allBaskets = sc.textFile(basketsTxt) \
               .map(lambda line: line.split(',')) \
               .map(lambda line: [int(x) for x in line]) \
               .collect()

def phase2(basketsPhase1):#function to find global frequents
    counts = {}
    for values in basketsPhase1: #phase1 basket items
        for tuples in allBaskets: #all baskets 
            combinationOk = True
            if isinstance(values,tuple):
                for element in values:
                    if element not in tuples:
                        combinationOk = False
                if combinationOk:
                    if values not in counts:
                        counts[values] = 1
                    else:
                        counts[values] = counts[values] + 1
            else:
                if values in tuples:
                    if values not in counts:
                        counts[values] = 1 
                    else:   
                        counts[values] = counts[values] +1
    #return counts
    for element, count in counts.items():
        if(count / float(allBasketsLen)) < support:
            del counts[element]
    return counts

rdd_phase2 = rdd_phase1.mapPartitions(phase2).collect() #phase2 results

outputFile = open(outputTxt, 'w') #opening file to write the values of RDD
for values in rdd_phase2:
    temp = ""
    if isinstance(values, tuple):
        for keys in values:
            temp = temp + str(keys) + ", "
        outputFile.write(temp[:-2] + "\n")
    else:
        outputFile.write(str(values) + "\n")

        
outputFile.close()
