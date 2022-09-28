import hashlib
import aeshash

name = "Tested".encode("utf-8")
myalgos = ["md4", "md5", "sha1", "sha256", "sha512", "blake2s", "blake2b"]
goodalgos = [al for al in myalgos if al in hashlib.algorithms_available]

print("aes_hash", aeshash.digest(name).hex())

for algo in goodalgos:
    h = hashlib.new(algo)
    h.update(name)
    if "shake" in h.name:
        print(algo, h.hexdigest(length=32))
    else:
        print(algo, h.hexdigest())


