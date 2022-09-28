from Cryptodome.Hash import SHA256
from Cryptodome.Random import random, get_random_bytes
from Cryptodome.Cipher import AES
import base64
import sys

p = int(0xDEADBEEF)

def f(password: str):
    passbytes = password.encode("utf-8")
    hasher = SHA256.new()
    hasher.update(passbytes)
    reshash = hasher.digest()
    return int.from_bytes(reshash, byteorder="big")

def Hash(num: int):
    inbyt = num.to_bytes(280, byteorder="big")
    hasher = SHA256.new()
    hasher.update(inbyt)
    reshash = hasher.digest()
    return reshash

def Enc(key: bytes, data: bytes):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(data)
    return cipher.iv + ct_bytes

def Dec(key: bytes, data: bytes):
    iv = data[0:16]
    ct = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return cipher.decrypt(ct)


def keyDh(name: str, partner: str):
    pi = input("Password > ")
    xa = random.randrange(0, p)
    Xa = pow(f(pi), xa, p)
    print(f"X{name} <", base64.b64encode(  Xa.to_bytes(  (Xa.bit_length() + 7)//8  ,byteorder="big")  ).decode("utf-8"))
    Xb = int.from_bytes(base64.b64decode(input(f"X{partner} > ").encode("utf-8")), byteorder="big")
    K = Hash(pow(Xb, xa, p))
    return K


def vera(key: bytes):
    Ca = get_random_bytes(16)
    E1 = Enc(key, Ca)
    print("E1 <", base64.b64encode(E1).decode("utf-8"))
    E2 = base64.b64decode(input("E2 > ").encode("utf-8"))
    E2d = Dec(key, E2)
    if not (E2d.endswith(Ca) and len(E2d) == 32):
        print("FAIL")
        return False
    Cb = E2d[0:16]
    E3 = Enc(key, Cb)
    print("E3 <", base64.b64encode(E3).decode("utf-8"))
    print("PASS")
    return True

def verb(key: bytes):
    E1 = base64.b64decode(input("E1 > ").encode("utf-8"))
    Ca = Dec(key, E1)
    Cb = get_random_bytes(16)
    E2 = Enc(key, Cb+Ca)
    print("E2 <", base64.b64encode(E2).decode("utf-8"))
    E3 = base64.b64decode(input("E3 > ").encode("utf-8"))
    E3d = Dec(key, E3)
    if E3d == Cb:
        print("PASS")
        return True
    else:
        print("FAIL")
        return False


if sys.argv[1] in ["A", "a", "Alice"]:
    kl = keyDh("A", "B")
    suc = vera(kl)
    if suc:
        print("K ==", base64.b64encode(kl).decode("utf-8"))
else:
    kl = keyDh("B", "A")
    suc = verb(kl)
    if suc:
        print("K ==", base64.b64encode(kl).decode("utf-8"))
