# _summary_
# ==================================================
import sys
import os 
# ==================================================

def GCD(a: int, b: int) -> int:
    """Stein's algorithm"""
    if a == 0: return b
    if b == 0: return a

    if a % 2 == 0 and b % 2 == 0: 
        return 2 * GCD(a//2, b//2)
    elif a % 2 == 1 and b % 2 == 0: 
        return GCD(a, b//2)
    elif b % 2 == 1 and a % 2 == 0: 
        return GCD(a//2, b)
    else: 
        return GCD(abs(a - b), min(a, b))
    
def LCM(a: int, b: int) -> int:
    """LCM(a, b) = a * b // GCD(a, b)"""
    return a * b // GCD(a, b)

def N2nbase(N, n):
    """N to n-base"""
    if N < 0 or n < 2:
        raise ValueError("N and n must be positive integers greater than 1")
    elif N == 0:
        return [0]
    elif n == 2:
        return bin(N)
    elif n == 8:
        return oct(N)
    elif n == 16:
        return hex(N)
    res = ''
    while N > 0:
        if (tmp := N % n) > 9:
            res += chr(tmp + 87) # 97 = ord('a'), tmp = 10 = a
        else:
            res += str(tmp)
        N //= n
    return res[::-1]

def auto_fname(name, ext):
    """Generate a filename with a unique number at the end"""
    i = 1

# ==================================================

def main():
    pass
    
# ==================================================
from time import perf_counter
if __name__ == '__main__':
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print('\ntime :%.3f ms' %((end_time - start_time)*1000))