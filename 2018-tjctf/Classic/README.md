# Classic
**Category:** Cryptography
> My primes might be close in size but they're big enough that it shouldn't matter right? [rsa.txt](https://static.tjctf.org/6bd24f59c2861c8f62358d17d677812bc079876f6951c22d13f396bbf1059cca_rsa.txt)

We're given some public parameters for RSA (`e`, `n`), and an encrypted message.
The public modulus is 1024, which wouldn't normally be practical to factor.
However, since the primes are said to be "close", it's significantly easier to
factor.

> TODO: figure out exactly why (...)

We use an online [integer factorization
calculator](https://www.alpertron.com.ar/ECM.HTM) to factor the modulus, which
gives us the two factors fairly quickly.

Afterwards, we just decrypt the ciphertext.

```python
p = 11326943005628119672694629821649856331564947811949928186125208046290130000912120768861173564277210907403841603312764378561200102283658817695884193223692869
q = 11326943005628119672694629821649856331564947811949928186125208046290130000912216246378177299696220728414241927034282796937320547048361486068608744598351187
d = number.inverse(e, (p-1)*(q-1))

print(number.long_to_bytes(pow(c, d, n)).decode('utf-8'))
```

flag: `tjctf{1_l1ke_squares}`
