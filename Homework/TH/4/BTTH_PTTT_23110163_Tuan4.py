import matplotlib.pyplot as plt
import numpy as np
import time
import random
import heapq
import sys
from time import perf_counter
from math import log2

# Bài 1
def RNG_A(N):
    return sorted(random.sample(range(1, N*100 + 1), N))

def binary_search(A, target):
    l, r = 0, len(A)-1
    while l <= r:
        m = (l + r) // 2
        if A[m] == target:
            return m

        if A[m] > target:
            r = m - 1
        else:
            l = m + 1

    return None

T = []
N = [10*i for i in range(1, 1001)]
for n in N:
    A = RNG_A(n)
    x = random.choice(A)
    
    tic = perf_counter()
    index = binary_search(A, x)
    T.append(perf_counter() - tic)
    
    T[-1] = T[-1] * 1e6 
     
    # if index:
    #     print(f'Found {x} at {index}')
    # else:
    #     print('Not found')
        

plt.plot(N, T, label='Binary Search')
plt.plot(N, [log2(n) for n in N], label='O(log N)', linestyle='--')
plt.xlabel('N')
plt.ylabel('microseconds')
plt.title('Binary Search Time Complexity')
plt.legend()
plt.grid()
plt.show()


# Bài 2
def RNG_S(N):
    return random.sample(range(1, 1001), N)

def find_k_smallest(S, k):
    if not S:
        return None
        
    pivot = random.choice(S)
    
    left = [x for x in S if x < pivot]   
    mid = [x for x in S if x == pivot]   
    right = [x for x in S if x > pivot]
    
    L = len(left)
    M = len(mid)
    
    if k <= L:
        return find_k_smallest(left, k)
        
    elif k > L + M:
        return find_k_smallest(right, k - L - M)
        
    else:
        return mid[0]

k = 5
num_trials = 1000 
avg_time_arr = []
for N in range(10, 101, 10):
    total_time = 0
    
    for _ in range(num_trials):
        start_time = perf_counter()
        S = RNG_S(N)
        total_time += (perf_counter() - start_time)
        
    avg_time = total_time / num_trials
    avg_time *= 1e6
    avg_time_arr.append(avg_time)
    
    sample_S = RNG_S(N)
    result = find_k_smallest(sample_S, k)
    
    print(f'{N = }, k-smallest = {result}, avg time = {avg_time:.8f} microseconds')
    
plt.plot(range(10, 101, 10), avg_time_arr, marker='o')
plt.plot(range(10, 101, 10), [N for N in range(10, 101, 10)], label='O(N)', linestyle='--')
plt.legend()
plt.xlabel('N')
plt.ylabel('microseconds')
plt.title('Average Time to Generate Unique Set of Size N')
plt.grid()
plt.show()

 
