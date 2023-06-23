import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


key = b"YELLOW SUBMARINE"

with open("7.txt", "r") as f:
    ctx = base64.b64decode(str(f.read()))

cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(ctx) + decryptor.finalize()

print(decrypted_data.decode())
