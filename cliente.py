import socket
import sys
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5555))

msg = (1).to_bytes(2, 'big')
s.sendall(msg)


print("Cliente prestes a receber mensage")
data = s.recv(6)
print('Received', repr(data))


fileName = sys.argv[3]
if (len(fileName) > 15 or len(fileName.split('.')) != 2 or not all(ord(c) < 128 for c in fileName) or len(fileName.split('.')[1]) > 3 ):
    print("Nome não permitido")

#print(fileName)

msg = (3).to_bytes(2, 'big')

padSize = 15 - len(fileName)
msg += (0).to_bytes(padSize, 'big')

for c in fileName:
    msg += (ord(c)).to_bytes(1,'big')

msg += os.path.getsize(fileName).to_bytes(8,'big')

print(len(msg))
s.sendall(msg)


s.close()