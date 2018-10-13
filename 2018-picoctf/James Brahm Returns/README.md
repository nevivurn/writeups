# James Brahm Returns
**Category:** Cryptography
> Dr. Xernon has finally approved an update to James Brahm's spy terminal.
> (Someone finally told them that ECB isn't secure.) Fortunately, CBC mode is
> safe! Right? Connect with `nc 2018shell1.picoctf.com 22666`.
> [Source](https://2018shell1.picoctf.com/static/7858d9aeeba4938ed586cbef2931d6a9/source.py).
>
> Hints:
> - What killed SSL3?

The answer to the hint is the POODLE attack, or the "Padding Oracle On
Downgraded Legacy Encryption" attack. We follow the genral gist of the attack in
our solution.

While examining the provided source file, we notice a few things: first, the
padding is removed by only looking at the final byte of the ciphertext, and
chopping of the correct number of bytes from the end according to that byte.
Then, the server will check the integrity of the plaintext by checking if the
SHA-1 of the message matches the last 20 bytes of the plaintext. We note that
this makes it so any incorrect padding will end up with an invalid message,
because a padding byte too large or too short will make the MAC check invalid.

In this problem, we can modify two portions of the plaintext: a portion before
the secret, and a portion after the secret. This allows us to mount the
following attack:

First, we construct a plaintext that will be a multiple of 16, thus the
plaintext will be appended with a full block of padding before encryption. We
also make sure that the first byte of the secret will be at the end of a 16-byte
block. Obviously, this is only possible by knowing the length of the secret,
which we can easily discover by creating plain of diffrent lengths and seeing
when the length of the ciphertext changes.

Given this ciphertext, we can easily calculate which block contains the block
that has a single byte of the secret. Then, we send the ciphertext straight back
to the server, except this time, we've replaced the last 16 bytes (the full
block of padding) with the "target block" (the block with the unknown byte at
the end).

The server will only accept this modified ciphertext if the last byte of the
modified ciphertext decrypts to 16, which will be the case only if the last byte
of the target block, the first byte of the secret, was `16 ^ ciphertext[-17] ^
ciphertext[i-16]` with `i` as the index of the target byte in the plaintext.
This will be true with a 1/256 chance. Therefore, we can retry this method over
and over with new ciphertexts until the server accepts our modified ciphertext,
which reveals the value of the first byte of the secret.

Once we know the first value of the secret, we "shift" the plaintext to the
left, by shortening the text added before the secret by one, and lengthening the
text added after the secret by one. Then, we repeat the procedure to decrypt the
second byte of the secret, and so on.

This allows us to decrypt the ciphertext in, on average, `n*128` attempts, which
is slow, but still very much doable.

	./solution.py
	[...]
	picoCTF{g0_@g3nt006!_0574902}

flag: `picoCTF{g0_@g3nt006!_0574902}`
