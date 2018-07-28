# USSH 3.0
**Category:** Crypto
> We've developed a new restricted shell. It also allows to manage user access more securely.
>
> Let's try it nc crypto-01.v7frkwrfyhsjtbpfcppnu.ctfz.one 1337

We're given a pseudo shell-like environment, and `help` lists the possible
commands. Obviously we need to read `flag.txt`, but naturally, permission
denied:

	$ cat flag.txt
	cat: flag.txt: Permission denied.
	Expect group=root

It seems we need to change our current group (`regular`, from `id` output) to
`root`. Our username does not seem to matter.

Of the commands listed, we see `session`, which we can use to get the current
session string or set it to something else. The session string looks something
like `znnwL3t5+VytUmYrYe26MQ==:IBA0/W0y48Bw0PGMDg0xYnx2sM9GgXD+BkktJCRntRs=`, in
the form of two base64-encoded messages delimited by a colon. Both message
lengths are multiples of 16 (16 and 32, respectively), which suggests that it's
using AES to encrypt the messages.

The first block could be something like an IV, we verify this by flipping bits
in the IV and see what effect it has on the session. After a bit of
experimentation, we discover that changing bytes 9-15 (if the username is long
enough) changes the n-8th byte of the username, and all other changes result in
an invalid session. This confirms that the first block is the IV, as well as
that we're probably using AES-CBC.

In order to figure out which padding scheme is being used, we just change the
last block, and we're told that `Error: PKCS7 padding is incorrect`.

After a bit of experimentation with usernames of different lengths, we figure
out that the message is `9 bytes || username || 14 bytes || padding`.

At this point, we need to guess what the contents of the 9 and 14 bytes of
unknown data could be. It turns out the message format is as follows: (the
delimiter used is `:`, but it could be something else, doesn't matter)

	username=<username>:group=regular
	012345678          0123456789abcd

Since we're using CBC, we can flip bits in the n+1th block by xoring the nth
block with the flips we want in the n+th block. This will result in some garbage
output in the block we directly modified, so we need to do this where it doesn't
matter. Luckily, it seems the server does not do any sort of sanitation or
verification of the username portion.

This means that we can simply choose a username such that it will occupy at
least one full block and allow the 14 bytes of the group chunk to be contained
in a single block, then flip bits in the block consisting entirely of username
in order to change the group block to read `:group=root[padding]`. We also cut
off the last block of "real" padding.

	Login: 12345670123456789abcdef89
	$ session --get
	1SgZBnAd1HC7L5vzLx58PQ==:8Fl/vaWdxjia3T+2seGDJBGdnoQfoHdpKkOOlrnK/2RRbYED+CZFxOmdScZ51KKZmnJdUGzDzhKCq2Xrueunag==	
	# Run solution.py and input the above session string
	$ session --set
	1SgZBnAd1HC7L5vzLx58PQ==:8Fl/vaWdxjia3T+2seGDJBGdnoQfoHdpKkOEnrilnRVRbYED+CZFxOmdScZ51KKZ
	$ id
	uid=0(root) gid=0(root) groups=0(root)
	$ cat flag.txt
	ctfzone{2e71b73d355eac0ce5a90b53bf4c03b2}

flag: `ctfzone{2e71b73d355eac0ce5a90b53bf4c03b2}`
