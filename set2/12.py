import base64
from os import urandom
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

key = urandom(16)

def padding(ctx):
    padding_length = 16 - (len(ctx)%16)
    if padding_length == 0:
        padding_length = 16
    padding = bytes([padding_length]) * padding_length
    return ctx + padding

def encryption_oracle(ctx):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padding(bytes(ctx)+base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"))) + encryptor.finalize()

def find_block_size():
    current_cipher = None
    for i in range(2, 20):
        previous_cipher = current_cipher or encryption_oracle(b"a"*1)
        current_cipher = encryption_oracle(b"a"*i)
        if previous_cipher[:4] == current_cipher[:4]:
            return i - 1

def find_payload_length():
    previous_length = len(encryption_oracle(b''))
    for i in range(20):
        length = len(encryption_oracle(b'X'*i))
        if length != previous_length:
            return previous_length - i

def recover_byte(ctx, block_size):
    k = len(ctx)
    padding_length = (-k-1) % block_size
    padding = b"A" * padding_length

    target_block_number = len(ctx) // block_size
    target_slice = slice(target_block_number * block_size, (target_block_number+1)*block_size)
    target_block = encryption_oracle(padding)[target_slice]

    for i in range(256):
        message = padding + ctx + bytes([i])
        block = encryption_oracle(message)[target_slice]
        if block == target_block:
            return bytes([i])

def recover(block_size):
    ctx = b""
    payload_length = find_payload_length()
    for _ in range(payload_length):
        new_byte = recover_byte(ctx, block_size)
        ctx += new_byte

print(recover(find_block_size()).decode())
