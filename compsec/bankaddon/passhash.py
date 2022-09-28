import hashlib
import os

def hash_password(password):
    saltbytes = os.urandom(16)
    passbytes = password.encode("utf-8")
    reshash = hashlib.scrypt(passbytes, salt=saltbytes, n=(2**14), r=8, p=8)
    passstring = reshash.hex() + ":" + saltbytes.hex()
    return passstring

def check_password_hash(hashstr, password):
    hscomponents = hashstr.split(":")
    saltbytes = bytes.fromhex(hscomponents[1])
    passbytes = password.encode("utf-8")
    reshash = hashlib.scrypt(passbytes, salt=saltbytes, n=(2**14), r=8, p=8)
    return reshash == bytes.fromhex(hscomponents[0])
