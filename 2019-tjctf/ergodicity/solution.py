#!/usr/bin/env python3

import base64
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify
import sys

with open('keys') as k, open('enc_data.txt') as d:
    data = base64.b64decode(next(d))
    for line in k:
        ts, key, iv = line.split()

        cipher = AES.new(key, mode=AES.MODE_CBC, IV=iv)
        dec = cipher.decrypt(data)

        if b'<article>' in dec:
            print(ts, key, iv)
            break
    else:
        print('key not found')
        sys.exit(1)

    for line in d:
        try:
            data = base64.b64decode(line)
            dec = cipher.decrypt(data)
            dec = dec[:-dec[-1]]
            print(dec.decode())
        except:
            # truncated & lines following truncated lines
            continue
