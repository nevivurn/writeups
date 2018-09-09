#!/usr/bin/env python3

import socket
from Crypto.Cipher import AES

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('chal.noxale.com', 3141))

with open('Encrypted.txt', 'rb') as f:
    data = f.read()
print('data length = {}'.format(len(data)))

def check(iv, d):
    sock.send(b'32' + iv+d)
    return sock.recv(1) == b'1'

def solve(d):
    iv = bytearray(16)

    known = 0
    while known < 16:
        for v in reversed(range(256)):
            iv[-known - 1] = v

            if check(iv, d):
                if known != 15:
                    iv[-known - 2] = 1
                    if not check(iv, d):
                        iv[-known - 2] = 0
                        continue
                    iv[-known - 2] = 0

                known += 1
                print('+ {} = {}'.format(known, v))
                for i in range(known):
                    iv[-i - 1] ^= (known+1)^known
                break

    for i in range(16):
        iv[i] ^= 17
    return iv

plain = bytearray()
for i in range(1, len(data)//16):
    plain += solve(data[i*16:(i+1)*16])

print(list(plain))
for i in range(len(plain)):
    plain[i] ^= data[i]
print(plain.decode('utf-8'))
