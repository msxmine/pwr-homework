from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def bxor(a,b):
    res = b""
    for x, y in zip(a,b):
        res += bytes([x^y])
    return res

def digest(msg):
    msglen = len(msg)
    fullblocks = msglen // 32
    rd = msglen - (fullblocks)*32
    if rd <= 16:
        msg += bytes(16-rd)
    else:
        msg += bytes((32-rd)+16)
    msg += msglen.to_bytes(16, byteorder="big")
    res = bytes([0xff]*32)
    for i in range(0,len(msg),16):
        blk = msg[i:i+16]
        aes = Cipher(algorithms.AES(blk), modes.ECB())
        enc = aes.encryptor()
        ct = enc.update(res) + enc.finalize()
        res = bxor(ct, res)
    return res
