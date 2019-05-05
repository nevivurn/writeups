+++
title = "INS'HACK 2019"
date = 2019-05-03
math = true
+++

- [Website](https://scoreboard.ctf.insecurity-insa.fr/)
- [CTFTime](https://ctftime.org/event/763)

## Hack Code
**Category**: Programming

> We have a little budgeting issue with our latest red team campaign. Please help us figure it out :
> 
> `https://hack-code.ctf.insecurity-insa.fr`
> 
> This challenge has 4 different flags, better solutions will grant you more flags.

The website had a problem description like so:

> ### Problem
> 
> [This file](hack-code/routes.txt) contains 10 000 network routes. We want to have at least one network tap on each route.
> Find a list of routers to intercept, and keep the number of taps low ! You will get the first flag for any solution with at most 150 taps.
> 
> ### Example
> 
> If we have the following routes :
> 
> c,b,a  
> d,a,g  
> b,c,e  
> f,d,g
> 
> One solution could be :
> 
> g  
> b

I initially tried to solve this using my own code, performing the following steps:

1. For each router, detect routers that are in a strict subset of routes that another router is in, and delete those routers.
2. "Simplify" routes by removing references to routers deleted by step 1.
3. Remove duplicate routes, created by step 2.
4. If there are any routes of size 1, add the single element of those routes to the "forced" set, and remove the "forced" routers from the router set.

By repeating these steps until there were no changes, I was able to reduce the routers to 105 forced routers and 33 "unforced" routes, for a minimum of 138 taps. This implementation can be seen [here](hack-code/incomplete.py).

At this point, I realized that this problem was quite easy to represent with z3, as follows:

1. Each router is a boolean variable.
2. Each route is an `Or` constraint between the routers in that route.
3. The goal is to minimize the number of "true" routers.

This was able to reduce the number of taps to [126](hack-code/solution.txt), which is the optimum. The website returns the following text when you give it the correct input:

```
The first flag is INSA{N0t_bad_f0r_a_start}. The next flag will be awarded at <= 135.
INSA{135_is_pretty_g0Od_but_how_l0w_c4n_u_gO}. Get your next flag at <= 128
INSA{Getting_cl0ser}. The last flag is waiting for you at 126 !
INSA{Master_of_0pt1mizatioN}. 126 is the best solution we could find, please contact @Mathis_Hammel or another admin if you find lower and we'll award you a few bonus points !
```

- flag: `INSA{N0t_bad_f0r_a_start}`
- flag: `INSA{135_is_pretty_g0Od_but_how_l0w_c4n_u_gO}`
- flag: `INSA{Getting_cl0ser}`
- flag: `INSA{Master_of_0pt1mizatioN}`
- solution: [solution.py](hack-code/solution.py)

## Yet Another RSA Challenge - Part 2
**Category**: Programming

> If not done already, you should probably attempt Part 1 of this challenge (in the Crypto category).
> 
> [Same player, shoot again.](rsa2/rsa2.tar.gz)

Similar problem as [part one](#yet-another-rsa-challenge-part-1), but with more replacements. I solved this through brute force, by computing the list of all possible values of `p`.

The list of possible values of `p` is obtained by starting with a list with one element, the original masked value of `p`. Then, go through the list of replacement pairs *in reverse order*, looping from 0 to the length of the `p` string. For each element in the list, check if the text at the index matches the replacement pair, and if they do match, add a new element to the list with the segment replaced.

Obviously this is quite slow (about 6 minutes on my machine) and requires quite a lot of memory (about 8 GiB). It's not ideal, but since the script does run in a reasonable time, I decided it was good enough. Turned out `p` was as follows:

```
27207852581327866405087823667605448590879010013227826358847092780035210321793504880325940216718337487396072164496007982969062153457249825841387303789340168307345198340289780841780775519616179644375029427001893073329165063349924021531316671597438108960745173365258247048176055774932736580556497631388766619325642748953764064431900902509832526296549507917189176177626973840443734025141158673750408928322616401221180059867496281187731967858877968251610849486692645888138411828273843287901045651440388515710393698604711633177126248348930473971258291695989452776816815123460972817838228697384263540612910611262936800312657
```

Once I obtained `p`, I decrypted the message to obtain the flag.

- flag: `INSA{Uh_never_give_4w4y_your_Pr1mes_I_m34n_duhhh}`
- solution: [solution.py](rsa2/solution.py)

## Crunchy
**Category**: Programming

> Trade 500 billion years of CPU time and 50 exabytes of RAM for a shiny flag : [crunchy](crunchy/crunchy.tar.gz)

The code is like so:

```python
def crunchy(n):
    if n < 2: return n
    return 6 * crunchy(n - 1) + crunchy(n - 2)

g = 17665922529512695488143524113273224470194093921285273353477875204196603230641896039854934719468650093602325707751568

print("Your flag is: INSA{%d}"%(crunchy(g)%100000007))
```

The `crunchy` function is much like the fibonacci sequence, but instead of $F\_n = F\_{n-1} + F\_{n-2}$ , we had $C\_n = 6 C\_{n-1} + C\_{n-2}$ .

Here, note that we can calculate both fibonacci and crunchy numbers through matrix multiplication:

$$
\begin{align}
	\begin{pmatrix}F\_{n+1} \\\\ F\_{n}\end{pmatrix} &= \begin{pmatrix}1 & 1 \\\\ 1 & 0\end{pmatrix} \begin{pmatrix}F\_n \\\\ F\_{n-1}\end{pmatrix}
	\\\\ \begin{pmatrix}C\_{n+1} \\\\ C\_{n}\end{pmatrix} &= \begin{pmatrix}6 & 1 \\\\ 1 & 0\end{pmatrix} \begin{pmatrix}C\_n \\\\ C\_{n-1}\end{pmatrix}
\end{align}
$$

Therefore, we can compute arbitrary crunchy numbers like so:

$$
\begin{pmatrix}C\_n \\\\ C\_{n-1}\end{pmatrix} = \begin{pmatrix}6 & 1 \\\\ 1 & 0\end{pmatrix}^{n-1} \begin{pmatrix}1 \\\\ 0\end{pmatrix}
$$

Also, note that the fast modular exponentiation algorithm (often used in RSA) can be generalized to matrices as well. Combining these, I could compute $C\_g \pmod{100000007}$ easily.

- flag: `INSA{41322239}`
- solution: [solution.py](crunchy/solution.py)

## Exploring the Universe
**Category**: Web

> Will you be able to find the `flag` in the `universe/` ?
> 
> I've been told that the guy who wrote this nice application called `server.py` is a huge fan of `nano` (yeah... he knows `vim` is better).
> 
> `http://exploring-the-universe.ctf.insecurity-insa.fr/`

`nano` creates a `.$filename.swp` file whenever it's editing a file. The challenge description seems to want us to access that file.

Accessing `https://exploring-the-universe.ctf.insecurity-insa.fr/.server.py.swp` gave me the server [source](universe/server.py).

Examining the source, I noticed that the application only checks whether the requested path is below `ROOT`, not `ROOT/public`. Therefore, I could request `../universe/flag` and obtain the flag:

```
curl https://exploring-the-universe.ctf.insecurity-insa.fr/../universe/flag --path-as-is 
```

- flag: `INSA{3e508f6e93fb2b6de561d5277f2a9b26bc79c5f349c467a91dd12769232c1a29}`

## Dashlame - Part 1
**Category**: Reverse

> Can you try our new [password manager](dashlame1/dashlame1.tar.gz) ? There's a free flag in every password archive created !
> 
> This challenge contains a second part in the Crypto category.

I first decompiled the `.pyc` file using an [online decompiler](https://python-decompiler.com), which gave me the [source code](dashlame1/source.py). In the source, I noticed the following line:

```python
db_fd.write(zlib.decompress('x\x9c\x0b\x0e\xf4\xc9,IUH\xcb/\xcaM,Q0f`a`ddpPP````\x82b\x18`\x04b\x164>!\xc0\xc4\xa0\xfb\x8c\x9b\x17\xa4\x98y.\x03\x10\x8d\x82Q0\n\x88\x05\x89\x8c\xec\xe2\xf2\xf2\x8c\x8d\x82%\x89I9\xa9\x01\x89\xc5\xc5\xe5\xf9E)\xc5p\x06\x93s\x90\xabc\x88\xabB\x88\xa3\x93\x8f\xab\x02\\X\xa3<5\xa9\x18\x94\xabC\\#Bt\x14J\x8bS\x8b\xf2\x12sa\xdc\x02\xa820W\x13\x927\xcf0\x00\xd1(\x18\x05\xa3`\x08\x03#F\x16mYkh\xe6\x8fO\xadH\xcc-\xc8I\x85\xe5~O\xbf`\xc7\xea\x90\xcc\xe2\xf8\xa4\xd0\x92\xf8\xc4\xf8`\xe7"\x93\x92\xe4\x8cZ\x00\xa8&=\x8f'))
```

The decompressed data contains the flag at the end.

- flag: `INSA{Tis_bUt_a_SCr4tch}`

## Yet Another RSA Challenge - Part 1
**Category**: Crypto

> [Buy an encrypted flag, get a (almost intact) prime factor for free !](rsa1/rsa1.tar.gz)
> 
> You can find a harder version of this challenge in the Programming category.

The source code is like so:

```python
import subprocess
p = subprocess.check_output('openssl prime -generate -bits 2048 -hex')
q = subprocess.check_output('openssl prime -generate -bits 2048 -hex')
flag = int('INSA{REDACTED}'.encode('hex'), 16)

N = int(p,16) * int(q,16)
print N
print '0x'+p.replace('9F','FC')
print pow(flag,65537,N)
```

This means that each insteance of `FC` in the provided `p` may actually be `9F`. Since there are only four instances of `FC` in the provided output (and thus only $2^4$ possibilities) I manually tried each possible value of `p` to see if it divided `N`.

The correct value of `p` is:

```
27869881035956015184979178092922248885674897320108269064145135676677416930908750101386898785101159450077433625380803555071301130739332256486285289470097290409044426739584302074834857801721989648648799253740641480496433764509396039330395579654527851232078667173592401475356727873045602595552393666889257027478385213547302885118341490346766830846876201911076530008127691612594913799272782226366932754058372641521481522494577124999360890113778202218378165756595787931498460866236502220175258385407478826827807650036729385244897815805427164434537088709092238894902485613707990645011133078730017425033370001084830929985251
```

- flag: `INSA{I_w1ll_us3_OTp_n3xT_T1M3}`

## Jean-Sébastien Bash
**Category**: Crypto

> I've found a revolutionary way to securely expose my server!
> 
> `ssh -i <your_keyfile> -p 2227 user@jean-sebastien-bash.ctf.insecurity-insa.fr` To find your keyfile, look into your profile on this website.

The server prompted me as such:

```
Welcome on my server. /help for help  

>/help
This is a tool so that only me can execute commands on my server
(without all the GNU/Linux mess around users and rights).

- /help for help
- /exit to quit
- /cmd <encrypted> to execute a command

Notes (TODO REMOVE THAT) ---------------------------
Ex: 
/cmd AES(key, CBC, iv).encrypt(my_command)
/cmd 7bcfab368dc137d4628dcf45d41f8885

>/cmd 7bcfab368dc137d4628dcf45d41f8885
Running b'ls -l'
total 8
-rw-r--r-- 1 root root   21 Apr 25 21:18 flag.txt
-rwxr-xr-x 1 root root 2066 Apr 25 21:50 server.py
```

On invalid padding, the server responded with `What do you mean?!`, which meant that I had a padding oracle. Furthermore, on any message with valid padding, even if it wasn't a valid command, the server would kindly decrypt the message for us:

```
>/cmd 00000000000000000000000000000062
Running b'\xcc\xcfu\xd9A\x84\x93\xe7\xdc?`(\x953\xdf'
sh: 1: Syntax error: EOF in backquote substitution
```

The above message was found by trying arbitrary messages until I found one that worked. After confirming this behavior, I tried to find a 32-byte message accepted by the server, and found the following:

```
>/cmd 0000000000000000000000000000000000000000000000000000000000000055
Running b'\x0e6u4\xae\xa0\x9d\'8\xf1B\x8b\x11\x87\xc3\xe1\x93\xd6{\xb0\x15\x8c\xbbU\xba!{"\xe4gr'
sh: 1: Syntax error: Unterminated quoted string
```

Calling the sent message `msg` and the returned message `dec`, this means that `Decrypt(msg[16:]) = dec[16:] + '\x01'` (`\x01` due to padding). This also meant that `Decrypt(d + msg[16:]) = R + d^dec[16:]`, so I could produce arbitrary plaintexts in the last 16 bytes, and as long as the first 16 bytes of garbage didn't cause too much trouble, I could execute arbitrary commands.

I could compute the value of `d` needed to create the message I wanted by computing `(dec[16:]+'\x01') ^ want`.

```
>/cmd a8f618d161acdd39db4655569c13700300000000000000000000000000000055
Running b'*\xc6o\xf1H\xb7U\x8e\xccX\xca\x8ckrW\xac; cat flag.txt'
sh: 1: *ÆoñH·UÌXʌkrW¬: not found
INSA{or4cle_P4dd1ng}
```

- flag: `INSA{or4cle_P4dd1ng}`

## Dashlame - Part 2
**Category**: Crypto

> This challenge is in two parts. You can find the first (easy) part in the Reverse Engineering category.
> 
> I've lost my master key... Please help me recover the credentials from my [archive](dashlame2/dashlame2.tar.gz) !

Examining the source obtained from [part one](#dashlame-part-1), the archive file is essentially a twice-encrypted sqlite database, with AES-CBC, using keys and IVs produced using the `get_pearson_hash` function. Examining the [wordlist](dashlame1/wordlist.txt) included in part one, there are "only" 586880 words, which is brute-forceable, but 344428134400 ( $586880^2$ ) is pushing it. In order to make the process much faster, I performed a meet-in-the-middle attack.

Thanks to the zlib-compressed data I used in part one, I knew what the first few bytes of the database were going to be (`SQLite format 3\x00`) and I had the encrypted database. Trying every single word in the wordlist, I encrypted the known plaintext with each key & IV pair, and decrypted the known ciphertext with the same, recording the output bytes in separate maps.

Once this was done, I looked for an instance of a block being in both maps, and then I could decrypt the database using the key recorded in the decryption ("backward") map, and again with the key recorded in the encryption ("forward") map, obtaining the decrypted database.

Once I had the [decrypted database](dashlame2/decrypted.db), I just had to read out the `Passwords` table.

- flag: `INSA{D0_you_f1nD_it_Risible_wh3N_I_s4y_th3_name}`
- solution: [solution.py](dashlame2/solution.py)
