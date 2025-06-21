import base64
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


iv = b"\x00"*16
key = b"YELLOW SUBMARINE"

data = base64.b64decode(open("10.txt", "r").read())
cbc = CBC(iv, key)
print(cbc.decrypt(data))
