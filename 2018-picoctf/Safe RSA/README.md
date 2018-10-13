# Safe RSA
**Category:** Cryptography
> Now that you know about RSA can you help us decrypt this
> [ciphertext](https://2018shell1.picoctf.com/static/ab772a2740031b404eba8d0cc76b43f2/ciphertext)?
> We don't have the decryption key but something about those values looks
> funky..
>
> Hints:
> - RSA [tutorial](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
> - Hmmm that e value looks kinda small right?
> - These are some really big numbers.. Make sure you're using functions that
>   don't lose any precision!

`e` is only 3, and the ciphertext seems quite small relative to the modulus,
which suggests that maybe the plaintext wasn't large enough for `m^e > N`. This
allows us to decrypt by just finding the cube root of the ciphertext.

```python
import gmpy2
from binascii import unhexlify
print(unhexlify(hex(gmpy2.iroot(c, 3)[0])[2:]).decode('utf-8'))
```

flag: `picoCTF{e_w4y_t00_sm411_34096259}`
