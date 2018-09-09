# Java Corporation
**Category:** Crypto
> Description: How much damage could a single character cause?
> 
> nc chal.noxale.com 3141
>
> [Encrypted.txt](https://ctf18.noxale.com/files/8d6c3cfc5091f294c5f3fcf30970093a/Encrypted.txt)
> [given\_server.py](https://ctf18.noxale.com/files/702ecddc3c5d593c3d544cf339cf43b5/given_server.py)

The `Encrypted.txt` has exactly 48 bytes, 3 16-byte blocks. According to the
code, this file has been encrypted with AES-CBC, the first block is the IV.

The vulnerability lies in the following code:

```python
ciphertext = client.recv(length)
plaintext = self.decrypt(ciphertext)
if self.check_pad(plaintext):
    client.send('1')
else:
    client.send('0')
```

It's a straightforward CBC padding oracle, so we just take advantage of this to
decrypt the message, one byte at a time.

	$ python3 solution.py
	[...]
	[125, 140, 83, 77, 41, 229, 21, 232, 44, 233, 246, 4, 21, 186, 73, 201, 243, 19, 21, 126, 130, 137, 189, 151, 192, 18, 95, 140, 252, 224, 67, 100]
	noxCTF{0n3_p4d_2_f4r}

flag: `noxCTF{0n3_p4d_2_f4r}`
