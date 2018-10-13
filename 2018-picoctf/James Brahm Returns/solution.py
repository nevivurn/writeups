#!/usr/bin/env python3

import socket
import re
from binascii import hexlify, unhexlify

def until(sock, delim):
    d = bytearray()
    while delim not in d:
        out = sock.recv(1024)
        if len(out) == 0:
            raise IOError()
        d.extend(out)
    return d

def oracle(sock, msg):
    sock.sendall(b's\n' + msg+b'\n')
    return not b'Ooops!' in until(sock, b'(S)\n')

def get_blocks(sock, a, b):
    sock.sendall(b'e\n' + b'0'*a+b'\n' + b'1'*b+b'\n')

    match = re.search(b'encrypted: ([a-f0-9]+)\n', until(sock, b'(S)\n'))
    return match.group(1)

sock = socket.socket()
sock.connect(('2018shell1.picoctf.com', 22666))
until(sock, b'(S)\n')

prelen = 53
postlen = 31
finallen = 29

flaglen = 29
hashlen = 20

prepad = 11
block = 32
padding = 3

decrypt = bytearray()
while len(decrypt) < flaglen:
    try:
        out = get_blocks(sock, 11+block, padding)
        target = out[8*32:9*32]

        print('.', sep='', end='', flush=True)
        if not oracle(sock, out[:-32]+target):
            continue
        print()

    except IOError:
        sock = socket.socket()
        sock.connect(('2018shell1.picoctf.com', 22666))
        until(sock, b'(S)\n')
        continue

    out = unhexlify(out)
    target = unhexlify(target)

    decrypt.append(out[-17]^out[8*16-1]^16)

    block -= 1
    padding += 1
    print(decrypt)

print(decrypt.decode('utf-8'))
