def xor(a,b):
    return bytes([_a ^ _b for _a, _b in zip(a,b)])
print(xor(bytes.fromhex("1c0111001f010100061a024b53535009181c"), bytes.fromhex("686974207468652062756c6c277320657965")).hex())
