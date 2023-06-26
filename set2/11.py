from os import urandom
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def padding(ctx):
    padding_length = 16 - (len(ctx)%16)
    if padding_length == 0:
        padding_length = 16
    padding = bytes([padding_length]) * padding_length
    return ctx + padding

def check_ecb(ctx):
    num_blocks = len(ctx) // 16
    blocks = [ctx[x*16:(x+1)*16] for x in range(num_blocks)] 
    if len(set(blocks)) != num_blocks:
        return True
    else:
        return False


def encryption_oracle(ctx):
    enc = random.choice(range(2))
    if enc == 0:
        nbytes = random.choice(range(5, 11))
        cipher = Cipher(algorithms.AES(urandom(16)), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(padding(urandom(nbytes)+bytes(ctx)+urandom(nbytes))) + encryptor.finalize()

    else:
        nbytes = random.choice(range(5, 11))
        cipher = Cipher(algorithms.AES(urandom(16)), modes.CBC(urandom(16)), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(padding(urandom(nbytes)+bytes(ctx)+urandom(nbytes))) + encryptor.finalize()

msg = b'a'*64
cipher = encryption_oracle(msg)
if check_ecb(cipher):
    print("ECB")
else:
    print("CBC")
