# Simple RSA
**Category:** Crypto
> Download: https://bit.ly/2LDPBtM

This implementation of RSA is atypical in two important ways. First, it uses
four (~251 bit) primes, not two. Second, only the first prime is selected
randomly. The other four are selected through the following function:

```python
def next_prime(n):
    num = n + 1
    while True:
        if isPrime(num):
            return num
        num += 1
p = random.randint(1<<251,1<<252)
i = 10
p = next_prime(p)
p1 = next_prime(p*10)
p2 = next_prime(p1*10)
p3 = next_prime(p2*10)
```

In general, the `next_prime` function will search only a few values before it
finds a valid prime. `N` expressed in terms of `p`, then, is as follows:

	N = p[0] * p[1] * p[2] * p[3]
	= p[0] * (10p[0] + a) * (10p[1] + b) * (10p[2] + c)
	= p[0] * (10p[0] + a) * (100p[0] + 10a + b) * (1000p[2] + 100a + 10b + c)
	Since a, b, c << p,
	N ~ 1000000 * p[0]^4

This means that we can estimate the value of `p` by first performing a binary
search in the entire range `[1<<251, 1<<252]` in order to get a value of `p`
that gets us a value `1000000 * p^4 ~ N`. Afterwards, we can simply search
values close to this guess until we obtain a factor of `N`.

```python
for g in range(-1000+guess, 1000+guess):
    if n % g == 0:
        p = g
        break
```

We then obtain the next four primes in the same way they were first generated:

```python
primes = [p]
for i in range(3):
    primes.append(next_prime(primes[i]*10))
```

Afterwards, we just calculate `phi` as the product of `p-1` for each prime, then
find the multiplicative inverse of `e` modulo `phi`, and we decrypt the
ciphertext.

```python
phi = reduce(lambda a,b: a*(b-1), primes, 1)
print(long_to_bytes(pow(c, modinv(65537, phi), n)).decode('utf-8'))
# ISITDTU{f6b2b7472273aacf803ecfe93607a914}
```

flag: `ISITDTU{f6b2b7472273aacf803ecfe93607a914}`
