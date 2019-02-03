# nullcon HackIM 2019

- [Website](https://ctf.nullcon.net/)
- [CTFTime](https://ctftime.org/event/741)

Solved these two challenges and then spent the rest of the time failing
miserably on the web problems...

## 2FUN
**Category**: Crypto

> 24 bit key space is brute forceable so how about 48 bit key space? flag is hackim19{decrypted flag}
> 
> 16 bit plaintext: b'0467a52afa8f15cfb8f0ea40365a6692' flag: b'04b34e5af4a1f5260f6043b8b9abb4f8'
> 
> [2fun.py](2fun.py)

The `fun` function encrypts a 16-byte block with a 3-byte key, with an XOR,
bytewise substitution, and permutation. It's fairly easy to reverse, just apply
the operations in reverse order.

As the challenge description says, if this were the only operation, we could
just brute-force the key, as 24 bits is in the realm of "doable". 48 bits is
not.

The challenge makes use of 48-bit keys by essentially applying the encryption
function twice, first with the first 3 bytes of the key, then with the latter 3.
This construction allows us to mount a [meet-in-the-middle attack](https://en.wikipedia.org/wiki/Meet-in-the-middle_attack),
effectively reducing the number of keys we need to check from `2^48` to
`2^(24+1)` , at the cost of having to store `2^24` entries in memory, which
is barely doable on our machines.

Our initial attempt was written in python, but we couldn't figure out how to
optimize it so it would run in a more reasonable time. So we wrote it in Go and
optimized that instead.

First, we store the result of encrypting the known plaintext, `16 bit plaintext` (it
is lying!) with every possible key:

```go
forward := make(map[string]int, keys)
for i, key := range allKeys {
	forward[enc(key, plain, a, b)] = i
}

```

Then, we decrypt the given ciphertext `0467a52afa8f15cfb8f0ea40365a6692` again
with every possible key, seeing if we get a value we've seen before.

```go
for i, key := range allKeys {
	ind, ok := forward[dec(key, cipher, a, b)]
	if ok {
		ans[0], ans[1] = ind, i
		break
	}
}
```

Once we find an such an entry (there is only one) we can be fairly sure we've
found the key. Just decrypt the ciphertext twice, first with the second key and
then the first.

```
forward mapping...
reverse mapping...
keys: 10647477 12696715
1337_1n_m1ddl38f

real	0m37.355s
user	0m54.180s
sys	0m1.920s
```

- flag: `hackim19{1337_1n_m1ddl38f}`
- solution: [2fun\_solution.go](2fun_solution.go)

## GenuineCounterMode
**Category**: Crypto

> server runs on
> 
> `nc crypto.ctf.nullcon.net 5000`
> 
> can you get the flag?
> 
> [server.py](server.py)

The goal of this challenge is to produce a ciphertext that will decrypt to "may
i please have the flag", but we are not allowed to encrypt the message "flag".

Preparing the ciphertext is easy enough, we send the message "may i please have
the flaf" and flip the last bit of the ciphertext, since the encryption itself
is done with AES-CTR.

The problem is with the tag, which seems to be to verify the validity of the
ciphertext, which is similar to the one used in AES-GCM, although it has a few
differences. The polynomial is "backwards", as in the earlier ciphertext blocks
are coefficients for lower powers. There is no authenticated data, and the
lengths are not added to the end. Also, the tag is not encrypted, and is used
as-is. The last bit is what allows us to mount the following attack:

If we look over the `GHASH` function,

```python
def GHASH(ciphertext, nonce):
    assert len(nonce) == 12
    c = AES.new(key, AES.MODE_ECB).encrypt(nonce + bytes(3) + b'\x01')
    blocks = group(ciphertext)
    tag = bytes_to_long(c)
    for i, b in enumerate(blocks):
        tag += (bytes_to_long(b) * pow(bytes_to_long(H), i + 1, n)) % n
    return long_to_bytes(tag)
```

we notice that the only value we do not know is `H`. We can find `c` by XORing
the first 16 bytes of the ciphertext with the plaintext, recovering the
keystream. The other coefficients are just the ciphertext split into 16-byte
groups. Then, if we can just figure out the value of `H`, we could compute the
tag ourselves!

In order to recover `H`, we produce two ciphertexts instead of just one. Let's
call the tags attached to these ciphertexts `tag_a` and `tag_b` , and the
coefficients `a_i, b_i` (i in {1, 2, 3}) . Then,

	tag_a = a_1 + a_2 H + a_3 H^2
	tag_b = b_1 + b_2 H + b_3 H^2

We can then solve for `H` :

	H = (b_3 a_2 - a_3 b_2)^-1 , ( b_3 (tag_a - a_1) - a_3 (tag_b - b_1) )
	Since
	  = (b_3 a_2 - a_3 b_2)^{-1} , (b_3 (a_2 H + a_3 H^2) - a_3 (b_2 H + b_3 H^2))
	  = (b_3 a_2 - a_3 b_2)^{-1} , ((b_3 a_2 - a_3 b_2) H + (b_3 a_3 - a_3 b_3) H^2)
	  = (b_3 a_2 - a_3 b_2)^{-1} , (b_3 a_2 - a_3 b_2) H
	  = H

This is implemented like so:

```python
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
```

Once we know the value of `H` , we can just compute the `GHASH` for our modified
ciphertext and solve the challenge.

```
[+] Opening connection to crypto.ctf.nullcon.net on port 5000: Done
[*] received: 16f78a7d6317f102bbd95240:67ee53d4062ba68c9f4517615fd60ff7e5697f8f7011e783bfc7:01e5ef9ac31b617d689902822a8cec67b0
[*] received: 16f78a7d6317f102bbd90157:91e69df4d606a138b05d550b8263d3942e74eaad0885fa29436f:028f5d75665966f73048b3322f704e62f8
[+] H: 1100811469918366171773680758187695733
[*] payload: 16f78a7d6317f102bbd95240:67ee53d4062ba68c9f4517615fd60ff7e5697f8f7011e783bfc6:01adb1d5c2fbb32cf6c1aea38cea345b62
[+] Congrats username
    Here is your flag: hackim19{forb1dd3n_made_e4sy_a7gh12}
    may i please have the flag
[*] Closed connection to crypto.ctf.nullcon.net port 5000
```

- flag: `hackim19{forb1dd3n_made_e4sy_a7gh12}`
- solution: [gcm\_solution.py](gcm_solution.py)
