string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def xor(a,b):
    return bytes([_a ^ _b for (_a, _b) in zip(a,b)])

ascii_list = [32] + list(range(97,122))

def attack_xor(ctx):
    best = None
    for i in range(2**8):
        key = i.to_bytes(1, byteorder='big')
        keystream = key*len(ctx)
        msg = xor(ctx,keystream)
        nb_letters = sum([x in ascii_list for x in msg])
        if best == None or nb_letters > best['nb_letters']:
            best = {"message": msg, "nb_letters": nb_letters}

    return best

result = attack_xor(bytes.fromhex(string))

print(result['message'].decode())

