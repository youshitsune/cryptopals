def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def score(s):
    for i in s:
        if i not in list("ABCDEFGHIJKLOMNPQRSTUVWXYZabcdefghijklomnpqrstuvwxyz1234567890'\"-.,;!?\n "):
            return False

    return True

codes = [bytes.fromhex(x) for x in open("4.txt", "r").read().splitlines()]
for a in codes:
    for i in range(256):
        try:
            x = xor(a, [i]*len(a)).decode()
        except Exception:
            pass
        else:
            if score(x):
                print(x)
