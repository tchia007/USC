import sys
from pyspark import SparkContext
from operator import add

sc = SparkContext(appName="inf551")

product = sc.textFile('product.txt') \
			.map(lambda line: line.split(',')) \
			.map(lambda (name, price, category, maker):
				(name, category))

purchase = sc.textFile('purchase.txt') \
			 .map(lambda line: line.split(',')) \
			 .map(lambda (buyer, seller, store, product):
			 	(product, seller))

sellers_product = product.join(purchase) \
				 .map(lambda (list) : list[1])

laptops = sellers_product.filter(lambda (list) : list[0] == 'laptop') \
						 .map( lambda (list) : list[1]) \
						 .distinct()

cellphones = sellers_product.filter(lambda (list) : list[0] == 'cell phone') \
							.map(lambda (list) : list[1]) \
							.distinct()

no_cell_phones = laptops.subtract(cellphones).collect()

for item in no_cell_phones:
	print item
