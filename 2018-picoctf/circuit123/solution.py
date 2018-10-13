from z3 import *

with open('map2.txt') as f:
    cipher, (length, gates, check) = eval(f.read())

key = BoolVector('key', length)

for i, (name, args) in enumerate(gates):
    if name == 'true':
        key.append(True)
    else:
        u1 = Xor(key[args[0][0]], args[0][1])
        u2 = Xor(key[args[1][0]], args[1][1])
        if name == 'or':
            key.append(Or(u1, u2))
        elif name == 'xor':
            key.append(Xor(u1, u2))

s = Solver()
s.add(Xor(key[check[0]], check[1]))
print(s.check())
model = s.model()

ans = 0
for v in key[length-1::-1]:
    ans <<= 1
    if model.eval(v):
        ans += 1

print(ans)
