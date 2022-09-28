from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
import struct

#32bit block counter + 96bit nounce
nonce = struct.pack("<i", 0) + bytes(12)
key = 'tested'.encode().ljust(32, b'\0')[:32]

#RFC 7539
algorithm = algorithms.ChaCha20(key, nonce)
cipher = Cipher(algorithm, mode=None)
encryptor = cipher.encryptor()

output = bytes(0)
output += encryptor.update(bytes(128))
print(output.hex())
outfile = open("./bytes", "wb")
outfile.write(output)
outfile.close()

