# Baby
**Category:** Crypto
> nc 35.185.178.212 33337 or nc 35.185.178.212 33338
>
> Download: [Link](https://bit.ly/2v7zBGc)

We're given a server that will compute the following for us:

```python
x = sha512(str(f | m )).digest().encode("hex")
```

Where `f` is the secret and `m` is the user-provided integer. The most important
thing to notice is that the secret and user input are combined through OR, not
XOR as it is usual. This means that if all the on bits from our input are on in
the secret, the output will not change.

Therefore, we can just try integers with a particular bit position set, and if
it produces the same output as an empty input (0), we know that we've guessed
right.

```python
cur = 0
for i in range(8*30):
    t = cur | (1<<i)
    if test(t) == want:
        cur |= 1<<i
        print i, bin(cur)
```

Once we obtain the secret, we just decode it into ascii in order to obtain the
secret.

```python
s = ''
while c > 0:
    s = chr(c & 0xff) + s
    c >>= 8
print s
# ISITDTU{bit_flipping_is_fun}
```

flag: `ISITDTU{bit_flipping_is_fun}`
