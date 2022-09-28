import rsa
import sys

x = int(sys.argv[1])
p = int(sys.argv[2])
q = int(sys.argv[3])
dp = int(sys.argv[4])
dq = int(sys.argv[5])
qi = int(sys.argv[6])

print(rsa.rsarevcrt(x,p,q,dp,dq,qi))

