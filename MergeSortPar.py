import random
from threading import Thread
import argparse
import tempfile
import os

from integrate import Scheduler

def merge(part_l, part_r, pid, sched):
    # Function to merge two sorted lists
    
    while sched.check_execution_status(pid) != 1:
        # Thread waits till it gets a chance to run from scheduler
        continue
    
    merged = []
    
    i = 0
    j = 0
    
    while i < len(part_l) and j < len(part_r):
        while sched.check_execution_status(pid) != 1:
            # Thread waits till it gets a chance to run from scheduler
            continue
        if part_l[i] < part_r[j]:
            merged.append(part_l[i])
            i += 1
        else:
            merged.append(part_r[j])
            j += 1
    
    while i < len(part_l):
        while sched.check_execution_status(pid) != 1:
            # Thread waits till it gets a chance to run from scheduler
            continue
        merged.append(part_l[i])
        i += 1
    
    while j < len(part_r):
        while sched.check_execution_status(pid) != 1:
            # Thread waits till it gets a chance to run from scheduler
            continue
        merged.append(part_r[j])
        j += 1
        
    while sched.check_execution_status(pid) != 1:
        # Thread waits till it gets a chance to run from scheduler
        continue
    return merged

def merge_sort(arr, pid, sched):
    # Recursive mergeSort
    while sched.check_execution_status(pid) != 1:
        # Thread waits till it gets a chance to run from scheduler
        continue
    
    if len(arr) <= 1:
        return arr
    
    while sched.check_execution_status(pid) != 1:
        # Thread waits till it gets a chance to run from scheduler
        continue
    
    # Partioning of array into 2 lists
    mid = len(arr) // 2
    
    # Sort left part
    left_sorted = merge_sort(arr[:mid], pid, sched)
    
    # Sort right part
    right_sorted = merge_sort(arr[mid:], pid, sched)
    
    return merge(left_sorted, right_sorted, pid, sched)

def sort_sublist(arr, out_file, pid, sched):
    # Function to sort and write a sublist for temporary store
    while sched.check_execution_status(pid) != 1:
        # Thread waits till it gets a chance to run from scheduler
        continue
    
    # Perform basic merge sort on a sublist
    sorted_result = merge_sort(arr, pid, sched)
    
    # Store sorted sublist (using file as input could be very large)
    with open(out_file, 'w') as file:
        for i in sorted_result:
            while sched.check_execution_status(pid) != 1:
                # Thread waits till it gets a chance to run from scheduler
                continue
            file.write(f"{i}\n")
   
    # Thread execution is complete
    sched.mark_finished(pid)

def merge_driver(part_l, part_r):
    # Function to merge two sorted lists
    merged = []
    
    i = 0
    j = 0
    
    while i < len(part_l) and j < len(part_r):
        if part_l[i] < part_r[j]:
            merged.append(part_l[i])
            i += 1
        else:
            merged.append(part_r[j])
            j += 1
    
    while i < len(part_l):
        merged.append(part_l[i])
        i += 1
    
    while j < len(part_r):
        merged.append(part_r[j])
        j += 1
        
    return merged

def merge_n_lists(sorted_lists):
    sorted_result = sorted_lists[0]
    # Merging all the sorted sublists to one
    for part in sorted_lists[1:]:
        sorted_result = merge_driver(sorted_result, part)

    return sorted_result

def merge_sort_driver(in_file, out_file, num_threads, p_mode):
    # Function to perform parallel mergesort with schedular control
    
    # Read data to sort from a file
    with open(in_file, 'r') as file:
        input_numbers = file.readlines()
    
    input_numbers = [int(num.strip()) for num in input_numbers]
    
    sched = Scheduler()
    
    sched.octo_wumpus.switch_protocol(int(p_mode))

    # Size of each sublist to be sorted by a thread
    sort_size = len(input_numbers) // num_threads
    # sort_size += 1
    # Creating temporary place for threads to store sorted sublists
    temp_files = []
    for i in range(0, num_threads):
        temp_files.append("file_{}.txt".format(i))
    
    threads = []
    
    for i in range(num_threads):
        if i != num_threads - 1:
            sublist = input_numbers[i * sort_size : min((i+1) * sort_size, len(input_numbers))]
        else:
            sublist = input_numbers[i * sort_size : len(input_numbers)]
        pid = i
        sched.add_process(pid, random.random())
        thread = Thread(target=sort_sublist, args=(sublist, temp_files[i], pid, sched))
        threads.append(thread)
    
    for i in range(0, num_threads):
        threads[i].start()

    print("Added Processes: Ready for execution")
    # start the scheduler
    print("Starting scheduler.")
    sched.run_quantas()
    
    for thread in threads:
        thread.join()
        
    sorted_numbers = []
    for temp_file in temp_files:
        with open(temp_file, 'r') as file:
            sorted_part = []
            for i in file:
                sorted_part.append(int(i))
            sorted_numbers.append(sorted_part)
        os.remove(temp_file)
    sorted_result = merge_n_lists(sorted_numbers)
    
    with open(out_file, 'w') as file:
        for i in sorted_result:
            file.write(f"{i}\n")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True, help='File to sort path')
    parser.add_argument('-o', '--output_file', required=True, help='Sorted output file path')
    parser.add_argument('-n', '--num_threads', type=int, default=1, help='Number of threads')
    parser.add_argument('-p_mode', '--p_mode', help='Protocol mode: (Vanilla lottery (0), wumpus queue (1), alpha inflation (2))')
    args = parser.parse_args()
    
    print("The number of threads are: ", args.num_threads)
    print("Protocol mode is: ", args.p_mode)
    merge_sort_driver(args.input_file, args.output_file, args.num_threads, args.p_mode)