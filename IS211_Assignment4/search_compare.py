import time
import random


def get_me_random_list(n):
    """Generate list of n elements in random order
    
    :params: n: Number of elements in the list
    :returns: A list with n elements in random order
    """
    a_list = list(range(n))
    random.shuffle(a_list)
    return a_list

def sequential_search(a_list, item):
    start_time = time.time()
    first = 0

    last = len(a_list) - 1
    found = False
    while first <= last and not found:
        midpoint = (first + last) // 2
        if a_list[midpoint] == item:
            found = True
        else:
            if item < a_list[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1
                
    end_time = time.time()
    elapsed_time = end_time - start_time
    return found, elapsed_time

def ordered_sequential_search(a_list, item):
    start_time = time.time()
    pos = 0
    found = False
    stop = False
    while pos < len(a_list) and not found and not stop:
        if a_list[pos] == item:
            found = True
        else:
            if a_list[pos] > item:
                stop = True
            else:
                pos = pos + 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    return found, elapsed_time

def binary_search_iterative(a_list,item):
    start_time = time.time()
    first = 0
    last = len(a_list) - 1
    found = False
    while first <= last and not found:
        midpoint = (first + last) // 2
        if a_list[midpoint] == item:
            found = True
        else:
            if item < a_list[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    return found, elapsed_time

def binary_search_recursive(a_list,item):
    start_time = time.time()
    if len(a_list) == 0:
        end_time = time.time()
        elapsed_time = end_time - start_time
        return False, elapsed_time
    else:
        midpoint = len(a_list) // 2
        if a_list[midpoint] == item:
            end_time = time.time()
            elapsed_time = end_time - start_time
            return True, elapsed_time
        else:
            if item < a_list[midpoint]:
                return binary_search_recursive(a_list[:midpoint], item)
            else:
                return binary_search_recursive(a_list[midpoint + 1:], item)



if __name__ == "__main__":
    """Main entry point"""

    avg_times = {
        'sequential_search': 0,
        'ordered_sequential_search': 0,
        'binary_search_iterative': 0,
        'binary_search_recursive': 0
    }
    
    num_trials = 100
    list_sizes = [500, 1000, 10000]
    
    for size in list_sizes:
        total_times = {
            'sequential_search': 0,
            'ordered_sequential_search': 0,
            'binary_search_iterative': 0,
            'binary_search_recursive': 0
        }
        
        for _ in range(num_trials):
            random_list = get_me_random_list(size)  
            item = -1
            
            _, time_taken = sequential_search(random_list, item)
            total_times['sequential_search'] += time_taken
            
            _, time_taken = ordered_sequential_search(sorted(random_list), item)
            total_times['ordered_sequential_search'] += time_taken
            
            _, time_taken = binary_search_iterative(sorted(random_list), item)
            total_times['binary_search_iterative'] += time_taken
            
            _, time_taken = binary_search_recursive(sorted(random_list), item)
            total_times['binary_search_recursive'] += time_taken
        
        for key in total_times:
            avg_times[key] = total_times[key] / num_trials
        
        print(f"Average times for list size {size}:")
        print(f"Sequential Search took {avg_times['sequential_search']:10.7f} seconds to run, on average for a list of {size} elements")
        print(f"Ordered Sequential Search took {avg_times['ordered_sequential_search']:10.7f} seconds to run, on average for a list of {size} elements")
        print(f"Binary Search Iterative took {avg_times['binary_search_iterative']:10.7f} seconds to run, on average for a list of {size} elements")
        print(f"Binary Search Recursive took {avg_times['binary_search_recursive']:10.7f} seconds to run, on average for a list of {size} elements")

