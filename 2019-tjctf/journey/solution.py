#!/usr/bin/env python3

from pwn import *

word = input()

p = remote('p1.tjctf.org', 8009)

p.recvuntil('step:')
p.sendline(word)

while True:
    line = p.recvline()
    print(line)
    line = line[14:-2]
    p.recvuntil('step:')
    p.sendline(line)
