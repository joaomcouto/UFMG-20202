import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 5555))

s.listen()
conn,addr = s.accept() # Conn é soquete da conexão

print('Connected by', addr)


receiveMsg = bytearray()
while True: #A ideia aqui eh que o data SÓ VAI SER ZERO quando o outro lado fechar o soquete
    data = conn.recv(2) #Fica travado aqui até receber bytes ou 0 (socket dead)
    if not data:
        break
    else:
        receiveMsg.extend(data)
    print('Tamanho da mensagem recebida:', len(receiveMsg))
    #print('Mensagem: ' , receiveMsg)

    code = receiveMsg[1]
    print("Recebemos:" , code, '\n')
    if (code==1):
        print('Entrou no code 1')
        #udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #udpSocket.bind(('localhost', 5556))

        sendMsg = (2).to_bytes(2,'big')
        sendMsg += (5556).to_bytes(4, 'big')

        print(len(sendMsg))
        print("Server prestes a mandar mensage")
        conn.sendall(sendMsg)
        #print('Received', data)
        #print('Travado\n')
        #conn.sendall(data)



    

conn.close()
    