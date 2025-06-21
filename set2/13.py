import os
import random
from Crypto.Cipher import AES

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB)

def pkcs(s):
    t = 16 - len(s)%16
    if t == 0:
        t = 16
    return s + bytes([t]*t)

def parser(s):
    data = s.split("&")

    r = {}

    for block in data:
        t = block.split("=")
        r[t[0]] = t[1]

    return r

def profile_for(email):
    email = email.decode()
    email.replace("&", "")
    email.replace("=", "")
    r = pkcs(f"email={email}&uid=10&role=user".encode())

    return cipher.encrypt(r)


def decrypt(ciphertext):
    return parser(cipher.decrypt(ciphertext).decode())

target_email = b"e"*29
first_cipher = profile_for(target_email)

fab_email = b"a"*26 + pkcs(b"admin")
second_cipher = profile_for(fab_email)
r = first_cipher[:-16] + second_cipher[32:48]


print(decrypt(r))
