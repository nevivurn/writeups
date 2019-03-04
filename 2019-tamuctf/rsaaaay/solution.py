#!/usr/bin/env python3

import gmpy2

n, e = 2531257, 43
ctext = [906851, 991083, 1780304, 2380434, 438490, 356019, 921472, 822283, 817856, 556932, 2102538, 2501908, 2211404, 991083, 1562919, 38268]

for i in range(2, n//2):
	if n%i == 0:
		p = [i, n//i]
		break

phi = (p[0]-1) * (p[1]-1)
d = gmpy2.invert(e, phi)

dec = (str(pow(c, d, n)) for c in ctext)

for dt in dec:
    c = 0
    while dt:
        c = c*10 + int(dt[0])
        dt = dt[1:]
        if c > 60:
            print(chr(c), end='')
            c = 0
print()
