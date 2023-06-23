import base64
from Crypto.Cipher import AES

key = b"YELLOW SUBMARINE"

with open("7.txt", "r") as f:
    ctx = base64.b64decode(str(f.read()))

cipher = AES.new(key, AES.MODE_ECB)

print(cipher.decrypt(ctx).decode())
