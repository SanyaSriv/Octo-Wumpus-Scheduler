import sys

filename = sys.argv[1]
f = open(filename, 'r')

lines = f.readlines()
filename_1 = filename.split(".")[0] + "_fairness_ratio.txt"
filename_2 = filename.split(".")[0] + "_ticket_changes_per_epoch.txt"
filename_3 = filename.split(".")[0] + "_allocated_tickets_per_total_num.txt"
filename_4 = filename.split(".")[0] + "_turns_per_total_num.txt"

epoch_size = filename.split(".")[0] + "_epoch_size.txt"
master_fairness_dictionary = []

epoch_begin = 0
epoch_dictionry = {}
ticket_dictionary = {}
ticket_count_per_epoch = []
epoch_size_dictionary = {}
current_epoch_number = 0
allocated_tickets_per_num_tickets = []
turns_per_num_tickets = []

for i in lines:
	if "Winning process in quanta" in i:
		output = i.split()
		quanta_number = int(output[4])
		process_id = int(output[6])
		num_tickets = int(output[10])
		ticket_dictionary[process_id] = num_tickets
		if process_id in epoch_dictionry:
			epoch_dictionry[process_id] += 1
		else:
			epoch_dictionry[process_id] = 1
	if "Next epoch begin:" in i:
		# print stats for this epoch
		current_epoch_number = i.split()[3]
		# calculating the fairness
		fair = {}
		alloc_tick = {}
		turn = {}
    
		assert(sum(ticket_dictionary.values()) == sum(epoch_dictionry.values())) # asserting that the protocol is working properly
		sum_of_tickets = sum(ticket_dictionary.values())
		for j in ticket_dictionary:
			fair[str(j)] = str(epoch_dictionry[j] / ticket_dictionary[j])
			turn[str(j)] = str(epoch_dictionry[j] / sum_of_tickets)
			alloc_tick[str(j)] = str(ticket_dictionary[j] / sum_of_tickets)
		
		allocated_tickets_per_num_tickets.append(alloc_tick)
		turns_per_num_tickets.append(turn)
		master_fairness_dictionary.append(fair)

		str_ticket_dictionary = {}
		
		for j in ticket_dictionary:
			str_ticket_dictionary[str(j)] = str(ticket_dictionary[j])
      
		ticket_count_per_epoch.append(str_ticket_dictionary)
		epoch_begin = int(current_epoch_number)
		# resetting everything here
		epoch_dictionry = {}
		ticket_dictionary = {}
	if "Total tickets/epoch length:" in i:
		# make a nwe dictionary that keeps a track of increasing number of tickets with epochs
		epoch_size_dictionary[str(current_epoch_number)] = i.split()[3]

f.close()

with open(filename_2, 'w') as f:
  f.write(str(ticket_count_per_epoch))

with open(epoch_size, 'w') as f:
  f.write(str(epoch_size_dictionary))

with open(filename_1, 'w') as f:
  f.write(str(master_fairness_dictionary))

with open(filename_3, 'w') as f:
	f.write(str(allocated_tickets_per_num_tickets))

with open(filename_4, 'w') as f:
	f.write(str(turns_per_num_tickets))
  

