# 1
import time
import numpy as np
import matplotlib.pyplot as plt

def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot_val = arr[len(arr) // 2][0]
    left = [x for x in arr if x[0] < pivot_val]
    middle = [x for x in arr if x[0] == pivot_val]
    right = [x for x in arr if x[0] > pivot_val]

    return quick_sort(left) + middle + quick_sort(right)
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)
def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    
    return result
def algorithm(N, A, x, method = 1):
    # Bước 1: Ghép mỗi giá trị với vị trí ban đầu của nó
    A_with_indices = [(A[i], i) for i in range(N)]
    
    # Bước 2: Dùng hàm quick sort tự viết để sắp xếp
    if method == 1:
        sorted_A = quick_sort(A_with_indices)
    else:
        sorted_A = merge_sort(A_with_indices)

    # Bước 3: Thuật toán 2 con trỏ
    left, right = 0, N - 1
    
    while left < right:
        # Lấy giá trị hiện tại của 2 con trỏ (chú ý thêm [0])
        current_sum = sorted_A[left][0] + sorted_A[right][0]
        
        if current_sum == x:
            # Trả về vị trí gốc (nằm ở vị trí [1] của tuple)
            return (sorted_A[left][1], sorted_A[right][1])
        elif current_sum < x:
            left += 1
        else:
            right -= 1

    return None


def measure_time_numpy(N, x, num_trials=100, method=1):
    total_time = 0
    for _ in range(num_trials):
        # Tạo mảng numpy ngẫu nhiên gồm các phần tử khác nhau đôi một (replace=False)
        A = np.random.choice(np.arange(1, 10001), size=N, replace=False)
        
        start_time = time.perf_counter()
        algorithm(N, A, x, method=method)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)
        
    return total_time / num_trials

def test():
    x = 50
    N = np.arange(10, 1001, 10)
    
    plt.figure(figsize=(10, 6))
    colors = {1: 'blue', 2: 'green'}
    labels = {1: 'Quick Sort', 2: 'Merge Sort'}
    
    # Tính đường lý thuyết 1 lần để làm mốc
    # (Dùng một lần chạy nháp để lấy hằng số c tỷ lệ)
    plot_time = [measure_time_numpy(n, x, num_trials=5, method=1) for n in N]
    c = plot_time[-1] / (N[-1] * np.log(N[-1]))
    nlogn_time = c * N * np.log(N)
    plt.plot(N, nlogn_time, linestyle='--', color='red', label=r'Lý thuyết $O(N \log N)$')

    for method in [1, 2]:
        empirical_times = []
        print(f"\nRunning {labels[method]}")
        for n in N:
            avg_time = measure_time_numpy(n, x, num_trials=100, method=method)
            empirical_times.append(avg_time)
            # print(f"N: {n}, Average Time: {avg_time:.8f} seconds")
            
        plt.plot(N, empirical_times, marker='o', markersize=3, 
                 color=colors[method], label=f'Thực nghiệm ({labels[method]})')

    plt.title('Quick Sort & Merge Sort vs O(N log N)')
    plt.xlabel('N')
    plt.ylabel('time (s)')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.show()
test()