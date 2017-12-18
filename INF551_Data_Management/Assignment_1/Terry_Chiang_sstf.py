import sys
text_file = sys.argv[1]

with open(text_file, 'r') as file:
	head = file.readline().rstrip()
	head = int(head)

	sum = 0 #declaring some variables
	smallest_diff = 0
	difference = 0
	temp_head = 0
	temp = 0
	track_begin = 0
	track_end = 199
	prev_num = 0

	string = file.read() #reading second line
	queue = map(int, string.split()) #changing string into an array of int 
	size_queue = len(queue)
	highest_val = max(queue)
	lowest_val = min(queue)

	min_diff = abs(head - highest_val)

	while len(queue) > 0:
		for number in queue:
			difference = abs(head - number)
			if(difference < min_diff): #looking for minimum distance and storing temp head 
				min_diff = difference
				temp_head = number
				prev_num = number
			elif(difference == min_diff) and (temp_head != highest_val):
				print "hello"
				if len(queue) == size_queue: #if its the first step of the special case
					if(track_end - head) > head: #go to lower end
						 if(number < prev_num):
						 	temp_head = number
						 else:
						 	temp_head = prev_num
					else: #go to higher end
						if(number < prev_num):
							temp_head = prev_num
						else:
							temp_head = number
		sum += abs(head - temp_head) #accumulating sum
		head = temp_head
		queue.remove(temp_head)
		#print temp_head
		min_diff = abs(head - highest_val)

		if(temp_head == highest_val):
			temp_head = lowest_val #last case where only 1 left in the queue
		else:
			temp_head = highest_val 
	print sum