import sys
from pyspark import SparkContext
from operator import add

sc = SparkContext(appName="inf551")

company = sc.textFile('company.txt') \
			.map(lambda line: line.split(',')) \
			.map(lambda (cname, stock_price, country):
				(cname, {'stockprice' : stock_price, 'country': country}))


person = sc.textFile('person.txt') \
			.map(lambda line: line.split(',')) \
			.map(lambda (name, phone, city):
				(name, {'phone': phone, 'city': city}))

person_list = person.filter(lambda (name, dictionary) : dictionary['city'] == 'los angeles') \
					.sortByKey() \
					.map(lambda (name, _): name) \
					.collect()

for person in person_list:
	print person


product = sc.textFile('product.txt')
purchase = sc.textFile('purchase.txt')

