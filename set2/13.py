import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom
from math import ceil

key = urandom(16)

### ORACLE ###
def parser(ctx):
    parsed_ctx = {}
    for item in ctx.split("&"):
        parsed_ctx[item.split("=")[0]] = item.split("=")[1]

    return parsed_ctx

def padding(ctx):
    padding_length = 16 - (len(ctx) % 16)
    if padding_length == 0:
        return ctx + bytes([padding_length])*16
    else:
        return ctx + bytes([padding_length])*padding_length

def profile_for(email):
    if b"&" in email or b"=" in email:
        print("Invalid email format")
    else:
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(padding(bytes(f"email={email.decode()}&uid=10&role=user", "utf-8"))) + encryptor.finalize()

def decrypt(ctx):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ctx) + decryptor.finalize()

### ATTACK ###
def split_bytes(ctx):
    blocks = ceil(len(ctx)/16)
    return [ctx[16*i:16*(i+1)] for i in range(blocks)]

target_email = b"eeeeeeeeeeeeeeee@attacker.com"
first_cipher = profile_for(target_email)

fab_email = b"nextBlockShouldSt@rt.Here:" + padding(b"admin")
second_cipher = profile_for(fab_email)
cut = second_cipher[32:48]
new_cipher = first_cipher[:-16] + cut

print(parser(decrypt(new_cipher).decode()))

