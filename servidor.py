import socket
import random
import time
import os
import threading
import sys


def get_free_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


TCP_PORT = int(sys.argv[1])
print(TCP_PORT)

s = socket.create_server(('', TCP_PORT), family=socket.AF_INET6, dualstack_ipv6=True)


def udp(connSocket, udpSocket, fileSize,fileName):
    fileDict = dict()
    totalBytes = 0
    while totalBytes < fileSize:
        data, udpAddr = udpSocket.recvfrom(1024)


        sequenceNum = int.from_bytes(data[2:6], 'big')
        payloadSize = int.from_bytes(data[6:8], 'big')
        
        payload = data[8:]

        if sequenceNum not in fileDict:
            totalBytes = totalBytes + payloadSize
                        
            fileDict[sequenceNum] = payload


        
        sendMsg = (7).to_bytes(2, 'big') #Ack
        sendMsg += (data[2:6])
        #time.sleep(random.uniform(0.5,1.5))
        connSocket.sendall(sendMsg)

    sendMsg = (5).to_bytes(2, 'big') 
    connSocket.sendall(sendMsg) #FIM

    f2 = open("output_" + fileName, "wb")
    for i in range (len(fileDict)):
        f2.write(fileDict[i])
    f2.close()

def file_transaction(connSocket):
    while True: #A ideia aqui eh que o data SÓ VAI SER ZERO quando o outro lado fechar o soquete
        receiveMsg = bytearray()
        data = connSocket.recv(1024) #Fica travado aqui até receber bytes ou 0 (socket dead)
        if not data:
            break
        else:
            receiveMsg.extend(data)
        print('Tamanho da mensagem recebida:', len(receiveMsg))

        code = receiveMsg[1]

        if (code==1):

            udpSocketv6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            udpSocketv6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            udpSocketv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpSocketv4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            udpPort = get_free_port()
            udpSocketv4.bind(('localhost', udpPort))
            udpSocketv6.bind(('localhost', udpPort))

            sendMsg = (2).to_bytes(2,'big')
            sendMsg += (udpPort).to_bytes(4, 'big')

            connSocket.sendall(sendMsg)


            
        if(code==3):
    
            fileName = receiveMsg[2:17].decode().replace('\x00', '')
            fileSize = int.from_bytes(receiveMsg[17:25], 'big')
            print("Cliente declaro filesize de ", fileSize)



            sendMsg = (4).to_bytes(2,'big')
            connSocket.sendall(sendMsg) #ok enviado
            v4 = threading.Thread(target=udp, args= (connSocket,udpSocketv6,fileSize,fileName))
            v4.start()
            v6 = threading.Thread(target=udp, args= (connSocket,udpSocketv4, fileSize, fileName))
            v6.start()

        

    connSocket.close()

while True:
    s.listen()
    conn,addr = s.accept()
    print('Connected by', addr)
    eg = threading.Thread(target=file_transaction, args= (conn,))
    eg.start()





    