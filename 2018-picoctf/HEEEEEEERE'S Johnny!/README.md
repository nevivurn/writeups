# HEEEEEEERE'S Johnny!
**Category:** Cryptography
>  Okay, so we found some important looking files on a linux computer. Maybe
>  they can be used to get a password to the process. Connect with `nc
>  2018shell1.picoctf.com 42165`. Files can be found here: 
> [passwd](https://2018shell1.picoctf.com/static/0cae99a3ebd7de5e0547e1ff8da980a0/passwd)
> [shadow](https://2018shell1.picoctf.com/static/0cae99a3ebd7de5e0547e1ff8da980a0/shadow).
>
> Hints:
> - If at first you don't succeed, try, try again. And again. And again.
> - If you're not careful these kind of problems can really "rockyou".

Inspecting the files, we have the hashed root password. Just try the most common
passwords (according to the rockyou dictionary) until you get the password.

	$ ./solution 
	kissme
	$ echo -e 'root\nkissme' | nc 2018shell1.picoctf.com 42165
	Username: Password: picoCTF{J0hn_1$_R1pp3d_5f9a67aa}

flag: `picoCTF{J0hn_1$_R1pp3d_5f9a67aa}`
