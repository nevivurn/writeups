# Magic Padding Oracle
**Category:** Cryptography
> Can you help us retreive the flag from this crypto service? Connect with `nc
> 2018shell1.picoctf.com 45008`. We were able to recover some
> [Source](https://2018shell1.picoctf.com/static/71aba0dacd85657a2ab6d0f4e576bcc5/pkcs7.py)
> Code.
>
> Hints:
> - Padding Oracle
>   [Attack](https://blog.skullsecurity.org/2013/padding-oracle-attacks-in-depth)

We have a server serving a a pretty straightforward padding oracle, which we can
take advantage of to forge messages from scratch. In fact, we don't need to use
the sample cookie at all.

In essense, our goal is to create a ciphertext that, when decrypted, has a valid
PKCS7 padding, as well as being a valid json with a username, `is_admin=true`,
and an expiry date in the future.

In order to create this, we start from any block we want. We then use the
padding oracle to decrypt the block of data, which will most likely be some
random-looking bytes. This allows us to choose the previous 16 bytes such that
the final block matches the last block of the ciphertext we are trying to
create.

Then, we repeat this procedure with the block that is serving as an IV to the
forged block, and so on, until we create an entire ciphertext. We do not have to
worry about garbage values in our plaintext, since only the IV will decrypt to
some random data, and the IV will not be decrypted.

	$ ./solution.py
	[...]
	b'a214910447773be343b38a37eb11ede0de2055dc137ac626c625706299c4f269a2ee6aae3019c33f855857f96c47138ca38c0bdc2096d29e0d539cc8de071881910fe712a50bde2be6dd9cd00c45a3dd00000000000000000000000000000000'

	./ echo a214910447773be343b38a37eb11ede0de2055dc137ac626c625706299c4f269a2ee6aae3019c33f855857f96c47138ca38c0bdc2096d29e0d539cc8de071881910fe712a50bde2be6dd9cd00c45a3dd00000000000000000000000000000000 | nc 2018shell1.picoctf.com 45008
	
	Welcome to Secure Encryption Service version 1.34
	
	Here is a sample cookie:
	5468697320697320616e20495634353642fef6c675ee50fca505d4023e8c21bd0b409a1f864eec9dad32e86199b518330ab686ba7afaf345e4b2bdca541146511d82c37e7f991be60eda932d1fd407c65ab1726c337c128163c4c3449ce2398d
	What is your cookie?
	username: admin
	Admin? true
	Cookie is not expired
	The flag is: picoCTF{0r4cl3s_c4n_l34k_2ea38c7d}
	
flag: `picoCTF{0r4cl3s_c4n_l34k_2ea38c7d}`
