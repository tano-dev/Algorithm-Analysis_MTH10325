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

def knapsack(a, S):
    n = len(a)
    dp = [[False] * (S+1) for _ in range(n+1)]

    for i in range(n+1):
        dp[i][0] = True
    
    for i in range(1, n+1):
        for j in range(1, S+1):
            if j < a[i-1]:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = dp[i-1][j] or dp[i-1][j-a[i-1]]
    
    if not dp[n][S]:
        return None

    result = []
    i, j = n, S
    while i > 0 and j > 0:
        if dp[i][j] and not dp[i-1][j]:
            result.append(a[i-1])
            j -= a[i-1]
        
        i -= 1

    return result

S = 200
NUM_TRIALS = 30 
avg_times = []
for n in range(50, 1001, 50):
    total_time = 0
    sample_result = None
    
    for _ in range(NUM_TRIALS):
        a = generate_a(n)

        tic = perf_counter()
        result = knapsack(a, S)
        toc = perf_counter()
        
        total_time += (toc - tic)
        sample_result = result 
        
    avg_time = total_time / NUM_TRIALS
    avg_times.append(avg_time)
    print(f'n = {n}')
    if sample_result:
        print(f'  -Solution subset of {S}: {sample_result}')
    else:
        print(f'  -No subset found that sums to {S}')
        
    print(f'  -Average Time: {avg_time:.6f}s')
    
    
n_values = list(range(50, 1001, 50))
C = avg_times[-1] / (n_values[-1] * S)
bigO_line = [C * (n * S) for n in n_values]

plt.figure(figsize=(10, 6))
plt.plot(n_values, avg_times, marker='o', color='blue', label='knapsack')
plt.plot(n_values, bigO_line, linestyle='--', color='red', label=r'$\mathcal{O}(n \times S)$')
plt.title('Average Time Complexity (S=200)')
plt.xlabel('n')
plt.ylabel('s')
plt.legend()
plt.grid(True)
plt.show()