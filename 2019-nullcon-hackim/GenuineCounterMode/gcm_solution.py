#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long, long_to_bytes
from gmpy2 import invert
from binascii import unhexlify, hexlify
from pwn import *

n = 327989969870981036659934487747327553919
plain = 'may i please have the flaf'

r = remote('crypto.ctf.nullcon.net', 5000)

r.sendlineafter('Enter username:', 'username')

lines = []
for i in range(2):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', plain)
    line = r.recvline(keepends=False).decode()

    log.info('received: ' + line)
    lines.append(line)

# Recover coefficients
def coeffs(c):
    coeff = []
    coeff.append(xor(c, plain, cut=16))
    coeff.append(c[:16])
    coeff.append(c[16:])
    return tuple(map(bytes_to_long, coeff))

# Recover H
def recover(a, b):
    _, c1, t1 = map(unhexlify, a.split(':'))
    _, c2, t2 = map(unhexlify, b.split(':'))

    t1 = bytes_to_long(t1)
    t2 = bytes_to_long(t2)

    cof1 = coeffs(c1)
    cof2 = coeffs(c2)

    aa = (t1-cof1[0]) * cof2[2] % n
    bb = (t2-cof2[0]) * cof1[2] % n
    diff = (cof1[1]*cof2[2] - cof2[1]*cof1[2]) % n

    return (aa - bb) * invert(diff, n) % n

H = recover(lines[0], lines[1])
log.success('H: %d' % H)

def GHASH(cipher):
    tag = sum(pow(H, i, n)*x % n for i,x in enumerate(coeffs(cipher)))
    return long_to_bytes(tag)

nonce, ciphertext, _ = tuple(map(unhexlify, lines[0].split(':')))
ciphertext = ciphertext[:-1] + bytes([ciphertext[-1] ^ 1])

pay = ':'.join(map(lambda b: hexlify(b).decode(), [nonce, ciphertext, GHASH(ciphertext)]))
log.info('payload: ' + pay)

r.sendlineafter('> ', '2')
r.sendlineafter(': ', pay)

log.success(r.recvuntil('may i please have the flag').decode())
