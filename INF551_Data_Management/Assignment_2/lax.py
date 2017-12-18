import json 
import sys

year = []
terminal = []
no_terminal_input = ["Terminal 1", "Terminal 2", "Terminal 3", "Terminal 4", "Terminal 5", "Terminal 6", "Tom Bradley International Terminal"]
traffic = []
result = []

sum = 0

terminal_first = False
year_first = False
traffic_first = False

def calculate_sum(result):
	new_sum = 0
	for r in result:
		new_sum += int(r[13])
	global sum 
	sum = new_sum

def format_terminal(terminal):
	new_terminal = []
	term = "Terminal "
	for value in terminal: 
		if value.lower() == "tbi":
			new_terminal.append("Tom Bradley International Terminal")
		else:
			temp = str(value[-1:])
			new_terminal.append(term + temp)
	return new_terminal


cmd_line_input = sys.argv[2].split()
for word in cmd_line_input:
	if len(word) == 4:
		year.append(word)
	elif word.lower() == "arrival":
		traffic.append("Arrival")
	elif word.lower() == "departure":
		traffic.append("Departure")
	elif word[0] == "T" or word[0] == 't':
		terminal.append(word)

terminal = format_terminal(terminal)

with open('lax.json') as json_data:
	data = json.load(json_data)
	refined_data = data["data"]
	if cmd_line_input:
		for value in refined_data:
			if terminal:
				for t in terminal:
					if str(value[10]) == t: #matching terminal 
						if year:
							for y in year:
								if str(value[9]).startswith(str(y)): #matching terminal and year
									if traffic: #matching terminal, year, and traffic
										for traf in traffic:
											if str(value[11]).lower() == str(traf).lower(): #matching terminal, year, and traffic
												result.append(value)
									else:
										result.append(value)
						elif traffic:						
							for traff in traffic: 
								if str(value[11]).lower() == str(traff).lower():
									result.append(value)
						else:
							result.append(value)
			else: #no terminal input. 
				for n in no_terminal_input:
					if str(value[10]) == n: #matching terminal 
						if year:
							for y in year:
								if str(value[9]).startswith(str(y)): #matching terminal and year
									if traffic: #matching terminal, year, and traffic
										for traf in traffic:
											if str(value[11]).lower() == str(traf).lower(): #matching terminal, year, and traffic
												result.append(value)
									else:
										result.append(value)
						elif traffic:							
							for traff in traffic: 
								if str(value[11]).lower() == str(traff).lower():
									result.append(value)
						else:
							result.append(value)			
	else:
		for value in refined_data:
			if no_terminal_input:
				for t in no_terminal_input:
					if str(value[10]) == t:
						result.append(value)
	calculate_sum(result)

	print sum









