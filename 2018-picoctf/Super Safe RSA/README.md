# Super Safe RSA
**Category:** Cryptography
>  Dr. Xernon made the mistake of rolling his own crypto.. Can you find the bug
>  and decrypt the message? Connect with `nc 2018shell1.picoctf.com 59208`.
>
> Hints:
> - Just try the first thing that comes to mind.

	$ nc 2018shell1.picoctf.com 59208
	c: 6894860222013150012154822541006007269632049899514873813327878590624006145299286
	n: 13339944981557564628315505106232801354185096187942443807854350103992956434464167
	e: 65537

The modulus is too small to be safe. Let's just factor it. This [online
factorizer](https://www.alpertron.com.ar/ECM.HTM) takes about 10 minutes on my
machine to complete.

```python
import gmpy2
from binascii import unhexlify
print(unhexlify(hex(pow(c, gmpy2.invert(e, phi), n))[2:]).decode('utf-8'))
# picoCTF{us3_l@rg3r_pr1m3$_5327}
```

flag: `picoCTF{us3_l@rg3r_pr1m3$_5327}`
