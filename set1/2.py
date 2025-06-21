def xor(a,b):
    return bytes([x ^ y for x, y in zip(a,b)])

a = bytes.fromhex(input("> "))
b = bytes.fromhex(input("> "))
print(xor(a, b))
