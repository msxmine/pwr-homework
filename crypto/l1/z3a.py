import rsa
import sys
import json
import base64

if len(sys.argv) < 3:
    print("second argument must be keyfile")
    sys.exit(1)

keyfile = open(sys.argv[2], "r")
keyjson = json.load(keyfile)

n = int.from_bytes(base64.urlsafe_b64decode(keyjson["n"] + "==="), byteorder="big", signed=False)
e = int.from_bytes(base64.urlsafe_b64decode(keyjson["e"] + "==="), byteorder="big", signed=False)
x = int(sys.argv[1])

print(rsa.rsa(x,n,e))

keyfile.close()
