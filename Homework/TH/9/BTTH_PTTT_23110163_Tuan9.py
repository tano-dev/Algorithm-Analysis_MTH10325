import math
import matplotlib.pyplot as plt
import numpy as np
import time
import random
import heapq
import sys
from time import perf_counter
from math import log2

def f(n):
    result = 0
    while n > 0:
        result += (n % 10) ** 2
        n //= 10
    return result

def find_cycle(n):
    seq = []
    last_number = n
    
    print(n, end=' -> ')
    while last_number not in seq:
        seq.append(last_number)
        new_number = f(last_number)
        if new_number in seq:
            print(new_number)
            seq.append(new_number)
            break    

        print(new_number, end=' -> ')
        last_number = new_number

    end_value = seq[-1]
    i = len(seq) - 2
    while seq[i] != end_value:
        i -= 1

    print(f'Smallest cycle: ', end='')
    while i < len(seq):
        print(seq[i], end=' ')
        i += 1
        
        
n = 85
print(f'{n = }')
find_cycle(n)

print()

n = 23110163
print(f'{n = }')
find_cycle(n)