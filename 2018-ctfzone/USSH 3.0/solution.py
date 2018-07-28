#!/usr/bin/python3
import base64

print('connect with the username "{}"'.format('1234567' + 'a'*16 + '89'))
session = input('session: ').split(':')

iv_enc = session[0]
data = base64.b64decode(session[1])

plain= b'regular'
want = b'root' + b'\x03'*3
plain= (16-len(plain))*b'\x00' + plain
want = (16-len(want))*b'\x00' + want

diff = [a^b for a,b in zip(plain, want)]

out = bytearray(data)
for i,v  in zip(range(16,32), diff):
    out[i] ^= v

out = iv_enc + ':' + base64.b64encode(out[:48]).decode('utf-8')

print('set session to "{}"'.format(out))
