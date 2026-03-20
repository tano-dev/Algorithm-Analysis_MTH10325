# 1.1
def binary(n: int):
    if n < 0:
        raise ValueError("Error: n is negative")
    bin = ''
    while n > 0:
        div = str(n % 2) # convert to string because 01 = 1 
        bin += div
        n //= 2
    return bin[::-1] 
input = [1, 2, 3, 100, 23110163]
for n in input:
    print(f'binary({n}) = {binary(n)}')

# 1.2
def binary(n):
    if n < 0:
        raise ValueError("Error: n is negative")
    # skip n < 0 because input is N = 100, 200, ..., 1000 

    gan = 0
    soSanh = 0
    bin = ''
    while n:
        soSanh += 1
        div = str(n % 2)
        bin += div
        n //= 2
        
        gan += 3 # 1 for div, 1 for bin, 1 for n

    soSanh += 1 # Because the last comparison break the while loop
    return bin[::-1], gan, soSanh


N = [100*i for i in range(1, 11)]
assignments, comparisons = [], []
for n in N:
    bin, gan, soSanh = binary(n)
    assignments.append(gan)
    comparisons.append(soSanh)
    print(f'binary({n}) = {bin} with assignments = {gan}, comparisons = {soSanh}')

# Plot for Gan(N) and SoSanh(N) and Log2N
from math import log2
import matplotlib.pyplot as plt

log2_plot = list(map(lambda x: log2(x), N))
plt.plot(log2_plot, label='Log2N')
plt.plot(assignments, label='Gan(N)')
plt.plot(comparisons, label='Sosanh(N)')
plt.xlabel('N')
plt.xticks([i for i in range(10)], N)
plt.legend()
plt.show()


# 2
from random import randint

def create_ab(k):
    a = randint(1, k)
    b = randint(1, k)
    while a >= b:
        a = randint(1, k)
        b = randint(1, k)
    return a, b

def createRandomArray(N, k):
    return [randint(1, k) for _ in range(N)]

def algorithm(A, a, b, k):
    count = [0] * (k + 1)
    cum_sum = [0] * (k + 1)
    assignment = 1
    comparison = 0

    for num in A:
        count[num] += 1
        assignment += 1

    
    cum_sum[0] = count[0]
    assignment += 2

    for i in range(1, k + 1):
        cum_sum[i] = cum_sum[i - 1] + count[i]
        assignment += 1

    result = cum_sum[b] - cum_sum[a - 1]
    return result, assignment, comparison

# TH1
bigO_list = []
assignments = []
comparisons = []
k = 100
for N in [10*i for i in range(1, 1001)]:
    A = createRandomArray(N, k)
    a, b = create_ab(k)
    result, assignment, comparison = algorithm(A, a, b, k)
    bigO = N + k

    bigO_list.append(bigO)
    assignments.append(assignment)
    comparisons.append(comparison)

plt.figure(figsize=(10, 5))
plt.plot(bigO_list, label='O(N+k)')
plt.plot(assignments, label='Gan(N, k)')
plt.plot(comparisons, label='Sosanh(N, k)')
plt.xlabel('N')
plt.legend()
plt.title('TH 1: k = 100')
plt.show()

# TH2
bigO_list = []
assignments = []
comparisons = []
N = 20000
for k in [10*i for i in range(1, 1001)]:
    A = createRandomArray(N, k)
    a, b = create_ab(k)
    result, assignment, comparison = algorithm(A, a, b, k)
    bigO = N + k
    bigO_list.append(bigO)
    assignments.append(assignment)
    comparisons.append(comparison)

plt.figure(figsize=(10, 5))
plt.plot(bigO_list, label='O(N+k)')
plt.plot(assignments, label='Gan(N, k)')
plt.plot(comparisons, label='Sosanh(N, k)')
plt.xlabel('k')
plt.legend()
plt.title('TH 2: N = 20000')
plt.show()
