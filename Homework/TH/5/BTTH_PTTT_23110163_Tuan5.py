import matplotlib.pyplot as plt
import numpy as np
import time
import random
import heapq
import sys
from time import perf_counter
from math import log2

# Bai 1

def generate_matrix(n):
    return np.random.randint(1, 1001, size=(n, n))

# 1
def multiply(A, B):
    row_A, col_A = len(A), len(A[0])
    row_B, col_B = len(B), len(B[0])

    if col_A != row_B:
        raise ValueError('invalid dimensions')

    C = [[0 for _ in range(col_B)] 
         for _ in range(row_A)]

    for i in range(row_A):
        for j in range(col_B):
            for k in range(row_B):
                C[i][j] += A[i][k] * B[k][j]
    return C


# 2

def split(matrix):
    n = len(matrix)
    return matrix[:n//2, :n//2], matrix[:n//2, n//2:], matrix[n//2:, :n//2], matrix[n//2:, n//2:]

def strassen(A, B):
    if len(A) == 1:
        return A * B

    a11, a12, a21, a22 = split(A)
    b11, b12, b21, b22 = split(B)

    p1 = strassen(a11 + a22, b11 + b22)
    p2 = strassen(a21 + a22, b11)
    p3 = strassen(a11, b12 - b22)
    p4 = strassen(a22, b21 - b11)
    p5 = strassen(a11 + a12, b22)
    p6 = strassen(a21 - a11, b11 + b12)
    p7 = strassen(a12 - a22, b21 + b22)

    c11 = p1 + p4 - p5 + p7
    c12 = p3 + p5
    c21 = p2 + p4
    c22 = p1 + p3 - p2 + p6
    return np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))

T_normal, T_strassen = [], []
Ns = []
# wtf why the frick k = 10-32 is too much for a potato laptop :skull:
for k in range(1, 10):
    n = 2 ** k
    Ns.append(n)
    print(f'{k = }, {n = }')
    A = generate_matrix(n)
    B = generate_matrix(n)
    
    
    tic = perf_counter()
    C = multiply(A, B)
    T_normal.append(perf_counter() - tic)
    print('Basic multi:' + f' {T_normal[-1]:.4f} s')
    
    tic = perf_counter()
    C = strassen(A, B)
    T_strassen.append(perf_counter() - tic)
    print('Strassen multi:' + f' {T_strassen[-1]:.4f} s')


bigO_line = list(map(lambda x: x**3, Ns))
plt.figure(figsize=(8, 5))
ax = plt.gca()
ax2 = ax.twinx()
ax.set_xlabel('N')
line1, = ax.plot(bigO_line, label=r'O(N^3)', color='r', ls='--', alpha=0.8)
ax.set_ylabel('Time Complexity')
line2, = ax2.plot(T_normal, label=r'T_normal(N)', color='C0', alpha=0.8)
ax2.set_ylabel('s')
ax.legend(handles=[line1, line2])
plt.title('time complexity of basic matrix multiplication')
plt.show()

bigO_line = list(map(lambda x: x**np.log2(7), Ns))
plt.figure(figsize=(8, 5))
ax = plt.gca()
ax2 = ax.twinx()
ax.set_xlabel('N')
line1, = ax.plot(bigO_line, label=r'O(N^log2(7))', color='r', ls='--', alpha=0.8)
ax.set_ylabel('Time Complexity')
line2, = ax2.plot(T_strassen, label=r'T_strassen(N)', color='C0', alpha=0.8)
ax2.set_ylabel('s')
ax.legend(handles=[line1, line2])
plt.title('time complexity of Strassen\'s algorithm')
plt.show()
# combine 2 plots
plt.figure(figsize=(8, 5))
ax = plt.gca()
ax2 = ax.twinx()
ax.set_xlabel('N')
ax.set_ylabel('Time Complexity')
line1, = ax2.plot(T_strassen, label=r'T_strassen(N)', color='C0', alpha=0.8)
line2, = ax2.plot(T_normal, label=r'T_normal(N)', color='C1', alpha=0.8)
ax2.set_ylabel('s')
ax.legend(handles=[line1, line2])
plt.title('comparison of basic multi and Strassen multi')