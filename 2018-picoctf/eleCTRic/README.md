# eleCTRic
**Category:**: Cryptography
>  You came across a custom server that Dr Xernon's company eleCTRic Ltd uses.
>  It seems to be storing some encrypted files. Can you get us the flag? Connect
>  with nc 2018shell1.picoctf.com 36150. Source.  You came across a custom
>  server that Dr Xernon's company eleCTRic Ltd uses. It seems to be storing
>  some encrypted files. Can you get us the flag? Connect with `nc
>  2018shell1.picoctf.com 36150`.
>  [Source](https://2018shell1.picoctf.com/static/c410541dec00f69c06ba940a918a24c2/eleCTRic.py).
>
> Hints:
> - I have repeated myself many many many times- do not repeat yourself.
> - Do I need to say it in different words? You mustn't repeat thyself.

The vulnerability lies in the AESCipher class. It correctly generates a random
key and counter, but during encryption, we see that the counter is never
updated:

```python
def encrypt(self, raw):
    cipher = AES.new(self.key, AES.MODE_CTR, counter=lambda: self.ctr)
    return cipher.encrypt(raw).encode('base64').replace('\n', '')
```

This essentially reduces the encryption to a 16-byte (128-bit) repeating-key
multi-time-pad, easily breakable with a known plaintext attack.

We simply choose any known filename at least 16 bytes long, XOR the returned
"sharecode" (encrypted filename) with our known plaintext to recover the entire
keystream, then encrypt the target filename to retrieve the flag.

	$ ./solution.py 
	sharecode:Iclq0eZnSAb0GKqrkmn5GiHJdJWuIw== # from filename 00..00
	flagfile:flag_5d6ffd04be256f7815e4.txt
	b'd5U7holiHACiTv6rljusGCTPPNbuZk1T8Abu49Y='

	# In the nc session:
	Share code? d5U7holiHACiTv6rljusGCTPPNbuZk1T8Abu49Y=
	Data: 
	picoCTF{alw4ys_4lways_Always_check_int3grity_f3ecd90b}

flag: `picoCTF{alw4ys_4lways_Always_check_int3grity_f3ecd90b}`
