#!/usr/bin/python3

import hmac
import socket
from hashlib import sha1
from struct import pack, unpack

def totp(ti, secret):
    counter = pack('>Q', int(ti) // 30)
    totp_hmac = hmac.new(secret.encode('UTF-8'), counter, sha1).digest()
    offset = totp_hmac[19] & 15
    totp_pin = str((unpack('>I', totp_hmac[offset:offset + 4])[0] & 0x7fffffff) % 1000000)
    return totp_pin.zfill(6)

secret = input("secret: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('crypto-04.v7frkwrfyhsjtbpfcppnu.ctfz.one', 7331))

sock.send(b'login</msg>')
resp = sock.recv(1024)
sock.close()
resp = int(resp[:len(resp)-6])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('crypto-04.v7frkwrfyhsjtbpfcppnu.ctfz.one', 7331))

print(totp(resp, secret))
sock.send('admin {}</msg>'.format(totp(resp,secret)).encode('utf-8'))
print(sock.recv(1024))
