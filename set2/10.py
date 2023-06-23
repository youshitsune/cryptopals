import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def xor(a, b):
    return bytes(_a ^ _b for _a, _b in zip(a, b))

def aes(ctx, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ctx) + decryptor.finalize()

key = b"YELLOW SUBMARINE"

with open("10.txt", "r") as f:
    ctx = base64.b64decode(str(f.read()))

cipher_blocks = []
for i in range(16, len(bytes(ctx))+1, 16):
    cipher_blocks.append(ctx[i-16:i])

cipher_blocks.reverse()
decrypted_blocks = []
for i in range(len(cipher_blocks)-1):

    decrypted_blocks.append(xor(aes(cipher_blocks[i], key), cipher_blocks[i+1]))

decrypted_blocks.append(xor(aes(cipher_blocks[len(cipher_blocks)-1], key), b"0"*16))

for i in range(len(decrypted_blocks)):
    decrypted_blocks[i] = decrypted_blocks[i].decode()   

print("".join(list(reversed(decrypted_blocks))))
