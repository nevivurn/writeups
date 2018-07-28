# XOR
**Category:** Crypto
> Download: [Link](https://bit.ly/2LLU51H)

The script uses a simple xor cipher with a 10-byte key, however, the text is
shuffled using some odd algorithm.

```python
for a in range(len(key)):
    i = a
    for b in range(len(flag)/len(key)):
        if b % 2 != 0:
            m.append(ord(flag[i]) ^ ord(key[a]))
        else:
            m.append(ord(flag[i+len(key)-(a+1+a)])^ ord(key[a]))
        i += len(key)
```

Therefore, we create an `unshuffle` function to undo the shuffling, reusing the
code from the shuffling code:

```python
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

enc_flag = unshuffle(enc_flag)
keyind =  unshuffle(keyind)
```

Then, as usual, we can use the known plaintext `ISITDTU{` (8 characters) to find
8 out of 10 characters of the key, trying all positive starting positions of the
known plaintext.

```python
plain = 'ISITDTU{'
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
```

Afterwards, we try decrypting with all the partial keys, seeing which ones will
produce only acceptable characters. For now, we'll replace the unknown bits
(since we don't know 2 characters of the key) with some placeholder.

```python
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
# ISITDTU{####ome_to_ISITDTUCT####ntest!_Hav3_a_g0####ay._Hope_y0u_w1l####j0y_and_hav3_a_h####rank_1n_0ur_F1rs####f_C0nt3st._Thank##
````

It's clear it's supposed to read some variant of "welcome", so we just add
characters to the known plaintext until we get a complete plaintext. Eventually,
we find out it's `We`. We change the known plaintext in the above script, and we
obtain:

	ISITDTU{Welcome_to_ISITDTUCTF_C0ntest!_Hav3_a_g00d_day._Hope_y0u_w1ll_3nj0y_and_hav3_a_h1gh_rank_1n_0ur_F1rst_Ctf_C0nt3st._Thank5}

flag: `ISITDTU{Welcome_to_ISITDTUCTF_C0ntest!_Hav3_a_g00d_day._Hope_y0u_w1ll_3nj0y_and_hav3_a_h1gh_rank_1n_0ur_F1rst_Ctf_C0nt3st._Thank5}`
