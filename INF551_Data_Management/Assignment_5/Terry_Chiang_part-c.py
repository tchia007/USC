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

product = sc.textFile('product.txt') \
			.map(lambda line: line.split(',')) \
			.map(lambda (name, price, category, maker):
				(name, {'price': price, 'category' : category, 'maker' : maker}))

purchase = sc.textFile('purchase.txt') \
			 .map(lambda line: line.split(',')) \
			 .map(lambda (buyer, seller, store , product):
			 	(buyer, {'seller' : seller, 'store' : store, 'product' : product} ))


company = company.map(lambda (cname, dictionary) : (cname, dictionary['country'] ) )
#for item in company:
#	print item
product = product.map(lambda (name, dictionary) : (dictionary['maker'], name) )
#for item in product:
#	print item
product_list = product.join(company) \
					  .map(lambda (name, list) : (list[0], list[1]) ) \
					  .sortByKey() \
					  .collect()


for product in product_list:
	print str(product[0] + ", " + product[1])
