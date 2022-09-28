import rsa
import sys

x = int(sys.argv[1])
n = int(sys.argv[2])
e = int(sys.argv[3])

print(rsa.rsa(x,n,e))
