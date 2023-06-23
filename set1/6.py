import base64

with open("6.txt", "r") as f:
    ctx = base64.b64decode(str(f.read()))

ascii_list = [32] + list(range(97,122))

def xor(a, b):
    return bytes(_a ^ _b for _a, _b in zip(a,b))

def distance(a, b):
    count = 0
    for _a, _b in zip(a, b):
        count+=bin(int(_a ^_b)).count("1")
    return count

def attack_xor(ctx):
    best = None
    for i in range(2**8):
        key = i.to_bytes(1, byteorder='big')
        keystream = key*len(ctx)
        msg = xor(ctx, keystream)
        nb_letters = sum([x in ascii_list for x in msg])
        if best == None or nb_letters > best['nb_letters']:
            best = {"key": key, "nb_letters": nb_letters}

    return best

def letter_ratio(ctx):
    nb_letters = sum([x in ascii_list for x in ctx])
    return nb_letters / len(ctx)

def is_text(ctx):
    r = letter_ratio(ctx)
    return True if r>0.7 else False

keysizes = range(2, 41)
score = distance(ctx[:keysizes[0]], ctx[keysizes[0]: 2*keysizes[0]+1]) // keysizes[0]
keysize = [(score, keysizes[0])]
for i in range(1, 39):
    current_score = (distance(ctx[:keysizes[i]], ctx[keysizes[i]:(2*keysizes[i])]) + distance(ctx[(2*keysizes[i]):(3*keysizes[i])], ctx[(3*keysizes[i]):(4*keysizes[i])])) // 2 // keysizes[i]
    keysize.append((current_score, keysizes[i]))

keysize = sorted(keysize)
index = 0
for i in range(1,len(keysize)):
    if keysize[0][0] == keysize[i][0]:
        continue
    else:
        index = i
        break

keysize = keysize[:index]

for score, key in keysize:
    ctx_blocks = []
    for i in range(0, len(ctx), key):
        ctx_blocks.append(ctx[i:(i+key)])

    transposed_ctx_blocks = []
    for i in range(key):
        block = []
        for j in range(len(ctx_blocks)):
            block.append(ctx_blocks[j][i:i+1].decode())
        transposed_ctx_blocks.append(bytes("".join(block), "utf-8"))

    score = []
    for i in range(key):
        score.append(attack_xor(transposed_ctx_blocks[i]))

    key_parts = []
    for i in score:
        key_parts.append(i['key'].decode())

    key = "".join(key_parts)
    if is_text(xor(ctx, bytes(key, "utf-8")*(len(ctx)//len(key) + 1))):
        print(key)
        print(xor(ctx, bytes(key, "utf-8")*(len(ctx)//len(key) + 1)).decode())
