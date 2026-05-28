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
def find_kth_char(n, k):
    # Bước 1: Khởi tạo mảng độ dài các chuỗi từ f_0 đến f_n
    L = [0] * (n + 1)
    L[0] = 3
    if n > 0:
        L[1] = 3
        for i in range(2, n + 1):
            L[i] = L[i-1] + L[i-2]
            
    # Kiểm tra k có hợp lệ không (tùy chọn)
    if k < 1 or k > L[n]:
        return "k nằm ngoài phạm vi chiều dài của chuỗi!"

    # Bước 2: Đệ quy tìm kiếm (không tạo chuỗi mới)
    def search(n_curr, k_curr):
        # Base cases
        if n_curr == 0:
            return "abc"[k_curr - 1] # -1 vì index trong Python bắt đầu từ 0
        if n_curr == 1:
            return "def"[k_curr - 1]
            
        # Chiều dài của nửa đầu tiên (tức là f_{n-1})
        len_first_half = L[n_curr - 1]
        
        # Quyết định rẽ nhánh
        if k_curr <= len_first_half:
            return search(n_curr - 1, k_curr)
        else:
            return search(n_curr - 2, k_curr - len_first_half)

    return search(n, k)

# Test thử nghiệm
n = 4
k = 2
print(f"Ký tự thứ {k} của chuỗi f_{n} là '{find_kth_char(n, k)}'")

# Thử với n rất lớn (Code cũ của bạn sẽ bị treo, code này chạy chớp mắt)
print(f"Ký tự thứ 100 của chuỗi f_50 là '{find_kth_char(50, 100)}'")