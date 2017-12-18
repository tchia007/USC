import json
import sys
import os
import mysql.connector

cnx = mysql.connector.connect(user='inf551', password='inf551', host='127.0.0.1', database='inf551')
cursor = cnx.cursor()

year = sys.argv[1] 

dem = "Select name, affiliation From Candidates Where year = %s and affiliation = %s"
rep = "Select name, affiliation From Candidates Where year = %s and affiliation = %s"
data_dem = (year, "democrat")
data_rep = (year, "republican")
cursor.execute(dem, data_dem)
for value in cursor:
    name, affiliation = value
    print affiliation + ": " + name 
cursor.execute(rep, data_rep)
for value in cursor:
    name, affiliation  = value
    print affiliation + ": " + name
