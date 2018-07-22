# Federation Workflow System
**Category:** Crypto
> The source code for the Federation Workflow System has been leaked online this night.
>
> Our goal is to inspect it and gain access to their Top Secret documents.
>
> [sources.zip](https://ctf.bi.zone/files/sources.zip.afa88a0c79b60ae74b4bf7f32659d8c6)
>
> nc crypto-04.v7frkwrfyhsjtbpfcppnu.ctfz.one 7331

Examining the server sources, we notice a few strings and files defined. Most of
the important files seem to be stored in `../top_secret/`, except `totp.secret`.

	self.log_path = '../top_secret/server.log'
	self.real_flag = '../top_secret/real.flag'
	self.aes_key = '../top_secret/aes.key'
	self.totp_key = 'totp.secret'

Also, when returning the encrypted file data, the server prevents directory
traversal  by checking if the requested path inside the current working
directory. However, since `totp_secret` is stored in the current working
directory, we can still access it.

The server encrypts the files by first prepending `filename: ` to the contents
of the file, then encrypts it with AES-ECB. The filename here is not sanitized
or normalied in any way from user input, which gives us a pretty good encryption
oracle.

Furthermore, we can construct valid paths that refer to `../totp_secret` with
all possible lengths modulo 16, which would lead to the first few bits of the
secret being encrypted along with our known plaintext (known since we created
it), by using `./` and `../files/`. For example,

	../files/.././././totp_secret: <data>
	0123456789abcdef0123456789abcdef01234

Once the server responds with some encrypted text, we can use the encryption
oracle by sending the known plaintext + a guess, and repeat until we obtain the
same ciphertext as when we requested `totp_secret` from the server.

Also, we can use this to obtain the length of the plaintext, by seeing what
amount of padding we need to add in order to change the number of ciphertext
blocks returned. Since all offsets except 0 produced 3 blocks of extra
ciphertext, we conclude that the `totp_secret` file is 48 bytes.

Just repeat the above process for all 48 bytes of the secret, and we can fully
decrypt it:

	$ go run solution_secret.go
	[...]
	[48 98 50 53 54 49 48 57 56 48 57 48 48 99 102 102 101 54 53 98 102 97 49 49 99 52 49 53 49 50 101 50 56 98 48 99 57 54 56 56 49 97 57 51 57 97 50 100]
	0b25610980900cffe65bfa11c41512e28b0c96881a939a2d       

Now that we've obtained the secret, we just need to compute the current totp
token by obtaining the current server time, running the same function as found
in the server code, and sending this token to the server for verification.

	$ python3 solution_totp.py 
	secret: 0b25610980900cffe65bfa11c41512e28b0c96881a939a2d
	260668
	b'flag: ctfzone{A74D92B6E05F4457375AC152286C6F51}\n</msg>'

flag: `ctfzone{A74D92B6E05F4457375AC152286C6F51}`
