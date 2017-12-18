import json
import sys
import os
import mysql.connector

cnx = mysql.connector.connect(user='inf551', password='inf551', host='127.0.0.1', database='inf551')
cursor = cnx.cursor()
year = 0
e_counter = 1
p_counter = 1
candidate_counter = 1
fileList = os.listdir(sys.argv[1])
cwd = os.getcwd()
dp_vote = 0
rp_vote = 0

for f in fileList:
	jsonFile = open(sys.argv[1] + "/" + f)
        year = f[0:4]
	raw_data = json.load(jsonFile)
	for affiliation in raw_data["candidates"]:
	    add_candidates = """Insert into Candidates (CID, name, year, affiliation) values (%s, %s, %s, %s)""" 
            data_candidates = (candidate_counter, raw_data["candidates"][affiliation], year, affiliation)
	    cursor.execute(add_candidates, data_candidates)
            candidate_counter += 1
            cnx.commit()
        for states in raw_data["votes"]:
            for type in raw_data["votes"][states]:
                if type == "electoral":
                    de_vote = raw_data["votes"][states]["electoral"]["democrat"]
                    re_vote = raw_data["votes"][states]["electoral"]["republican"]
                    add_d_votes = """Insert into Electoral (EID, statename, year, affiliation, votes) values (%s, %s, %s, %s, %s)"""
                    add_r_votes = """Insert into Electoral (EID, statename, year, affiliation, votes) values (%s, %s, %s, %s, %s)"""
                    data_d_votes = (e_counter, states, year, "democrat", de_vote)
                    e_counter += 1
                    data_r_votes = (e_counter, states, year, "republican", re_vote)
                    cursor.execute(add_d_votes, data_d_votes)
                    cursor.execute(add_r_votes, data_r_votes)
                    e_counter += 1
                elif type == "popular":
                    dp_vote = raw_data["votes"][states]["popular"]["democrat"]
                    rp_vote = raw_data["votes"][states]["popular"]["republican"] 
                    add_d_votes = """Insert into Popular (PID, statename, year, affiliation, votes) values (%s, %s, %s, %s, %s)"""
                    add_r_votes = """Insert into Popular (PID, statename, year, affiliation, votes) values (%s, %s, %s, %s, %s)"""
                    data_d_votes = (p_counter, states, year, "democrat", dp_vote)
                    p_counter += 1
                    data_r_votes = (p_counter, states, year, "republican", rp_vote)
                    cursor.execute(add_d_votes, data_d_votes)
                    cursor.execute(add_r_votes, data_r_votes)
                    p_counter += 1 
                cnx.commit()
cursor.close()
cnx.close()
