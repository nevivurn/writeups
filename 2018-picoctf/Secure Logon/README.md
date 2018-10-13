# Secure Logon
**Category:** Web Exploitation
> Uh oh, the login page is more secure... I think.
> `http://2018shell1.picoctf.com:56265`
> ([link](http://2018shell1.picoctf.com:56265/)).
> [Source](https://2018shell1.picoctf.com/static/a39b448f70e7523eb03516bb9c211c1a/server_noflag.py).
>
> Hints:
> - There are versions of AES that really aren't secure.

The server uses CBC encryption to encrypt the cookies, with no MAC. This lets us
easily modify the IV and flip bits in the first 16 bytes of the plaintext.
Luckily for us, the cookie stores the admin flag (since it starts with 'a') at
the beginning, putting it within range for us.

If this weren't the case we would have had to use a slightly more complicated
scheme, by flipping bits in the second block to flip the third block (etc..) and
then chopping off the previous blocks, while making sure the cookies remained
valid.

```python
import base64
c = bytearray(base64.b64decode(c))
c[10] ^= 1
print(base64.b64encode(c).decode('utf-8'))
```

Then set the output as your cookie.

flag: `picoCTF{fl1p_4ll_th3_bit3_2efa4bf8}`
