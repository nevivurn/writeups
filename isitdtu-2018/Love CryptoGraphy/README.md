# Love CryptoGraphy
**Category:** Crypto
> Download: [Link](https://bit.ly/2LHWBpx)

This short script computes

```python
x = (m* ord(i) + c) % n
```

With secret values `m`, `c`, and `n` for each character in the plaintext. Since
we know for sure that `ISITDTU` is in the plaintext, let's compute values for
`i`.

	I	73
	S	83
	I	73
	T	84
	D	68
	T	84
	U	85

We know that there'll be a repetition between the 1st and 3rd, and 4th and 6th
outputs, since they're repeated in the plaintext. We use this to locate the
known plaintext in the ciphertext.

```python
ciphers = {}
for i in range(len(plain)):
    print plain[i], ord(plain[i]), cipher[ind+i]
    ciphers[ord(plain[i])] = cipher[ind+i]
# I 73 1470896290937720121923671834268680644293311486759008609851306976
# S 83 998119569566922793772397587105095499481847516084421474175736111
# I 73 1470896290937720121923671834268680644293311486759008609851306976
# T 84 2108440654988370562048343461399852810852299068780806568036885800
# D 68 549685894064591284908235658839357390847445522332458370260385633
# T 84 2108440654988370562048343461399852810852299068780806568036885800
# U 85 903564225292763328142142737672378470519554721949504047040621938
```

Thanks to the fact that 'S' and 'T' are only 1 number apart (83 and 84), and
added to the fact that `enc(83) < enc(84)`, we conclude that the value does not
'loop over' `n` in these values.

This can be computed as follows:

```python
# enc(84) - enc(83) =
# ((m*(83+1) + c) mod n) - ((m*(83) + c) mod n) =
# ((m*(83+1) + c) + n*j) - ((m*(83) + c) + n*j) =
# m
m = ciphers[84]-ciphers[83]
# 1110321085421447768275945874294757311370451552696385093861149689L
```

We now use 'T' and 'U', also 1 apart (84 and 85), but these values do loop over,
as `enc(84) > enc(85)`.

```python
# enc(84)+m - enc(85) =
# ((m*(84) + c) mod n)+m - ((m*(84+1) + c) mod n) =
# ((m*(84) + c) + n*j)+m - ((m*(85) + c) + n*(j+1)) =
# (84m + c + nj)+m - (85m + c + n(j+1)) =
# n
n = ciphers[84]+m - ciphers[85]
# 2315197515117055002182146598022231651703195899527687614857413551L
```

Finally, we need to find `c`.

```python
# enc(68) - (68*m mod n) =
# (68*m + c mod n) - (68*m mod n) =
# c
c = (ciphers[68] - (m*68)%n) % n
# 1449370084268958114154753941529504723862204623391963277996853964L
```

Since we know `m`, `n`, and `c`, we can reverse the encryption by the following:

```python
minv = modinv(m, c)
cinv = -c % n
print(''.join([chr(((i+cinv)*minv)%n) for i in cipher]))
# Hello everybody, this is your flag: ISITDTU{break_LCG_unknown_all}
```

flag: `Hello everybody, this is your flag: ISITDTU{break_LCG_unknown_all}`
