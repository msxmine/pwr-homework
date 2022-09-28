def rsa(x, n, e):
    return pow(x, e, n)

def rsarevcrt(x, p, q, dp, dq, qi):
    yp = pow(x, dp, p)
    yq = pow(x, dq, q)
    return (yq + ((yp-yq)*q)*qi)%(p*q)
