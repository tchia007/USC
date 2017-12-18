from pyspark import SparkContext
from operator import add 
import sys

sc = SparkContext(appName="inf553")

inputA = sys.argv[1]
inputB = sys.argv[2]
output = sys.argv[3]

matA = sc.textFile(inputA)
matB = sc.textFile(inputB)

map1A = matA.map(lambda line : line.split(","))\
		    .map(lambda row, column, value : (column, ('A', row, value) ))

map1B = matB.map(lambda line: line.split(",")) \
			.map(lambda row, column, value : (row, ('B', column, value)))

reducer1 = map1A.union(map1B). \
				.groupByKey(). \
				.map(lambda x: (x[0], list(x[1])))

