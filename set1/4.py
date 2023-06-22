with open("4.txt", "r") as f:
    strings = f.read().splitlines()

def xor(a,b):
    return bytes([_a ^ _b for _a, _b in zip(a,b)])

ascii_list = [32] + list(range(97, 122))

class error(Exception):
    pass

def attack_xor(ctx):
    best = {"nb_letters": 0}
    for i in range(2**8):
        key = i.to_bytes(1, byteorder='big')
        msg = xor(ctx, key*len(ctx))
        nb_letters = sum([x in ascii_list for x in msg])
        if nb_letters > best['nb_letters']:
            best = {"message": msg, "nb_letters": nb_letters}
    if best['nb_letters'] > 0.7*len(msg):
        return best
    else:
        raise error(best['message'])


results = []
for i in strings:
    try:
        msg = attack_xor(bytes.fromhex(i))['message']
    except Exception:
        pass
    else:
        results.append(msg)

if len(results) > 1:
    print("Error")
else:
    print(results[0].decode())
