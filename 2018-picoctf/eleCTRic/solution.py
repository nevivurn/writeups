#!/usr/bin/env python3

from itertools import cycle
import base64

chosen = '0'*16

def get_fromshare(c):
    return bytes([ord(a)^b for a,b in zip(chosen, c)])

if __name__ == '__main__':
    share = input('sharecode:')
    key = get_fromshare(base64.b64decode(share))

    target = input('flagfile:')
    out = bytes([ord(a)^b for a,b in zip(target, cycle(key))])
    print(base64.b64encode(out))
