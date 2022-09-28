from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import bigprimes
import json

desiredlengths = [ 128, 256, 512, 1024, 1536, 2048, 3072, 4096]

generated_keys = {}

def getManualKey(p, q):
    e = 65537
    n = p*q
    d = pow(e, -1, (p-1)*(q-1))

    pubn = rsa.RSAPublicNumbers(e, n)
    dmp1 = rsa.rsa_crt_dmp1(d, p)
    dmq1 = rsa.rsa_crt_dmq1(d, q)
    iqmp = rsa.rsa_crt_iqmp(p, q)
    return rsa.RSAPrivateNumbers(p,q,d,dmp1, dmq1, iqmp, pubn).private_key()


for dlen in desiredlengths:
    generated_keys[dlen] = []
    for kidx in range(1000):
        print(f"iteration {kidx} klen {dlen}")
        if dlen < 256:
            newkey = getManualKey(bigprimes.genPrime(dlen), bigprimes.genPrime(dlen))
        else:
            newkey = rsa.generate_private_key(65537, dlen*2)
        generated_keys[dlen].append(newkey.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()).decode("utf-8"))

with open("./allkeys.json", "w") as kfil:
    json.dump(generated_keys, kfil)



