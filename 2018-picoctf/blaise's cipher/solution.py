#!/usr/bin/env python3

from itertools import cycle

charset = 'abcdefghijklmnopqrstuvwxyz'

def get_keylen(s, lo=2, hi=40):
    best = 0
    for cur in range(lo, hi+1):
        cnt = 0
        for a, b in zip(s, s[cur:]):
            if a == b: 
                cnt += 1
        cnt /= len(s)-cur
        if cnt > best:
            best, length = cnt, cur
    return length

freq = 'etaoinshrdlcumwfgypbvkjxqz'
def solve_caesar(s):
    best = 0
    for k in range(26):
        t = [(ord(c)-ord('a') - k)%26 + ord('a') for c in s]

        score = 0
        for c in t:
            score += len(freq) - freq.index(chr(c))

        if score > best:
            best, key = score, k
    return chr(key+ord('a'))

with open('text.txt') as f:
    orig = f.read()

text = [c for c in orig if c.lower() in charset]
keylen = get_keylen(text)

key = []
for pos in range(keylen):
    key.append(solve_caesar(text[pos::keylen]))

print('key:', ''.join(key))

plaintext = []
keystream = cycle(key)
for c in orig:
    if c.isalpha():
        p = chr((ord(c.lower())-ord(next(keystream)))%26 + ord('a'))
        if c.isupper():
            p = p.upper()

        plaintext.append(p)
    else:
        plaintext.append(c)

print(''.join(plaintext))
