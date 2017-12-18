import json
import sys
import os
import mysql.connector

cnx = mysql.connector.connect(user='inf551', password='inf551', host='127.0.0.1', database='inf551')
cursor = cnx.cursor()

year = sys.argv[1] 
candidate = sys.argv[2]
state = sys.argv[3] 
e_value = 0
p_value = 0

candidate = candidate.title()
year = year.upper()

electoral_query = """SELECT E.votes FROM Electoral E, Candidates C WHERE E.year = C.year AND E.year = %s AND C.name = %s AND E.statename = %s AND C.affiliation = E.affiliation"""

popular_query = """SELECT P.votes FROM Popular P, Candidates C WHERE P.year = C.year AND P.year = %s AND C.name = %s AND P.statename = %s and C.affiliation = P.affiliation"""
data_query = (year, candidate, state)
cursor.execute(electoral_query, data_query)
for value in cursor:
    e_value = value[0]

cursor.execute(popular_query, data_query)
for value in cursor:
    p_value = value[0]

print "EV: " + str(e_value) + "; PV: " + str(p_value)
cnx.commit()

cursor.close()
cnx.close()
