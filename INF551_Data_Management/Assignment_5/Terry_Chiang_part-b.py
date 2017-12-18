import sys
from pyspark import SparkContext
from operator import add

sc = SparkContext(appName="inf551")

person = sc.textFile('person.txt') \
			.map(lambda line: line.split(',')) \
			.map(lambda (name, phone, city):
				(name, {'phone': phone, 'city': city}))

purchase = sc.textFile('purchase.txt') \
			 .map(lambda line: line.split(',')) \
			 .map(lambda (buyer, seller, store , product):
			 	(buyer, {'seller' : seller, 'store' : store, 'product' : product} ))

person = person.filter(lambda (name, dictionary) : dictionary['city'] == 'los angeles')

purchase = purchase.filter(lambda (buyer, dictionary) : dictionary['seller'] == 'john')


person_list = person.join(purchase) \
					.map(lambda (name, _): name) \
					.distinct() \
					.collect()

for person in person_list:
	print person