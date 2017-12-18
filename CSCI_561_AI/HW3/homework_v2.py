import copy

#global variables 
num_queries = 0
queries = [] 
kb = [] #kb of sentences with variables 
kb_constants = [] #copy of kb_constants
kb_constants_og = [] #original kb constants
output = [] #output array 
seen = [] # seen sentences from resolution steps

#class sentence to hold the predicate and variables for that predicate
class Sentence:
	def __init__(self, predicate, variables, negation):
		self.predicate = predicate 
		self.variables = variables #list of variables 
		self.negation = negation

def readInput():
	with open('input.txt', 'r') as f:
		counter = 0
		for line in f:
			val = line.strip()
			try:
				int(val)
				counter += 1
			except ValueError:
				if counter == 1: #getting queries 
					sentence = createSentence(val.strip())
					queries.append(sentence)
				elif counter == 2: #getting KB 
					if "|" not in val:
						sentence = createSentence(val.strip())
						kb_constants_og.append(sentence)
					else:
						ors = [] #list to store the sentences separated by logical or 
						split = val.split('|')
						for sent in split:
							ors.append(createSentence(sent.strip()))
						kb.append(ors)
def createOutput():
	with open('output.txt', 'w') as f:
		for val in output:
			f.write(str(val).upper() + "\n")
	exit()

#helper function to negate a query in preparation for resolution
def negateQuery(negation):
	if negation == True:
		return False
	else:
		return True

#create an instance of class sentence given a raw string
def createSentence(raw_str):
	negation = bool()
	if raw_str[0] == '~': 
		raw_str = raw_str[1:]
		negation = True
	else:
		negation = False
	variable = raw_str[raw_str.find("(")+1:raw_str.find(")")].split(',')
	predicate = raw_str[0:raw_str.find("(")]
	return Sentence(predicate, variable, negation);

#function to check if contradiction occurs in the kb given an array
def checkContradiction(check):
	toAddKB = []
	print "Checking contradiction"
	for sentence in check:
		for kb_sent in kb_constants:
			if sentence.predicate == kb_sent.predicate and sentence.variables == kb_sent.variables and sentence.negation != kb_sent.negation:
				print "---------------Found contradiction"
				printSentence(kb_sent)
				printSentence(sentence)
				return True
		#add to kb_constants if a constant is found
		add_kb = True
		for variable in sentence.variables:
			if len(variable) == 1:
				add_kb = False
				break
		if add_kb:
			# toAddKB.append(sentence)
			print "Adding to kb"
			printSentence(sentence)
			kb_constants.append(sentence)
	return False

def printSentence(sentence):
	if sentence.negation == True:
		print "~" + str(sentence.predicate) + str(sentence.variables)
	else:
		print sentence.predicate, sentence.variables

def printOrsArr(arr):
	printArr = str()
	for val in arr:
		if val.negation == True:
			printArr += "~" + str(val.predicate) + "("
			for v in val.variables:
				printArr += v + ", "
			printArr = printArr[:-2] + ")"
		else:
			printArr += val.predicate + "("
			for v in val.variables:
				printArr += v + ", "
			printArr = printArr[:-2] + ")"
		printArr += " | " 
	print printArr[:-2]


def removeDuplicates(arr):
	seenSentences = set()
	returnArr = []
	for sentence in arr:
		temp_str = ""
		if sentence.negation == True:
			temp_str = "~" + str(sentence.predicate) + str(sentence.variables)
		else:
			temp_str = str(sentence.predicate) + str(sentence.variables)
		if temp_str not in seenSentences:
			returnArr.append(sentence)
		else:
			seenSentences.add(temp_str)
	return returnArr


#function to unify sentences given current resolution sentence and kb sentence
def unifySentence(res_arr, kb_arr):
	print "----------------Unifying"
	printOrsArr(res_arr)
	printOrsArr(kb_arr)
	unmatched = set() #unmatched stores remaining kb sentences after cancelation
	unmatchedRes = [] #stores remaining resolution sentences after cancelation
	unification = {}
	cancelPred = []
	completeCancel = False
	for r in res_arr:
		dup_pred = False
		counter = 0
		for k in kb_arr:
			counter += 1
			save_k = True
			if r.predicate == k.predicate and r.negation != k.negation:
				#exact same variables but predicates cancel. no need to continue
				if k.variables == r.variables:
					print "matched"
					completeCancel = True
					cancelPred.append(k.predicate)
					break
				#finding unification of variables 
				else:
					#unification already filled up based on length
					if (len(unification) == len(k.variables)):
						unmatched.add(copy.deepcopy(k))
						if counter == len(kb_arr):
							break
					#if unification isn't done 
					if len(unification) != len(k.variables):
						for i in range(0, len(k.variables)):

							#if the variable has already been mapped 
							if k.variables[i] in unification:
								unification = {}
								break
							#if the only assignment is var1 = var2 then break, no unification possible
							if (k.variables[i].islower() and r.variables[i].islower()) and k.variables[i] != r.variables[i]:
								unification = {}
								break
							#if constant1 is set to = constant2 no unification possible
							if k.variables[i][0].isupper() and r.variables[i][0].isupper() and k.variables[i] != r.variables[i]:
								return (None, False)
								unification = {}
								break
							#unification possible. setting mapping here 
							if k.variables[i].islower():
								unification[k.variables[i]] = r.variables[i]
							elif r.variables[i].islower():
								unification[r.variables[i]] = k.variables[i]
					if unification:
						cancelPred.append(k.predicate)
				#removing duplicates 
				if k in unmatched:
					unmatched.remove(k)
				if k.predicate not in cancelPred:
					unmatched.add(copy.deepcopy(k))
			else:
				if k.predicate not in cancelPred:
					unmatched.add(k)
		if r.predicate not in cancelPred:
			unmatchedRes.append(copy.deepcopy(r))

	unmatched = list(unmatched)

	#complete cancellation of sentences. returns the remainder of the sentences after cancellation if any. no unification
	if completeCancel:
		tempArr = []
		for r in res_arr:
			if r.predicate not in cancelPred:
				printSentence(r)
				tempArr.append(copy.deepcopy(r))
		for u in unmatched:
			if u.predicate not in cancelPred:
				printSentence(r)
				tempArr.append(copy.deepcopy(u))
		print "Returning remainder"
		return (tempArr, False)

	if not unification:
		if unmatchedRes and cancelPred:
			returnArr = []
			print "Returning remainder"
			print "cancel pred", cancelPred
			for sent in unmatchedRes:
				if sent.predicate not in cancelPred:
					returnArr.append(sent)
			for sent in unmatched:
				if sent.predicate not in cancelPred:
					returnArr.append(sent)
			return (returnArr, False)
		else:
			print "No unification"
			return (None, False)
	else:
		checkKB = False
		final_matched = []
		final_unmatchedRes = []
		# final_unmatched = copy.deepcopy(unmatched)
		final_unmatched = set()
		seenSentences = set()

		#doing unification process for sentences and returning the remainder 
		if unmatched:
			for u in unmatched:
				final_unmatched.add(copy.deepcopy(u))

		if unmatchedRes:
			for u in unmatchedRes:
				final_unmatched.add(copy.deepcopy(u))

		print unification
		final_unmatched = list(final_unmatched)
		for f in final_unmatched:
			for i in range(0, len(f.variables)):
				if f.variables[i] in unification:
					f.variables[i] = unification[f.variables[i]]
				else:
					checkKB = True
		print "Result"
		printOrsArr(final_unmatched)
		if not final_unmatched:
			print "empty final_unmatched"
			return (["contradiction"], True)
		if checkKB:
			# return unifyKB(final_unmatched)
			return (final_unmatched, True)
		else:
			return (final_unmatched, False)

#function to see if sentence has been seen or not. 
#helps resolution determine whether or not to add this sentence to resList
def seenSentence(arr):	
	#converting array into string form 
	sentence = str()
	# for orsArr in arr:
	for val in arr:
		if val.negation == True:
			sentence += "~" + str(val.predicate) + "("
			for v in val.variables:
				sentence += v + ", "
			sentence = sentence[:-2] + ")"
		else:
			sentence += val.predicate + "("
			for v in val.variables:
				sentence += v + ", "
			sentence = sentence[:-2] + ")"
		sentence += " | " 
	sentence = sentence[:-2]
	if sentence in seen:
		return True
	else:
		seen.append(sentence)
		return False

#function for handling resolution proof 
def resolution():
	#looping through queries and doing the resolution proof
	for q in queries:
		print "------------------Start"
		kb_copy = copy.deepcopy(kb) #2d array
		global kb_constants
		kb_constants = copy.deepcopy(kb_constants_og)
		resQuery = Sentence(q.predicate, q.variables, negateQuery(q.negation)) #negated query
		resList = [] #resolution list 
		resList.append([resQuery])
		#initializing empty sets to be used in resolution
		updatedResList = []
		unmatched = []

		#setting counter for infinite loop check in case of continuing growth of resolving sentences
		counter = 0

		#looping through kb to find things to cancel until contradiction is found
		contradiction = False
		while(contradiction == False and counter < 5000):
			counter += 1
			if counter == 5000:
				contradiction = True
				output.append(False)
					break
			updatedResList = []	
			checkNext = False
			saveNext = False
			#each array in resList
			updatedResList = []
			unifyKBArr = []
			for i in range(0, len(resList)):
				for j in range(0, len(kb_copy)):
					if contradiction:
						output.append(True)
						break
					tup = unifySentence(resList[i], kb_copy[j])
					tempArr = tup[0]
					checkKb = tup[1]
					if tempArr:
						print "returned from unification"
						printOrsArr(tempArr)
						tempArr = removeDuplicates(tempArr)
						print "~~~~Removed duplicates"
						printOrsArr(tempArr)
						unifyKBArr.append(tempArr)

			if not unifyKBArr:
				unifyKBArr = resList

			#checking unification with kb constants 
			print "Checking with kb"
			failedKb = True
			for tempArr in unifyKBArr:
				for k in kb_constants:
					kb_return = []
					if isinstance(k, list):
						kb_return = unifySentence(copy.deepcopy(tempArr), k)
					else:
						kb_return = unifySentence(copy.deepcopy(tempArr), [k])
					tempArrKB = kb_return[0]
					if tempArrKB:
						if "contradiction" in tempArrKB:
							print "hello"
							contradiction = True
							failedKb = False
							break
						failedKb = False
						print "contradiction 1"
						contradiction = checkContradiction(tempArrKB)
						if contradiction:
							break
						if seenSentence(tempArrKB) == False:
							# print "Updating res list 1"
							updatedResList.append(copy.deepcopy(tempArrKB))

				if failedKb == True:
					print "contradiction 2"
					printOrsArr(tempArr)
					contradiction =	checkContradiction(tempArr)
					if contradiction:
						break
					if seenSentence(tempArr) == False:
						# print "Updating res list 3"
						updatedResList.append(copy.deepcopy(tempArr))

			if contradiction:
				output.append(True)
				break
			resList = updatedResList
			if not resList:
				print "here"
				contradiction = True
				output.append(False)
				break

def main():
	readInput()
	resolution()
	createOutput()

if __name__ == "__main__":
	main()