import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5555))

msg = (1).to_bytes(2, 'big')
s.sendall(msg)


print("Cliente prestes a receber mensage")
data = s.recv(1024)
print('Received', repr(data))

#msg = (3).to_bytes(2, 'big')


s.close()