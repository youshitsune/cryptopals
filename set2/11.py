import os
import random
from Crypto.Cipher import AES

class CBC:
    def __init__(self, iv, key):
        self.iv = iv
        self.aes = AES.new(key, AES.MODE_ECB)
    
    def xor(self, a, b):
        return bytes([x ^ y for x, y in zip(a, b)])

    def decrypt(self, ciphertext):
        text = [self.xor(self.iv, self.aes.decrypt(ciphertext[0:16]))]

        for i in range(16, len(ciphertext), 16):
            text.append(self.xor(ciphertext[i-16:i], self.aes.decrypt(ciphertext[i:i+16])))

        return b"".join(text).decode()

    def encrypt(self, text):
        ciphertext = [self.aes.encrypt(self.xor(self.iv, text[0:16]))]

        for i in range(16, len(text), 16):
            ciphertext.append(self.aes.encrypt(self.xor(ciphertext[-1], text[i:i+16])))

        return b"".join(ciphertext)

def rand16():
    return os.urandom(16)

def pkcs(s):
    t = 16 - (len(s)%16)
    if t == 0:
        t = 16
    return s + bytes([t]*t)

def encryption_oracle(x):
    nb = random.randint(5, 10)
    x = os.urandom(nb) + x + os.urandom(nb)

    x = pkcs(x)

    rn = random.randint(0, 1)

    if rn == 0:
        cbc = CBC(rand16(), rand16())
        print("CBC")
        return cbc.encrypt(x)
    else:
        cipher = AES.new(rand16(), AES.MODE_ECB)
        print("ECB")
        return cipher.encrypt(x)


def detector():
    r = encryption_oracle(b"a"*64)

    size = len(r)//16
    t = [r[i:i+16] for i in range(0, len(r), 16)]

    if len(set(t)) != size:
        return "ECB"
    else:
        return "CBC"

print(detector())
