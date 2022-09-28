import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends.openssl import backend as ossl
import myrsa
import time
import random

ossl._rsa_skip_check_key = True

keys = {}

with open("./allkeys.json", "r") as jsf:
    data = json.load(jsf)
    print("Loading keys")
    for plen in data:
        keys[int(plen)] = []
        for kidx, kstr in enumerate(data[plen]):
            # if kidx > 9:
            #     break
            keys[int(plen)].append(ossl.load_pem_private_key(kstr.encode("utf-8"), password=None))
    print("Keys loaded")

# akey: rsa.RSAPrivateNumbers = keys[2048][0].private_numbers()
# amsg = "Hello!"
# testmsg = int.from_bytes(amsg.encode("utf-8"), byteorder="little")
# enctest = myrsa.encrypt(testmsg, akey.public_numbers.n, akey.public_numbers.e)
# print(enctest)
# # dectest = myrsa.decrypt(enctest, akey.public_numbers.n, akey.d)
# dectest = myrsa.decryptcrt(enctest, akey.p, akey.q, akey.dmp1, akey.dmq1, akey.iqmp)
# dectestmsg = dectest.to_bytes((dectest.bit_length() + 7)//8, "little").decode("utf-8")
# print(dectestmsg)

exectimes = {}

for klen in keys:
    print(f"testing length {klen}")
    numofkeys = len(keys[klen])
    lenclsavg = 0.0
    lencrtavg = 0.0
    for key in keys[klen]:
        priv : rsa.RSAPrivateNumbers = key.private_numbers()
        pub : rsa.RSAPublicNumbers = priv.public_numbers
        todecrypt = random.randrange(2, pub.n)
        start = time.process_time()
        myrsa.decrypt(todecrypt, pub.n, priv.d)
        classictime = time.process_time() - start
        start = time.process_time()
        myrsa.decryptcrt(todecrypt, priv.p, priv.q, priv.dmp1, priv.dmq1, priv.iqmp)
        crttime = time.process_time() - start
        lenclsavg += (classictime/numofkeys)
        lencrtavg += (crttime/numofkeys)
    exectimes[klen] = {"cls": lenclsavg, "crt": lencrtavg}

with open("./times.json", "w") as resfil:
    json.dump(exectimes, resfil)


