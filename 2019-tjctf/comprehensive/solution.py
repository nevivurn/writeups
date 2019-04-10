#!/usr/bin/env python3

lst = [225, 228, 219, 223, 220, 231, 205, 217, 224, 231, 228, 210, 208, 227, 220, 234, 236, 222, 232, 235, 227, 217, 223, 234, 2613]

total = lst[-1]
lst = lst[:-1]
known = 'tjctf{'

key = [0]*8

# Subtract k[0] from all elements
key[0] = lst[0] - ord('t')
lst = [i-key[0] for i in lst]

# Extract key bytes from known plaintext
for i in range(len(known)):
        key[i] = lst[i*3] ^ ord(known[i]) ^ key[0]
key[-1] = lst[-1] ^ ord('}') ^ key[2]

def dexor(lst, key):
    lst = lst.copy()
    for a in range(8):
        for b in range(3):
            lst[a*3 + b] ^= key[a] ^ key[b]
    return lst

# Brute-force the last byte
for i in range(26):
    key[6] = i + ord('a')
    msg = dexor(lst, key)
    if sum(msg) == total:
        break

msg = [msg[a + b*3] for a in range(3) for b in range(8)]
print('key:', bytes(key).decode())
print('msg:', bytes(msg).decode())
