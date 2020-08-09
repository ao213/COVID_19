def fibo(n):
    result = []
    a = 1
    b = 1

    while b < n:
        result.append(b)
        val = a + b
        b = a 
        a = val
    return result

if __name__ == "__main__":
    print("{0}".format(fibo(100)))