import argparse
import sys
from threading import Thread
import random

random.seed(5)

sys.path.append('.')

from integrate import Scheduler

def dfs(start_node, edge_list, end_node, pid, sched):
    while (sched.check_execution_status(pid) != 1):
        continue # keep waiting while there is no permission from the scheduler to begin
    queue = [start_node]
    seen_array = []
    while (len(queue) > 0):
        # keep the DFS going
        while (sched.check_execution_status(pid) != 1):
            continue # wait for the permission from the scheduler
        top_node = queue[-1]
        queue.pop() # removing it from the queue
        seen_array.append(top_node)
        if top_node in edge_list:
            for i in edge_list[top_node]:
                if (i == end_node):
                    sched.mark_finished(pid)
                    return 1 # we are done
                if i not in seen_array:
                    queue.append(i)
    while (sched.check_execution_status(pid) != 1):
        continue
    sched.mark_finished(pid)
    return 1 # when everything is done

def read_file(filename):
    edge_list = {}
    min_node = 1000000 
    max_node = -1 # nodes should always be positive
    f = open(filename, 'r')
    lines = f.readlines()
    for i in range(0, len(lines)):
        e = lines[i].split()
        from_node = int(e[0])
        to_node = int(e[1])
        if from_node in edge_list:
            edge_list[from_node].append(to_node)
        else:
            edge_list[from_node] = [to_node]
        min_node = min(from_node, to_node, min_node)
        max_node = max(from_node, to_node, max_node)
    f.close()
    return edge_list, min_node, max_node


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n', type=int, help='Number of threads')
parser.add_argument('-graph', '--graph', help='Enter the name of the file')
parser.add_argument('-p_mode', '--p_mode', help='Protocol mode: (Vanilla lottery (0), wumpus queue (1), alpha inflation (2))')

args = parser.parse_args()
print(args.graph)
print("Protocol mode is: ", int(args.p_mode))

graph = args.graph
edge_list, min_node, max_node = read_file(graph)

number_of_threads = args.n

start_node = []
end_node = []
sched = Scheduler()

sched.octo_wumpus.switch_protocol(int(args.p_mode))

for i in range(0, number_of_threads):
    # i = pid 
    start_node.append(random.randint(min_node, max_node//2))
    end_node.append(random.randint(start_node[-1] + 1, max_node))

thread_array = []

for i in range(0, number_of_threads):
    # i = pid
    thread_array.append(Thread(target=dfs, args=(start_node[i], edge_list, end_node[i], i, sched)))

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