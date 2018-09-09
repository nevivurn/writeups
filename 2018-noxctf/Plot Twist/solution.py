import random, time, socket
from randcrack import RandCrack

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('chal.noxale.com', 5115))

sock.send(b'0'*(16*624))

rc = RandCrack()
for i in range(624):
    read = 0
    while read < 34:
        read += len(sock.recv(34-read))
    read, resp = 0, b''
    while read < 37:
        resp += sock.recv(37-read)
        read += len(resp)
    resp = int(resp[20:-1])

    print('- {}'.format(resp))
    rc.submit(resp)

guess = rc.predict_getrandbits(32)
print('+ {}'.format(guess))
sock.send(str(guess).rjust(16, '0').encode('utf-8'))

read = 0
while read < 34:
    read += len(sock.recv(34-read))

print(sock.recv(1024).decode('utf-8'))

