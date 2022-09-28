def encrypt(x, n, e):
    return pow(x, e, n)

def decryptcrt(x, p, q, dp, dq, qi):
    yp = pow(x, dp, p)
    yq = pow(x, dq, q)
    return (yq + q*((qi*(yp-yq))%p))%(p*q)

def decrypt(x, n, d):
    return pow(x,d,n)

