# blaise's cipher
**Category:** Cryptography
>  My buddy Blaise told me he learned about this cool cipher invented by a guy
>  also named Blaise! Can you figure out what it says? Connect with `nc
>  2018shell1.picoctf.com 46966`.
>
> Hints:
> - There are tools that make this easy.
> - This cipher was NOT invented by Pascal

Look up "blaise", and you'll quickly arrive at "Blaise de Vigenère", which
points you to a Vigenère cipher.

You can solve it using one of the many tools available online, or with some very
simple frequency analysis (since we have a pretty sizeable chunk of ciphertext,
we can get away with a very simple scoring function.

	$ ./solution.py 
	key: flagflagflagflagflag
	[...]
	Blaise de Vigenere published his description of a similar but stronger autokey cipher before the court of Henry III of France, in 1586. Later, in the 19th century, the invention of Bellaso's cipher was misattributed to Vigenere. David Kahn in his book The Codebreakers lamented the misattribution by saying that history had "ignored this important contribution and instead named a regressive and elementary cipher for him [Vigenere] though he had nothing to do with it". picoCTF{v1gn3r3_c1ph3rs_ar3n7_bad_cdf08bf0}
	[...]

flag: `picoCTF{v1gn3r3_c1ph3rs_ar3n7_bad_cdf08bf0}`
