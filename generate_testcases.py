import copy
from random import randint 
import sys
import math
import numpy as np

x,y = 0,1

def gcdExtended(a, b):
    global x, y
 
    # Base Case
    if (a == 0):
        x = 0
        y = 1
        return b
 
    # To store results of recursive call
    gcd = gcdExtended(b % a, a)
    x1 = x
    y1 = y
 
    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1
 
    return gcd
 
 
def modInverse(A, M):
    g = gcdExtended(A, M)
    res = (x % M + M) % M
    return res
    # print("Modular multiplicative inverse is ", res)

"""
    a, m <= 2^31 - 1
    a,m are coprime
    find x, 0<x<m such that ax = 1 mod m
"""
def create_q2_testcases():
    for num in range(1, 101):
        m = randint(1, (1 << 31) - 1)
        a = randint(1, m - 1)

        while math.gcd(a, m) != 1:
            a = randint(1, m - 1)

        with open(f"testcases/Q2/input/{num}", "w+") as f:
            f.write(f"{a}\n")
            f.write(f"{m}\n")

        # x = modInverse(a, m)

        # print(a, x, m, (a*x) % m)

        # with open(f"testcases/Q2/output/{num}", "w+") as f:
        #     f.write(f"{x}\n")


"""
 Upto 10000 elements, where each element <= 10000
"""
def create_q3_testcases():
    n = 10000
    arr = [randint(1, 10000) for _ in range(n)]
    brr = copy.deepcopy(arr)
    brr.sort()

    with open(f"testcases/Q3/input/1", "w+") as f:
        f.write(f"{n}\n")
        for i in range(n):
            f.write(f"{arr[i]}\n")

    n = 10
    arr = [randint(1, 10000) for _ in range(n)]
    brr = copy.deepcopy(arr)
    brr.sort()

    with open(f"testcases/Q3/input/2", "w+") as f:
        f.write(f"{n}\n")
        for i in range(n):
            f.write(f"{arr[i]}\n")
                
    for num in range(3, 101):
        n = num * 25
        arr = [randint(1, 10000) for _ in range(n)]
        brr = copy.deepcopy(arr)
        brr.sort()

        with open(f"testcases/Q3/input/{num}", "w+") as f:
            f.write(f"{n}\n")
            for i in range(n):
                f.write(f"{arr[i]}\n")


def get_testcase(num, size_max):
    n, m, p = randint(size_max // 2, size_max), randint(size_max // 2, size_max), randint(size_max // 2, size_max)
    A = [[randint(1, 1000) for _ in range(m)] for _ in range(n)]
    B = [[randint(1, 1000) for _ in range(p)] for _ in range(m)]

    with open(f"testcases/Q4/input/{num}", "w+") as f:
        f.write(f"{n}\n")
        f.write(f"{m}\n")
        f.write(f"{m}\n")
        f.write(f"{p}\n")

        for i in range(n):
            for j in range(m):
                f.write(f"{A[i][j]}\n")

        for i in range(m):
            for j in range(p):
                f.write(f"{B[i][j]}\n")

    a = np.array(A)
    b = np.array(B)
    c = np.matmul(a, b)
    
    with open(f"testcases/Q4/output/{num}", "w+") as f:
        f.write("100\n")
        for i in range(n):
            for j in range(p):
                f.write(f"{c[i, j]}\n")


def create_q4_testcase():
    for num in range(1, 91):
        get_testcase(num, 50)

    for num in range(91, 101):
        get_testcase(num, 200)


"""
    a, m <= 2^63 - 1
    a,m are coprime
    find x, 0<x<m such that ax = 1 mod m
"""
def create_q5_testcases():
    for num in range(1, 401):
        m = randint(1, (1 << 63) - 1)
        a = randint(1, m - 1)

        while math.gcd(a, m) != 1:
            a = randint(1, m - 1)

        with open(f"testcases/Q2/bonus/input/{num}", "w+") as f:
            f.write(f"{a}\n")
            f.write(f"{m}\n")

        # x = modInverse(a, m)

        # print(a, x, m, (a*x) % m)

        # with open(f"testcases/Q2/output/{num}", "w+") as f:
        #     f.write(f"{x}\n")
        
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate_testcases.py <Question-no>")
        sys.exit(1)

    question_no = int(sys.argv[1])

    if question_no == 2:
        create_q2_testcases()
    elif question_no == 3:
        create_q3_testcases()
    elif question_no == 4:
        create_q4_testcase()
    elif question_no == 5:
        create_q5_testcases()


if __name__ == "__main__":
    main()