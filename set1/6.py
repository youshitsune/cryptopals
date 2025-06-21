import base64

def distance(a, b):
    count = 0
    for _a, _b in zip(a, b):
        count+=bin(int(_a ^_b)).count("1")
    return count

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def score(s):
    r = 0
    for i in s:
        if i in list("ABCDEFGHIJKLOMNPQRSTUVWXYZabcdefghijklomnpqrstuvwxyz1234567890'\"-.,:;!?\n "):
            r+=1
    return r

def checktext(s):
    for i in s:
        if i not in list("ABCDEFGHIJKLOMNPQRSTUVWXYZabcdefghijklomnpqrstuvwxyz1234567890'\"-.,:;!?\n "):
            return False
    return True


def sxor(a):
    scores = []
    for i in range(256):
        try:
            x = xor(a, [i]*len(a)).decode()
        except Exception:
            pass
        else:
            scores.append((score(x), i))

    return sorted(scores, reverse = True,  key = lambda y: y[0])[0][1]

def rxor(text, key):
    r = []

    for i in range(len(text)):
        r.append(key[i % len(key)] ^ text[i])

    return r

cipher = base64.b64decode(open("6.txt", "r").read())

values = []
for keysize in range(2, 41):
    dist = distance(cipher[0:keysize], cipher[keysize:2*keysize])/keysize
    dist2 = distance(cipher[2*keysize:3*keysize], cipher[3*keysize:4*keysize])/keysize
    values.append(((dist+dist2)/2, keysize))

values = sorted(values, key = lambda x: x[0])
for _, minkey in values:
    blocks = []
    for i in range(0, len(cipher), minkey):
        blocks.append(cipher[i:i+minkey])

    transposed = []
    for i in range(0, minkey):
        r = []
        for block in blocks:
            r.append(block[i:i+1])
        transposed.append(b"".join(r))
        r = []


    key = ""
    for i in transposed:
        key += chr(sxor(i))

    results = rxor(cipher, key.encode())

    r = ""
    for i in results:
        r += chr(i)

    if checktext(r):
        print("Key:", key)
        print(r)
        break
