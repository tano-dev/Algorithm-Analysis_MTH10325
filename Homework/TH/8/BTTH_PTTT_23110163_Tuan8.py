import time
import matplotlib.pyplot as plt

def find_k_char(n, k):
    L = [0] * (n + 1)
    L[0] = 3
    if n > 0:
        L[1] = 3
        for i in range(2, n + 1):
            L[i] = L[i-1] + L[i-2]

    def search(n_curr, k_curr):
        if n_curr == 0:
            return "abc"[k_curr - 1] 
        if n_curr == 1:
            return "def"[k_curr - 1]
            
        len_first_half = L[n_curr - 1]
        
        if k_curr <= len_first_half:
            return search(n_curr - 1, k_curr)
        else:
            return search(n_curr - 2, k_curr - len_first_half)

    return search(n, k)

n_values = list(range(1, 2001, 50)) # Từ 1 đến 2000 với bước 50 để tránh thời gian quá lâu
avg_times = []
num_trials = 100 

for n in n_values:
    total_time = 0
    k_test = 2 
    
    for _ in range(num_trials):
        start_time = time.perf_counter()
        find_k_char(n, k_test)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)
        
    avg_times.append(total_time / num_trials)

C = avg_times[-1] / n_values[-1]
bigO_line = [C * n for n in n_values]

# Vẽ đồ thị
plt.figure(figsize=(10, 6))
plt.plot(n_values, avg_times, marker='o', color='blue', label='find_kth_char()')
plt.plot(n_values, bigO_line, linestyle='--', color='red', label=r'$O(n)$')

plt.title('Average Time Complexity')
plt.xlabel('n')
plt.ylabel('s')
plt.legend()
plt.grid(True)
plt.show()