import base64
from Crypto.Cipher import AES

key = b"YELLOW SUBMARINE"

cipher = AES.new(key, AES.MODE_ECB)

data = base64.b64decode(open("7.txt", "r").read())
print(cipher.decrypt(data).decode())
