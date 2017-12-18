import sys
text_file = sys.argv[1]

with open(text_file, 'r') as file:
	head = file.readline().rstrip()
	head = int(head)

	sum = 0 #declaring some variables

	string = file.read() #reading second line
	queue = map(int, string.split()) #changing string into an array of int 
	for number in queue:
		sum += abs(head - number)
		head = number
	print sum