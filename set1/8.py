from Crypto.Cipher import AES

key = b"YELLOW SUBMARINE"

cipher = AES.new(key, AES.MODE_ECB)

data = [bytes.fromhex(x) for x in open("8.txt", "r").read().splitlines()]

for block in data:
    t = []
    size = len(block)//16
    for i in range(0, len(block), 16):
        t.append(block[i:i+16])
    
    if len(set(t)) != size:
        print(block.hex())
