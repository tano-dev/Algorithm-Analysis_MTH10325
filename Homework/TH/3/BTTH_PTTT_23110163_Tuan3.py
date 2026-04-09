import math
import numpy as np
import warnings

# # Bỏ qua các cảnh báo toán học của numpy để output gọn gàng
# warnings.simplefilter('ignore', np.RankWarning)

def estimate_complexity(f, a, b):
    n_vals = []
    fn_vals = []
    log_n = []
    log_fn = []
    
    # BƯỚC 1: Lấy dữ liệu và chuyển sang dạng Logarit
    for n in range(a, b + 1):
        try:
            val = f(n)
            abs_val = abs(val) # Xét trị tuyệt đối cho độ lớn của hàm
            
            if abs_val > 0:
                # Xử lý các số cực lớn (vd n^n) để tránh lỗi tràn bộ nhớ (Overflow)
                if isinstance(abs_val, int) and abs_val > 1e250:
                    l_fn = abs_val.bit_length() * math.log(2)
                else:
                    l_fn = math.log(abs_val)
                    
                n_vals.append(n)
                fn_vals.append(val)
                log_n.append(math.log(n))
                log_fn.append(l_fn)
        except Exception:
            pass

    if len(n_vals) < 2:
        print(" => Lỗi: Không đủ dữ liệu để tính toán.")
        return

    # Lọc đường bao trên (Upper Envelope) để tìm xu hướng thật sự
    # Kỹ thuật này giúp loại bỏ nhiễu khi hàm dao động lên xuống do cos(n)
    env_log_n, env_log_fn = [], []
    max_val = -float('inf')
    for ln, lfn in zip(log_n, log_fn):
        if lfn >= max_val:
            max_val = lfn
            env_log_n.append(ln)
            env_log_fn.append(lfn)

    # Chia đôi dữ liệu bao trên để kiểm tra xem hệ số góc có ổn định không
    # Nếu hệ số góc tăng vọt -> Hàm tăng phi đa thức (như hàm mũ n^n)
    mid = len(env_log_n) // 2
    if mid >= 2:
        slope1 = np.polyfit(env_log_n[:mid], env_log_fn[:mid], 1)[0]
        slope2 = np.polyfit(env_log_n[mid:], env_log_fn[mid:], 1)[0]
        if slope2 - slope1 > 0.5:
            print(" => Output: Không có dạng O(n^alpha) hiện thông báo.")
            print("-" * 60)
            return

    # Tính độ dốc trung bình của toàn bộ đường bao trên
    overall_slope = np.polyfit(env_log_n, env_log_fn, 1)[0]
    alpha = int(round(overall_slope))

    if alpha == 0:
        print(" => Output: Độ phức tạp O(1)")
    elif alpha == 1:
        print(" => Output: Độ phức tạp O(n)")
    else:
        print(f" => Output: Độ phức tạp O(n^{alpha})")

    # BƯỚC 2: Thế f(n) và n để giải hệ phương trình tìm a_0, a_1,..., a_alpha
    try:
        # np.polyfit(X, Y, deg) trả về hệ số đa thức theo thứ tự: [a_alpha, ..., a_1, a_0]
        coeffs = np.polyfit(n_vals, fn_vals, alpha)
        
        # Đảo ngược mảng để in đúng thứ tự yêu cầu của đề: a_0, a_1, ..., a_alpha
        coeffs_reversed = coeffs[::-1]
        
        # Làm tròn hệ số để hiển thị sạch sẽ (khử sai số dấu phẩy động 0.0000001)
        coeffs_rounded = [round(c, 4) for c in coeffs_reversed]
        
        print(" => Các hệ số [a_0, a_1, ..., a_alpha]:")
        str_coeffs = [f"a_{i} = {c}" for i, c in enumerate(coeffs_rounded)]
        print("    " + ", ".join(str_coeffs))
        
        # In ra dạng đa thức trực quan
        poly_terms = []
        for i, c in enumerate(coeffs_rounded):
            if c != 0:
                if i == 0: poly_terms.append(f"{c}")
                elif i == 1: poly_terms.append(f"{c}n")
                else: poly_terms.append(f"{c}n^{i}")
        
        poly_str = " + ".join(poly_terms).replace("+ -", "- ")
        print(f" => Hàm xấp xỉ: f(n) ≈ {poly_str}")
        print("-" * 60)
        
    except Exception as e:
        print(f" => Lỗi khi tính hệ số: {e}")
        print("-" * 60)

# ==========================================
# KIỂM TRA CÁC TRƯỜNG HỢP (TEST CASES)
# ==========================================
def func_a(n): return n**2
def func_b(n): return n**3 + math.cos(n) * (n**4)
def func_c(n): return n**n
def func_d(n): return n**3 + n**2 + n + 1

if __name__ == "__main__":
    a, b = 10, 1000
    print(f"--- KIỂM TRA VỚI n chạy từ {a} đến {b} ---\n")
    
    print("a) f(n) = n^2")
    estimate_complexity(func_a, a, b)
    
    print("b) f(n) = n^3 + cos(n).n^4")
    estimate_complexity(func_b, a, b)
    
    print("c) f(n) = n^n")
    estimate_complexity(func_c, a, b)
    
    print("d) f(n) = n^3 + n^2 + n + 1")
    estimate_complexity(func_d, a, b)