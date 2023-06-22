def xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

ctx = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = b"ICE"

print(xor(ctx, key*(len(ctx)//len(key) + 1)).hex())
