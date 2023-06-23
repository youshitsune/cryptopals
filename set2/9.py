cipher = input("Text: ")
key = input("Key: ")

while True:
    if len(bytes(cipher, "utf-8")) % len(bytes(key, "utf-8")) == 0:
        break
    else:
        key+="\x04"

print(bytes(key, "utf-8"))
