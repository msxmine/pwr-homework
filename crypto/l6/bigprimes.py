import random

def genCandidate(bits):
    num = 2**(bits-1)
    num += (random.getrandbits(bits-2)*2)
    num += 1
    return num

def fprimetest(num):
    for i in range(2,550):
        if num%i == 0:
            return False
    return True

def sprimetest(n, iter=200):
    d = n-1
    s = 0
    while d%2 == 0:
        d = d//2
        s += 1
    
    for i in range(iter):
        a = random.randrange(2,n-1)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        testgood = False
        for pwr in range(1, s):
            x = pow(x, 2, n)
            if x == n-1:
                testgood = True
                break
        if testgood:
            continue
        return False
    return True


def genPrime(bits):
    while True:
        pc = genCandidate(bits)
        if fprimetest(pc) == False:
            continue
        if sprimetest(pc) == False:
            continue
        if (pc-1)%65537 == 0:
            continue
        return pc


