import socket
import random
import time
import os
import threading
import sys


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


TCP_PORT = int(sys.argv[1])
print(TCP_PORT)


# sv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sv4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sv4.bind(('localhost', TCP_PORT))

# sv6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
# sv6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sv6.bind(('localhost', TCP_PORT))

# conn = socket.socket()


# def v4_listen():
#     sv4.listen()
#     try:
#         conn,addr = sv4.accept() 
#     except:
#         pass
#     print('Connected by', addr)

# def v6_listen():
#     sv6.listen()
#     try:
#         conn,addr = sv4.accept() 
#     except:
#         pass
#     print('Connected by', addr)
# # Conn é soquete da conexão


# v6Thread = threading.Thread(target=v6_listen)
# v6Thread .start()

# v4Thread = threading.Thread(target=v4_listen)
# v4Thread .start()

s = socket.create_server(('', TCP_PORT), family=socket.AF_INET6, dualstack_ipv6=True)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen()
conn,addr = s.accept()

print('Connected by', addr)

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.bind(('localhost', TCP_PORT))

#s.listen()
#conn,addr = s.accept() # Conn é soquete da conexão







while True: #A ideia aqui eh que o data SÓ VAI SER ZERO quando o outro lado fechar o soquete
    receiveMsg = bytearray()
    data = conn.recv(1024) #Fica travado aqui até receber bytes ou 0 (socket dead)
    if not data:
        break
    else:
        receiveMsg.extend(data)
    print('Tamanho da mensagem recebida:', len(receiveMsg))
    print('Server Received', repr(receiveMsg))


    

    #print('Mensagem: ' , receiveMsg)

    code = receiveMsg[1]
    #print("Recebemos:" , code, '\n')
    if (code==1):
        print('Entrou no code 1')
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpSocket.bind(('localhost', 5556))

        sendMsg = (2).to_bytes(2,'big')
        sendMsg += (5556).to_bytes(4, 'big')

        #print(len(sendMsg))
        #print("Server prestes a mandar mensage")
        conn.sendall(sendMsg)
        #print('Received', data)
        #print('Travado\n')
        #conn.sendall(data)

        #data = conn.recv(25)
        
    if(code==3):
        print('Entrou no code 3')
        fileName = receiveMsg[2:17].decode().replace('\x00', '')
        fileSize = int.from_bytes(receiveMsg[17:25], 'big')
        print("Cliente declaro filesize de ", fileSize)
        #print(fileName)
        #print(fileSize)

        # CRIAR ESTRUTURA DE DADOS PARA JANELA DESLIZANTE (???)
        fileDict = dict()


        sendMsg = (4).to_bytes(2,'big')
        conn.sendall(sendMsg) #ok enviado

        totalBytes = 0
        while totalBytes < fileSize:
            data, udpAddr = udpSocket.recvfrom(1024)
            print('UDP Server Received', repr(data))

            sequenceNum = int.from_bytes(data[2:6], 'big')
            payloadSize = int.from_bytes(data[6:8], 'big')
            
            payload = data[8:]

            if sequenceNum not in fileDict:
                totalBytes = totalBytes + payloadSize
                
                print('UDP Server Received PAYLOAD', repr(payload), "from sequence", sequenceNum , "total bytes: " , totalBytes)
                
                fileDict[sequenceNum] = payload


            
            sendMsg = (7).to_bytes(2, 'big') #Ack
            sendMsg += (data[2:6])
            time.sleep(random.uniform(0.3,1.2))
            conn.sendall(sendMsg)
        #print("Final result: \n")
        #print("".join(list(fileDict.values()) ))
        #print(fileDict)
        sendMsg = (5).to_bytes(2, 'big') 
        conn.sendall(sendMsg) #FIM

        f2 = open("output_" + fileName, "wb")
        for i in range (len(fileDict)):
            f2.write(fileDict[i])
        f2.close()


      

conn.close()
    