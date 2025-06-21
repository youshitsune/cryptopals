def pkcs(s, size):
    t = size - len(s)
    return s + bytes([t]*t)

print(pkcs(b"YELLOW SUBMARINE", 20))
