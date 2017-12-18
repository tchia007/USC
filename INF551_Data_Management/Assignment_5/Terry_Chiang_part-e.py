import sys
from pyspark import SparkContext
from operator import add

sc = SparkContext(appName="inf551")

product = sc.textFile('product.txt') \
			.map(lambda line: line.split(',')) \
			.map(lambda (name, price, category, maker):
				 (maker, float(price)))
product = product.aggregateByKey( (0,0), lambda U, price : (U[0] + price, U[1] + 1), lambda U1, U2 : (U1[0] + U2[0], U1[1] + U2[1]))
product = product.map(lambda (x, (y, z) ) : (x, float(y)/z )).sortByKey().collect()

for item in product:
	print str(item[0] + ", ") + str(item[1])