#!/usr/bin/env python2

enc_flag = '1d14273b1c27274b1f10273b05380c295f5f0b03015e301b1b5a293d063c62333e383a20213439162e0037243a72731c22311c2d261727172d5c050b131c433113706b6047556b6b6b6b5f72045c371727173c2b1602503c3c0d3702241f6a78247b253d7a393f143e3224321b1d14090c03185e437a7a607b52566c6c5b6c034047'
keylen = 10

def unshuffle(m):
    unshuf = [None]*len(m)
    ind = 0
    for a in range(keylen):
        i = a
        for b in range(len(m)/keylen):
            if b % 2 != 0:
                unshuf[i] = m[ind]
            else:
                unshuf[i + keylen-(a+1+a)] = m[ind]
            i += keylen
            ind += 1
    return unshuf

enc_flag = [ord(c) for c in enc_flag.decode('hex')]
keyind = []
for i in range(keylen):
    keyind += [i] * (len(enc_flag)/keylen)

enc_flag = unshuffle(enc_flag)
keyind =  unshuffle(keyind)

plain = 'ISITDTU{We'
keys = []
for off in range(len(enc_flag)-len(plain)):
    key = [None]*keylen
    for i,p in enumerate(plain):
        k = enc_flag[off+i] ^ ord(p)
        if key[keyind[off+i]] == None:
            key[keyind[off+i]] = k
        elif key[keyind[off+i]] != k:
            break
    if key.count(None) == keylen-len(plain):
        keys.append(key)

charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.!?@-{}'
for key in keys:
    plain = ''
    fine = True
    for c, k in zip(enc_flag, keyind):
        p = 0
        if key[k]:
            p = c ^ key[k]
            if chr(p) not in charset:
                fine = False
                break
        else:
            p = ord('#')
        plain += chr(p)
    if fine:
        print plain
