import base64

a = bytes.fromhex(input("> "))
print(base64.b64encode(a))
