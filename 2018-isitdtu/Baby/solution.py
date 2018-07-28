import socket
import re

def test(n):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('35.185.178.212', 33337))

    s.send('%d\n'%n)
    while True: 
        b = s.recv(4096)
        match = re.search('[0-9a-f]{128}', s.recv(4096))
        if match:
            return match.group(0)

want = test(0)
print 'target:', want

cur = 0
for i in range(8*30):
    t = cur | (1<<i)
    if test(t) == want:
        cur |= 1<<i
        print i, bin(cur)

c = int('1001001010100110100100101010100010001000101010001010101011110110110001001101001011101000101111101100110011011000110100101110000011100000110100101101110011001110101111101101001011100110101111101100110011101010110111001111101', 2)
s = ''
while c > 0:
    s = chr(c & 0xff) + s
    c >>= 8
print s
