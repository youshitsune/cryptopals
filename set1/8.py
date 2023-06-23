with open("8.txt", "rb") as f:
    ctx = f.read().splitlines()

for i in ctx:
    num_blocks = len(i) // 16
    blocks = [i[x*16:(x+1)*16] for x in range(num_blocks)]
    if len(set(blocks)) != num_blocks:
        print(i)
