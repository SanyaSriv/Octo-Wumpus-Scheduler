import argparse
import random
from pathlib import Path
import sys
import os
from threading import Thread
# from threading import Barrier

sys.path.append('.')

from integrate import Scheduler
# barrier = threading.Barrier(3)
def file_op(file1, file2, pid, sched):
    """Function will read from file1 and will write to file 2 in stages: 1 line at a time"""
    f1 = open(file1, 'r')
    f2 = open(file2, 'w')

    for l in f1: # read a line from file 1
        while (sched.check_execution_status(pid) != 1):
            # print(sched.check_execution_status(pid))
            # keep waiting while there is no permission from the scheduler to begin
            continue
        f2.write(l) # write the line read in file 2
    f1.close()
    f2.close()
    sched.mark_finished(pid) # mark done
    print("The thread: {} is going to exit now".format(pid))
    return

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n', type=int, help='Number of threads')
parser.add_argument('-f', '--f', nargs='+', help='List of files to read/write')
parser.add_argument('-p_mode', '--p_mode', help='Protocol mode: (Vanilla lottery (0), wumpus queue (1), alpha inflation (2))')

args = parser.parse_args()

print("The number of threads are: ", args.n)
print("The files getting operated are: ", args.f)
print("Protocol mode is: ", int(args.p_mode))

number_of_threads = int(args.n)
file_list = args.f

# making a scheduler instance here
sched = Scheduler()

sched.octo_wumpus.switch_protocol(int(args.p_mode))

thread_array = []

file_index = 0
for i in range(0, number_of_threads):
    # i = pid
    new_t = Thread(target=file_op, args=(file_list[file_index], file_list[file_index + 1], i, sched))
    thread_array.append(new_t)
    file_index += 2

for i in range(0, number_of_threads):
    thread_array[i].start() # As the execution status will be 0, none of the file operations would begin right now
    # add each of the processes in the scheudler
    sched.add_process(i, random.random()) # giving it a random phi
    print("Added Processes: Ready for execution")

# start the scheduler
print("Starting scheduler.")
sched.run_quantas()
for i in range(0, number_of_threads):
    thread_array[i].join()

file_index = 0
for i in range(0, number_of_threads):
    os.system("diff {} {}".format(file_list[file_index], file_list[file_index]))
    file_index += 1
print("Passed all checks")