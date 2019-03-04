#!/usr/bin/env python3

pkey = [99, 1235, 865, 990, 5, 1443, 895, 1477]
ctext = '11b90d6311b90ff90ce610c4123b10c40ce60dfa123610610ce60d450d000ce61061106110c4098515340d4512361534098509270e5d09850e58123610c9'

mapping = dict()
for c in range(256):
    enc = 0
    for i in range(8):
        if c&(1<<i):
            enc += pkey[i]
    mapping[hex(enc)[2:]] = chr(c)

d = ''
while ctext:
    if not d and ctext[0] == '0':
        ctext = ctext[1:]
    d += ctext[0]
    ctext = ctext[1:]

    if d in mapping:
        print(mapping[d], end='')
        d = ''
print()
