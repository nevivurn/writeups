# circuit123
**Category:** Reversing
> Can you crack the key to
> [decrypt](https://2018shell1.picoctf.com/static/93233a9d94c587fd9ecfa962e86b916b/decrypt.py)
> [map2](https://2018shell1.picoctf.com/static/93233a9d94c587fd9ecfa962e86b916b/map2.txt)
> for us? The key to
> [map1](https://2018shell1.picoctf.com/static/93233a9d94c587fd9ecfa962e86b916b/map1.txt)
> is 11443513758266689915.
>
> Hints:
> - Have you heard of z3?

We overview the provided source code. It takes two command-line arguments, the
key and the ciphertext, verifying the key and then decrypting the map file.

The decryption consists of XORing the ciphertext, an integer, with the SHA-512
digest of the key. It doesn't seem plausible to attack this directly, so we'll
try to obtain the key from the verification process instead.

The verification function first treats the key as a bit vector, LSB first. It
then appends bits that are a combination of some of the previous bits or the
true value, and finally verifies the result by checking the value at a certain
index.

This means that, if we can find a value of `key[0..n]` such that the resulting
check value is the desired one, we will have a valid key. Thus, we represent the
check bit as a combination of the unknown key bits and boolean constants, and
then solve the resulting expression for each input value.

As suggested in the hints, we used the [Z3 theorem
prover](https://github.com/Z3Prover/z3). The solution code is quite similar to
the provided decryption code, as expected.

	$ ./solution.py
	sat
	219465169949186335766963147192904921805
	$ ./decrypt.py map2.txt
	Attempting to decrypt map2.txt...
	Congrats the flag for map2.txt is:
	picoCTF{36cc0cc10d273941c34694abdb21580d__aw350m3_ari7hm37ic__}

flag: `picoCTF{36cc0cc10d273941c34694abdb21580d__aw350m3_ari7hm37ic__}`
