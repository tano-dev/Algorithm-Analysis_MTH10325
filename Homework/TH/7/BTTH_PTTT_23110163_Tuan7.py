import math
import matplotlib.pyplot as plt
import numpy as np
import time
import random
import heapq
import sys
from time import perf_counter
from math import log2

# Bai 1
def generate_a(n):
    return [random.randint(0, 500) for _ in range(n)]

def find_div10_element(a):
    threshold = math.ceil(len(a) / 10)
    count = {} 

    for x in a:
        if x in count:
            count[x] += 1
        else:
            count[x] = 1
            
    for x in count:
        if count[x] >= threshold:
            return x
        
    return None

n_test = 100
print(f'n = {n_test}')
a_test = generate_a(n_test)

element = find_div10_element(a_test)
if element:
    print(f' -> Tồn tại phần tử lấn chiếm cấp độ 10 là {element}\n')
else:
    print(f' -> Không tồn tại phần tử lấn chiếm cấp độ 10\n')


# Caculate average time and plot
n_values = list(range(10000, 500001, 20000))
avg_times = []
num_trials = 20 

for n in n_values:
    total_time = 0
    for _ in range(num_trials):
        a = generate_a(n)
        
        start_time = time.perf_counter()
        find_div10_element(a)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)
        
    avg_times.append(total_time / num_trials)

C = avg_times[-1] / n_values[-1]
bigO_line = [C * n for n in n_values]


plt.figure(figsize=(10, 6))
plt.plot(n_values, avg_times, marker='o', color='blue', label='find_div10_element')
plt.plot(n_values, bigO_line, linestyle='--', color='red', label=r'$O(n)$')

plt.title('Average Time Complexity')
plt.xlabel('n')
plt.ylabel('seconds')
plt.legend()
plt.grid(True)
plt.show()

# Bai 2
def generate_a_sorted(n):
    return sorted([random.randint(1, 500) for _ in range(n)])

def merge(a, b):
    n = len(a) 
    C = []
    i, j = 0, 0
    
    while i < n and j < n:
        if a[i] <= b[j]:
            C.append(a[i])
            i += 1
        else:
            C.append(b[j])
            j += 1
    
    while i < n:
        C.append(a[i])
        i += 1
    
    while j < n:
        C.append(b[j])
        j += 1
    
    return C


n_test = 5
a_test = generate_a_sorted(n_test)
b_test = generate_a_sorted(n_test)
print(f'a = {a_test}')
print(f'b = {b_test}')
print(f'Merged = {merge(a_test, b_test)}\n')


n_values = list(range(10000, 300001, 20000))
avg_times = []
num_trials = 15

for n in n_values:
    total_time = 0
    for _ in range(num_trials):
        a = generate_a_sorted(n)
        b = generate_a_sorted(n)
        
        start_time = time.perf_counter()
        merge(a, b)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)
        
    avg_times.append(total_time / num_trials)

C = avg_times[-1] / n_values[-1]
bigO_line = [C * n for n in n_values]

# Vẽ đồ thị
plt.figure(figsize=(10, 6))
plt.plot(n_values, avg_times, marker='o', color='blue', label='merge()')
plt.plot(n_values, bigO_line, linestyle='--', color='red', label=r'$O(n)$')

plt.title('Average Time Complexity')
plt.xlabel('n')
plt.ylabel('seconds')
plt.legend()
plt.grid(True)
plt.show()