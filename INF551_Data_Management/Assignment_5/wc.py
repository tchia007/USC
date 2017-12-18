import sys
from pyspark import SparkContext
from operator import add

sc = SparkContext(appName="inf551")

lines = sc.textFile('company.txt')

counts = lines.flatMap(lambda x: x.split(' ')) \
            .map(lambda x: (x, 1)) \
            .reduceByKey(add)

output = counts.collect()

for v in output:
    print '%s, %s' % (v[0], v[1])

