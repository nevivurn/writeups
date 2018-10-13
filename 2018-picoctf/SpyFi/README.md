# SpyFi
**Category:** Cryptography
> James Brahm, James Bond's less-franchised cousin, has left his secure
> communication with HQ running, but we couldn't find a way to steal his agent
> identification code. Can you? Conect with `nc 2018shell1.picoctf.com 37131`.
> [Source](https://2018shell1.picoctf.com/static/f17fc8f8cec5e5b01f516148a060e9d1/spy_terminal_no_flag.py).
>
> Hints:
> - What mode is being used?

It uses ECB mode.

We fully control a part of the plaintext, and we know exactly where the secret
is located in the ciphertext. Therefore, we could mount the following attack:

First, we send a message such that the first secret byte will be the last byte
of a block. Because we know the rest of the plaintext, we know what the
remaining 15 bytes are. To do this, we would obviously need to find out the
length of the flag first, which is done by sending messages of different lengths
until the ciphertext length changes.

Once we have the block of ciphertext that was constructed by encrypting the
single byte of secret information, we send guess data where we try to construct
messages that will encrypt the first 15 bytes of the target block as well as a
single guess byte. If we get it right, we will obtain the target block, which
confirms that our guess was correct.

Once we know the first byte of the secret, we can shift the message to the left
by one, construct a second target block with two bytes of secret (but we know
the first byte at this point) and then send guess blocks with 14 known plaintext
blocks, 1 secret byte and 1 guess byte. Continue for the rest of the message.

	$ ./solution.py
	[...]
	picoCTF{@g3nt6_1$_th3_c00l3$t_2432504}

flag: `picoCTF{@g3nt6_1$_th3_c00l3$t_2432504}`
