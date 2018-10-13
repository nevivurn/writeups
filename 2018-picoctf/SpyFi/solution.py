#!/usr/bin/env python3

from binascii import unhexlify
import socket

class Conn:
    def __init__(self, host, port):
        s = socket.socket()
        s.connect((host, port))
        self.s = s

    def until(self, delim):
        if type(delim) == str:
            delim = delim.encode('utf-8')

        d = bytes()
        while True:
            c = self.s.recv(1024)
            d += c
            if delim in c:
                break
        return d

    def send(self, s):
        if type(s) == str:
            s = s.encode('utf-8')
        self.s.sendall(s + b'\n')

pre = """Agent,
Greetings. My situation report is as follows:
"""
post = """
My agent identifying code is: """
final = """.
Down with the Soviets,
006
"""

def check(s):
    c = Conn('2018shell1.picoctf.com', 37131)
    c.until(':')
    c.send(s)
    out = c.until('\n').strip()
    c.s.close()
    return out

flaglen = 38

known = []
block = post[-15:]

prepad = '0'*11
payload = '0'*48

charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_-/!@#$%^&*()+='

for pos in range(flaglen):
    get = check(prepad+payload)
    target = get[128*2:128*2+32]

    for c in charset:
        get = check(prepad+block+c)
        get = get[64*2:64*2+32]

        if get == target:
            known.append(c)
            block = block[1:]+c
            payload = payload[1:]

            print(pos, c)
            break

    if len(known)-1 != pos:
        print('FAILED')
        break

print(''.join(known))
