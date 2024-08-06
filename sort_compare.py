import random
import time
import pickle

DATABASE_NAME = "drugs.data"
NUM_ITERATIONS = 999
KEY_TO_SORT_BY = 'Rates'
SUBKEY_TO_SORT_BY = 'Alcohol'
SUBSUBKEY_TO_SORT_BY = 'Use Disorder Past Year'
AGE_GROUP_TO_SORT_BY = '12-17' 

# Load the dataset
with open(DATABASE_NAME, 'rb') as file:
    dataset = pickle.load(file)

print(f"Loaded dataset with {len(dataset)} records.")

def get_sort_key(entry):
    # Extract the value to sort by
    try:
        return entry[KEY_TO_SORT_BY][SUBKEY_TO_SORT_BY][SUBSUBKEY_TO_SORT_BY][AGE_GROUP_TO_SORT_BY]
    except KeyError:
        return float('-inf')

def merge(arr, key_func):
    mid = len(arr) // 2
    i = 0
    j = mid
    k = 0

    aux = [0] * len(arr)

    while i < mid and j < len(arr):
        if key_func(arr[i]) <= key_func(arr[j]):
            aux[k] = arr[i]
            i += 1
        else:
            aux[k] = arr[j]
            j += 1
        k += 1

    while i < mid:
        aux[k] = arr[i]
        i += 1
        k += 1

    while j < len(arr):
        aux[k] = arr[j]
        j += 1
        k += 1

    for k in range(len(aux)):
        arr[k] = aux[k]

def merge_sort(arr, key_func):
    if len(arr) > 1:
        mid = len(arr) // 2

        merge_sort(arr[:mid], key_func)
        merge_sort(arr[mid:], key_func)
    
    merge(arr, key_func)

    return arr

def quick_sort_random_pivot(arr, key_func):
    if len(arr) <= 1:
        return arr
    else:
        pivot_index = random.randint(0, len(arr) - 1)
        pivot = arr[pivot_index]
        left = [x for x in arr if key_func(x) < key_func(pivot)]
        middle = [x for x in arr if key_func(x) == key_func(pivot)]
        right = [x for x in arr if key_func(x) > key_func(pivot)]
        return quick_sort_random_pivot(left, key_func) + middle + quick_sort_random_pivot(right, key_func)

def measure_average_time(sort_function, data, key_func, iterations=NUM_ITERATIONS):
    total_time = 0
    for _ in range(iterations):
        data_copy = data.copy()
        random.shuffle(data_copy) #shuffling to make sure that the way
        #the data is organized has no effect on the outcome
        start_time = time.time()
        sort_function(data_copy, key_func)
        total_time += time.time() - start_time
    return total_time / iterations

data_list = dataset.copy()

print(f"Sorting {len(data_list)} items.")

# Measure average execution time for Merge Sort
merge_sort_time = measure_average_time(merge_sort, data_list, get_sort_key)
print(f"Average execution time for Merge Sort: {merge_sort_time:.6f} seconds")

# Measure average execution time for Quick Sort with Random Pivot
quick_sort_time = measure_average_time(quick_sort_random_pivot, data_list, get_sort_key)
print(f"Average execution time for Quick Sort with Random Pivot: {quick_sort_time:.6f} seconds")
