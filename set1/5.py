def rxor(text, key):
    chunks = [x.encode() for x in text.splitlines()]
    key = key.encode()
    
    r = []
    t = []

    for chunk in chunks:
        for i in range(len(chunk)):
            t.append(key[i % len(key)] ^ chunk[i])

        r.append(bytes(t))
        t = []

    return r

key = "ICE"
code = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

result = rxor(code, key)

for i in result:
    print(i.hex())
