import sys
text_file = sys.argv[1]

with open(text_file, 'r') as file:
	head = file.readline().rstrip()
	head = int(head)
	original_head = head

	sum = 0 #declaring some variables
	difference = 0
	temp_head = 0
	track_begin = 0
	track_end = 199

	string = file.read() #reading second line
	queue = map(int, string.split()) #changing string into an array of int 
	queue.sort() #are we allowed to sort??? 
	max_val = max(queue)
	min_val = min(queue)

	min_diff = head - max_val

	#if(track_end - head) > (head): #jump to lower end first
	for number in reversed(queue):
		if number < head:
			sum += (head - number)
			head = number
	head = max_val
	for number in reversed(queue):
		if original_head > number:
			break
		if number < head:
			sum += (head-number)
			head = number
	print sum



