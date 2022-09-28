import rsa
import sys
import json
import base64

if len(sys.argv) < 3:
    print("second argument must be keyfile")
    sys.exit(1)

keyfile = open(sys.argv[2], "r")
keyjson = json.load(keyfile)

p = int.from_bytes(base64.urlsafe_b64decode(keyjson["p"] + "==="), byteorder="big", signed=False)
q = int.from_bytes(base64.urlsafe_b64decode(keyjson["q"] + "==="), byteorder="big", signed=False)
dp = int.from_bytes(base64.urlsafe_b64decode(keyjson["dp"] + "==="), byteorder="big", signed=False)
dq = int.from_bytes(base64.urlsafe_b64decode(keyjson["dq"] + "==="), byteorder="big", signed=False)
qi = int.from_bytes(base64.urlsafe_b64decode(keyjson["qi"] + "==="), byteorder="big", signed=False)
x = int(sys.argv[1])

print(rsa.rsarevcrt(x,p,q,dp,dq,qi))

keyfile.close()
