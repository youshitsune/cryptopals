import os
import base64
from Crypto.Cipher import AES

key = os.urandom(16)

def pkcs(s):
    t = 16 - len(s)%16
    if t == 0:
        t = 16
    return s + bytes([t]*t)

def oracle(x):
    t = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
    x += t

    x = pkcs(x)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(x)

def check_ecb(blocksize):
    r = oracle(b"a"*blocksize*4)

    size = len(r)//blocksize
    t = [r[i:i+blocksize] for i in range(0, len(r), blocksize)]

    if len(set(t)) != size:
        return True
    else:
        return False

def checktext(s):
    for i in s:
        if i not in list("ABCDEFGHIJKLOMNPQRSTUVWXYZabcdefghijklomnpqrstuvwxyz1234567890'\"-.,:;!?\n "):
            return False
    return True


def attacker():
    blocksize = 0
    for i in range(1, 2**8):
        r = oracle(b"a"*i*2)
        if r[0:i] == r[i:i*2]:
           blocksize = i
           break

    blocksize *= 16

    if not check_ecb(blocksize):
        return

    t = {}
    r = b""
    for j in range(1, blocksize):
        for i in range(2**8):
            t[oracle(b"a"*(blocksize-j)+r+bytes([i]))[:blocksize]] = b"a"*(blocksize-j)+r+bytes([i])
        tmp = bytes([t[oracle(b"a"*(blocksize-j))[:blocksize]][-1]])
        if not checktext(tmp.decode()):
            break
        r += bytes([t[oracle(b"a"*(blocksize-j))[:blocksize]][-1]])
        t = {}
    print(r.decode())

attacker()
