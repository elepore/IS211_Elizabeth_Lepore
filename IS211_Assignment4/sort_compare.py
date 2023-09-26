import argparse
import sys
import random
import time

class DummyStream:
    def write(self, *args, **kwargs):
        pass

def suppress_output():
    sys.stdout = DummyStream()

def restore_output():
    sys.stdout = sys.__stdout__


def get_me_random_list(n):
    """Generate list of n elements in random order
    
    :params: n: Number of elements in the list
    :returns: A list with n elements in random order
    """
    a_list = list(range(n))
    random.shuffle(a_list)
    return a_list


def insertion_sort(a_list):
    start_time = time.time()
    for index in range(1, len(a_list)):
        current_value = a_list[index]
        position = index

        while position > 0 and a_list[position - 1] > current_value:
            a_list[position] = a_list[position - 1]
            position = position - 1

        a_list[position] = current_value
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def shellSort(alist):
    start_time = time.time()
    sublistcount = len(alist)//2
    while sublistcount > 0:
        for startposition in range(sublistcount):
            gapInsertionSort(alist,startposition,sublistcount)

        print("After increments of size", sublistcount, "The list is",alist)

        sublistcount = sublistcount // 2
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def gapInsertionSort(alist, start, gap):

    for i in range(start+gap, len(alist), gap):
        currentvalue = alist[i]
        position = i

        while position >= gap and alist[position-gap] > currentvalue:
            alist[position] = alist[position-gap]
            position = position - gap

        alist[position] = currentvalue

def python_sort(a_list):
    """
    Use Python built-in sorted function

    :param a_list:
    :return: the sorted list
    """
    start_time = time.time()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return sorted(a_list), elapsed_time



if __name__ == "__main__":

    avg_times = {
        'insertion_sort': 0,
        'shellSort': 0,
        'gapInsertionSort': 0,
        'python_sort': 0 
    }
    
    num_trials = 100
    list_sizes = [500, 1000, 10000]
    
    for size in list_sizes:
        total_times = {
            'insertion_sort': 0,
            'shellSort': 0,
            'python_sort': 0 

        }
        
        for _ in range(num_trials):
            
            suppress_output()  

            random_list = get_me_random_list(size)  
            
            time_taken = insertion_sort(random_list)
            total_times['insertion_sort'] += time_taken
            
            time_taken = shellSort(random_list)
            total_times['shellSort'] += time_taken

            _, time_taken = python_sort(random_list)
            total_times['python_sort'] += time_taken  
            
            restore_output()

        for key in total_times:
            avg_times[key] = total_times[key] / num_trials
        
        print(f"Average times for list size {size}:")
        print(f"Insertion Sort took {avg_times['insertion_sort']:10.7f} seconds to run, on average, on average for a list of {size} elements")
        print(f"Shell Sort took {avg_times['shellSort']:10.7f} seconds to run, on average, on average for a list of {size} elements")
        print(f"Python Sort took {avg_times['python_sort']:10.7f} seconds to run, on average, on average for a list of {size} elements")

