import copy

process_list = []
total_wait = 0
total_turnaround_time = 0


def sort_list():
	global process_list
	process_list = sorted(process_list, key=lambda x: x[2])


def sort_selection(sort_num):
	switcher = {
		1: "You've selected sort option 1: FCFS",
		2: "You've selected sort option 2: HPF",
		3: "You've selected sort option 3: RR",
		4: "You've opted to run all sorts!"
	}

	return switcher.get(sort_num, '')


def sum_time(summed_list):
	tot = 0
	for z in range(len(summed_list)):
		tot += summed_list[z][1]
	return tot


def round_robin(quantum, temp_list):
	ta_counter = 0
	done = False
	print(f"\n<><><><><><><><><><> BEGIN PREEMPTIVE ROUND ROBIN SCHEDULING <><><><><><><><><><>\n")

	while not done:
		for i in range(len(process_list)):
			if process_list[i][1] <= 0:
				print(f"(RR) Process number {process_list[i][0]} has already completed")
				pass
			else:
				print(f"(RR) Processing process number {process_list[i][0]} now...")
				print(f"(RR) Process number {process_list[i][0]} has {process_list[i][1]} time slices left")
				print(f"(RR) Applying time slice of {quantum} to process number {process_list[i][0]}...")
				if (process_list[i][1] - quantum) < 0:
					ta_counter += 1
					process_list[i][1] = 0
					print(
						f"(RR) Turnaround time for process {process_list[i][0]} = {ta_counter}, needed: {temp_list[i][1]}, and {temp_list[i][1] / quantum} time slices")
				else:
					ta_counter += 1
					process_list[i][1] -= quantum
				print(f"(RR) Process number {process_list[i][0]} now has {process_list[i][1]} time slices remaining")

		if sum_time(process_list) <= 0:
			done = True

	print(f"(RR) Throughput for the {int(process_list.__len__())} processes = {int(process_list.__len__()) / sum_time(temp_list)}")
	print(f"(RR) Average RR Turnaround time for {process_list.__len__()} processes with quantum {quantum}: {sum_time(temp_list) / process_list.__len__()}")
	print(f"\n<><><><><><><><><><> END PREEMPTIVE ROUND ROBIN SCHEDULING <><><><><><><><><><>\n")


def run_scheduler(sort_type):
	global process_list, total_wait, total_turnaround_time

	print(f"\n<><><><><><><><><><> BEGIN {sort_type} SCHEDULING <><><><><><><><><><>\n")

	for i in range(len(process_list)):
		print(f"({sort_type}) Processing process number {process_list[i][0]} now...")
		if i == 0:
			print(f"({sort_type}) Wait time for process {process_list[i][0]} = 0")
			print(f"({sort_type}) Turnaround time for process {process_list[i][0]} = {int(process_list[i][1])}")
			total_turnaround_time += int(process_list[i][1])
		else:
			turnaround_time = total_wait
			total_turnaround_time += turnaround_time
			total_wait += int(process_list[i][1])
			print(f"({sort_type}) Total wait time for process {process_list[i][0]} = {total_wait}")
			print(f"({sort_type}) Total turnaround time for process {process_list[i][0]} = {turnaround_time}")

	print(f"({sort_type}) Average wait time for the {int(process_list.__len__())} processes = {total_wait / int(process_list.__len__())}")
	print(f"({sort_type}) Average turnaround time for the {int(process_list.__len__())} processes = {total_turnaround_time / (int(process_list.__len__()))}")
	print(f"({sort_type}) Throughput for the {int(process_list.__len__())} processes = {int(process_list.__len__()) / sum_time(process_list)}")

	print(f"\n<><><><><><><><><><> END {sort_type} SCHEDULING <><><><><><><><><><>\n")


prompt_process = input('Do you have a process to add? (Press y or yes if you would like to continue)\n')

if prompt_process.lower() == 'yes' or prompt_process.lower() == 'y':
	get_process = list(map(int, input(
		'Add your process as a triple in the following format with spaces between each value\n(e.g., <Process ID> <Completion time for process> <Priority for process>):\n').strip().split()))
	process_list.append(get_process)
	prompt_process = input('Do you have another process to add? (Press y or yes if you would like to continue)\n')

	while prompt_process.lower() == 'yes' or prompt_process.lower() == 'y':
		get_process = list(map(int, input(
			'Add your process as a triple in the following format with spaces between each value\n(e.g., <Process ID> <Completion time for process> <Priority for process>):\n').strip().split()))
		process_list.append(get_process)
		prompt_process = input('Do you have a process to add? (Press y or yes if you would like to continue)\n')
else:
	exit(0)

print('\n')

for x in range(len(process_list)):
	print(f"Process {process_list[x][0]} needs {process_list[x][1]}ms and has a priority of {process_list[x][2]}")

which_sort = int(input(
	'Which sorting algorithm would you like to run?\nPress 1 for FCFS sorting\nPress 2 for HPF sorting\nPress 3 for RR sorting\nPress 4 to do it all!\n'))

if which_sort < 1 or which_sort > 4:
	print('Sorry, you\'ve entered an incorrect sorting option. Bye!')
	exit(0)
elif which_sort == 3 or which_sort == 4:
	print(sort_selection(which_sort))
	time_quantum = int(
		input('Since you chose an option with round robin scheduling, what time quantum would you like?\n'))
else:
	print(sort_selection(which_sort))

temp_list = copy.deepcopy(process_list)

if which_sort == 1:
	run_scheduler('FCFS')
elif which_sort == 2:
	sort_list()
	print('The process list has been updated to:\n', ('\n'.join(' '.join(map(str, sub)) for sub in process_list)))
	run_scheduler('HPF')
elif which_sort == 3:
	sort_list()
	print('The process list has been updated to:\n', ('\n'.join(' '.join(map(str, sub)) for sub in process_list)))
	round_robin(time_quantum, temp_list)
elif which_sort == 4:
	run_scheduler('FCFS')
	print('FCFS scheduling has completed.\nNow sorting process list for HPF and RR schedulers.')
	sort_list()
	run_scheduler('HPF')
	print('HPF scheduling has completed.\nNow running RR scheduling.')
	round_robin(time_quantum, temp_list)
	print('All schedulers completed.\nGoodbye!')

exit(0)
