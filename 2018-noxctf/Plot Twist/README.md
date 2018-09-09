# Plot Twist
**Category:** Crypto
> Can you get the flag from the flawlessly written server?
> 
> nc chal.noxale.com 5115
>
> [server.py](https://ctf18.noxale.com/files/b5dc0ba4648f8937d4e3ee1de7acec04/server.py)

The important bit of the server code is as follows:

```python
def getKey(self, r):
    return str(r.getrandbits(32)).rjust(16, '0')

def listenToClient(self, client, address):
    # ...
    key = self.getKey(r)
    # ...
    while True:
        try:
            client.send('Please insert the decryption key:\n')
            key_guess = client.recv(16)
            if key_guess == key:
                client.send('Correct! Your flag is: ' + self.decrypt(key, client_flag) + '\n')
                client.close()
                break
            else:
                client.send('Wrong! The key was: ' + key + '\n')
                client_flag = self.decrypt(key, client_flag)
                key = self.getKey(r)
                client_flag = self.encrypt(key, client_flag)
```

The server generates random numbers with getrandbits(32), and reveals them to us
every time we guess wrong. We just need to get it right once.

Luckily, the server does not use a cryptographically secure rng, it becomes
predictable after observing enough bits. Additionally, we're given 32 bits,
which reveals all the bits produced by the rng, since random generates 32 bits
at a time.

Look around a bit, we find
[RandCrack](https://github.com/tna0y/Python-random-module-cracker). We just use
this.

	$ python3 solution.py
	[...]
	+ 2465292517
	Correct! Your flag is: noxCTF{41w4ys_us3_cryp70_s3cur3d_PRNGs}

flag: `noxCTF{41w4ys_us3_cryp70_s3cur3d_PRNGs}`
