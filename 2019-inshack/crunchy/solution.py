#!/usr/bin/env python3
mod = 100000007

def exp(m, e):
    if e == 0:
        return ((1, 0), (0, 1))
    if e%2 == 1:
        return mult(m, exp(m, e-1))
    d = exp(m, e//2)
    return mult(d, d)

def mult(a, b):
    out = list()
    for i in range(len(a)):
        row = list()
        for j in range(len(b[0])):
            n = 0
            for k in range(len(b)):
                n += a[i][k]*b[k][j]
            row.append(n % mod)
        out.append(tuple(row))
    return tuple(out)

def fast_crunchy(n):
    mat = ((6,1),(1,0))
    mat = exp(mat, n-1)
    return mat[0][0]

g = 17665922529512695488143524113273224470194093921285273353477875204196603230641896039854934719468650093602325707751568

print("INSA{%d}"%(fast_crunchy(g)))
