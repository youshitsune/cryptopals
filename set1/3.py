def xor(a, x):
    r = ""
    for i in range(len(a)):
        r += hex(a[i] ^ x)[2:]

    return r

def score(s):
    for i in s:
        if i not in list("ABCDEFGHIJKLOMNPQRSTUVXYZabcdefghijklomnpqrstuvxyz'\"-.,; "):
            return False

    return True

a = bytes.fromhex(input("> "))

for i in range(1, 256):
    try:
        x = bytes.fromhex(xor(a, i)).decode()
    except Exception:
        pass
    else:
        if score(x): 
            print(bytes.fromhex(xor(a, i)))
