import random
import matplotlib.pyplot as plt
import numpy as np
from time import perf_counter
from math import log2

# Bài 1
def findN_Alpha(func):
    arr = np.linspace(10, 1000)
    vals = np.abs(func(arr))
    
    alphas = np.log(vals) / np.log(arr)
    max_alpha = np.nanmax(alphas)
    
    if max_alpha == np.inf:
        print(f' O(n^a) not exist')
        return None
    else:
        print(f' f ~= O(n^{round(max_alpha)}) ')
        return max_alpha
    
def func_a(n): 
    return n**2
def func_b(n): 
    return n**3 + np.cos(n) * n**4
def func_c(n): 
    return n**n
def func_d(n): 
    return n**3 + n**2 + n + 1

print("a)", end="")
findN_Alpha(func_a)
print("b)", end="")
findN_Alpha(func_b)
print("c)", end="")
findN_Alpha(func_c)
print("d)", end="")
findN_Alpha(func_d)


# Bài 2
def listRNG(N):
    n = []
    for _ in range(N):
        n.append(random.randint(0, 9))

    while n[0] == 0:
        n[0] = random.randint(1, 9)
    return n

def to_list(n):
    l = []
    while n:
        l.insert(0, n % 10)
        n //= 10

    return l

def list_to_number(digits):
    number = 0
    for digit in digits:
        number = number * 10 + digit
    return number

def plot_time_complexity(T, bigO_line, bigO_label, title=''):

    plt.figure(figsize=(8, 5))
    ax = plt.gca()
    ax2 = ax.twinx()
    ax.set_xlabel('N')

    line1, = ax.plot(bigO_line, label=bigO_label, color='r', ls='--', alpha=0.8)
    ax.set_ylabel('Độ phức tạp thời gian', color=line1.get_color())
    line2, = ax2.plot(T, label='T(N)', color='C0', alpha=0.8)
    ax2.set_ylabel('Thời gian thực hiện (s)', color=line2.get_color())
    ax.legend(handles=[line1, line2])

    if title:
        plt.title(title)

    plt.show()
    
# 2a
def classic_multiply(A, B):
    len_a, len_b = len(A), len(B)
    res = [0] * (len_a + len_b)
    
    for i in range(len_a - 1, -1, -1):
        carry = 0
        for j in range(len_b - 1, -1, -1):
            temp = A[i] * B[j] + res[i + j + 1] + carry
            res[i + j + 1] = temp % 10
            carry = temp // 10
        res[i] += carry
        
    while len(res) > 1 and res[0] == 0:
        res.pop(0)
        
    return int("".join(map(str, res)))


T_a = []
Ns_a = []
for k in range(13):
    N = 2 ** k
    Ns_a.append(N)
    A = listRNG(N)
    B = listRNG(N)

    tic = perf_counter()
    classic_multiply(A, B)
    toc = perf_counter()

    duration = toc - tic
    print(f'{k = }, took {duration}s')
    T_a.append(duration)


    
bigO_line_a = list(map(lambda x: x**2, Ns_a))
plot_time_complexity(T_a, bigO_line_a, bigO_label='$O(N^2)$',title=f'Comparison 2a vs $O(N^2)$')

# 2b
def split(n: int):
    return divmod(n, 10**(numlength(n)//2))

def numlength(n: int):
    l = 0
    while n:
        n //= 10
        l += 1
    return l

def karatsuba_multiply(A, B):
    # Điều kiện dừng đệ quy
    if A < 10 or B < 10:
        return int(A * B)

    # Tìm mốc chia đôi m dựa trên số dài nhất
    str_A, str_B = str(A), str(B)
    n = max(len(str_A), len(str_B))
    m = n // 2
    
    # Lũy thừa để chia cắt số
    power = 10 ** m
    
    # Chia A = A_1 * 10^m + A_2
    A_1, A_2 = divmod(A, power)
    B_1, B_2 = divmod(B, power)
    
    # 3 lệnh gọi đệ quy Karatsuba
    C = karatsuba_multiply(A_1, B_1)          # Tương đương z2
    D = karatsuba_multiply(A_2, B_2)          # Tương đương z0
    E = karatsuba_multiply(A_1 + A_2, B_1 + B_2) - C - D  # Tương đương z1 - z2 - z0
    
    # Gộp lại theo mốc m đã định: C * 10^(2m) + E * 10^m + D
    return (C * (10 ** (2 * m))) + (E * power) + D

def rng(N):
    n = random.randint(0, 9)
    while n == 0:
        n = random.randint(0, 9)

    i = 1
    while i < N:
        n = n*10 + random.randint(0, 9)
        i += 1
    return n


T_b = []
Ns_b = []
for k in range(13):
    N = 2 ** k
    Ns_b.append(N)
    A = rng(N)
    B = rng(N)

    tic = perf_counter()
    karatsuba_multiply(A, B)
    toc = perf_counter()

    duration = toc - tic
    print(f'{k = }, took {duration}s')
    T_b.append(duration)

bigO_line_b = list(map(lambda x: x**log2(3) , Ns_b))
plot_time_complexity(T_b, bigO_line_b, bigO_label='$O(N^{\log{3}})$',title='Comparison 2b vs $O(N^{\log{3}})$')



# So sánh 2 phương pháp
# Tính hệ số C để chuẩn hóa đường lý thuyết về cùng đơn vị thời gian (giây)
C_a = T_a[-1] / bigO_line_a[-1]
C_b = T_b[-1] / bigO_line_b[-1]

bigO_line_a_scaled = [x * C_a for x in bigO_line_a]
bigO_line_b_scaled = [x * C_b for x in bigO_line_b]

plt.figure(figsize=(8, 5))
plt.plot(Ns_a, bigO_line_a_scaled, label='$O(N^2)$', color='red', ls='--', alpha=0.5)
plt.plot(Ns_a, T_a, label='$T_a$ (Classical)', color='red', marker='o')

plt.plot(Ns_a, bigO_line_b_scaled, label='$O(N^{\log_2{3}})$', color='blue', ls='--', alpha=0.5)
plt.plot(Ns_a, T_b, label='$T_b$ (Karatsuba)', color='blue', marker='s')

plt.xlabel('N')
plt.ylabel('s')
plt.legend()
plt.title('Comparison of Classical and Karatsuba Multiplication (Normalized)')
plt.grid(True, alpha=0.3)
plt.show()