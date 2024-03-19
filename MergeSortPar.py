from threading import Thread

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