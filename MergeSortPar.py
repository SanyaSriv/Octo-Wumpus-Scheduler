import random
from threading import Thread
import argparse
import tempfile
import os

from integrate import Scheduler

def merge(part_l, part_r):
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

def merge_sort(arr):
    # Recursive mergeSort
    
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    
    # Partioning of array into 2 lists
    left = arr[:mid]
    right = arr[mid:]
    
    # Sort left part
    left_sorted = merge_sort(left)
    
    # Sort right part
    right_sorted = merge_sort(right)
    
    return merge(left_sorted, right_sorted)

def parallel_merge_sort(arr, num_threads):
    # If only 1 thread, case is same as sequential
    if num_threads <= 1:
        merge_sort(arr)
        
    # Size of each sublist to be sorted
    sort_size = len(arr) // num_threads
    
    sub_sort_lists = [arr[i:i+sort_size] for i in range(0, len(arr), sort_size)]
    
    processes = []
    sorted_sub_lists = []
    
    # Assign sub lists to threads
    for sublist in sub_sort_lists:    
        thread = Thread(target=lambda sub_sort: sorted_sub_lists.append(merge_sort(sublist)), args=(sublist,))
        thread.start()
        processes.append(thread)

    # Sort each sublists assigned to each thread
    for thread in processes:
        thread.join()
    
    # Merging to get final sorted list
    merged = sorted_sub_lists[0]
    for sublist in sorted_sub_lists[1:]:
        merged = merge(merged, sublist)
        
    return merged

def sort_sublist(arr, out_file, pid, sched):
    # Function to sort and write a sublist for temporary store
    while sched.check_execution_status(pid) != 1:
        # Thread waits till it gets a chance to run from scheduler
        continue
    
    # Perform basic merge sort on a sublist
    sorted_result = merge_sort(arr)
    
    # Store sorted sublist (using file as input could be very large)
    with open(out_file, 'w') as file:
        for i in sorted_result:
            file.write(f"{i}\n")
            
    # Thread execution is complete
    sched.mark_finished(pid)

def merge_sort_driver(in_file, out_file, num_threads):
    # Function to perform parallel mergesort with schedular control
    
    # Read data to sort from a file
    with open(in_file, 'r') as file:
        input_numbers = file.readlines()
    
    input_numbers = [int(num.strip()) for num in input_numbers]
    
    sched = Scheduler()
    
    # Size of each sublist to be sorted by a thread
    sort_size = len(input_numbers) // num_threads
    
    # Creating temporary place for threads to store sorted sublists
    temp_files = [tempfile.mkdtemp() for _ in range(num_threads)]
    
    threads = []
    
    for i in range(num_threads):
        sublist = input_numbers[i * sort_size : min((i+1) * sort_size, len(input_numbers))]
        pid = i
        sched.add_process(pid, random.random())
        
        thread = Thread(target=sort_sublist, args=(sublist, temp_files[i], pid, sched))
        threads.append(thread)
        thread.start()
        
        print("Added Processes: Ready for execution")
    
    # start the scheduler
    print("Starting scheduler.")
    sched.run_quantas()
    
    for thread in threads:
        thread.join()
        
    sorted_numbers = []
    for temp_file in temp_files:
        with open(temp_file, 'r') as file:
            sorted_numbers.append([int(i.strip()) for i in file.readlines()])
        os.remove(temp_file)
    
    sorted_result = sorted_numbers[0]
    
    # Merging all the sorted sublists to one
    for part in sorted_numbers[1:]:
        sorted_result = merge(sorted_result, part)
    
    with open(out_file, 'w') as file:
        for i in sorted_result:
            file.write(f"{i}\n")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True, help='File to sort path')
    parser.add_argument('-o', '--output_file', required=True, help='Sorted output file path')
    parser.add_argument('-n', '--num_threads', type=int, default=1, help='Number of threads')
    args = parser.parse_args()
    
    print("The number of threads are: ", args.n)

    merge_sort_driver(args.input_file, args.output_file, args.num_threads)