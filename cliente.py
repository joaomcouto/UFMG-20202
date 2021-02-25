import socket
import sys
import os
import time

fileName = sys.argv[3]
TCP_PORT = int(sys.argv[2])
IP_ADDR = sys.argv[1]

if ':' in IP_ADDR:
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



s.connect((IP_ADDR, TCP_PORT))
s.setblocking(0) 

msg = (1).to_bytes(2, 'big')
s.sendall(msg)
code = 0



while True: #A ideia aqui eh que o data SÓ VAI SER ZERO quando o outro lado fechar o soquete
    receiveMsg = bytearray()
    if (code == 5):
        break

    while(True):
        try:
            data = s.recv(1024) #Fica travado aqui até receber bytes ou 0 (socket dead)
            break
        except:
            continue
    if not data:
        break
    else:
        receiveMsg.extend(data)
    code = receiveMsg[1]


    if (code == 2): #REceber porta UDP

        udpPort = int.from_bytes(receiveMsg[2:6], 'big')
        #print(udpPort)

        
        if (len(fileName) > 15 or len(fileName.split('.')) != 2 or not all(ord(c) < 128 for c in fileName) or len(fileName.split('.')[1]) > 3 ):
            print("Nome não permitido")

        msg = (3).to_bytes(2, 'big')

        padSize = 15 - len(fileName)
        msg += (0).to_bytes(padSize, 'big')

        for c in fileName:
            msg += (ord(c)).to_bytes(1,'big')

        msg += os.path.getsize(fileName).to_bytes(8,'big')

        s.sendall(msg)
    if (code==4):
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        if ':' in IP_ADDR:
            udpSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        else:
            udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        nextSequence = 0
        windowSize = 4
        f = open(fileName, 'rb')
        window = []
        windowIndex = dict()

        
        timeout = [0] * windowSize
        inWindow = [0] * windowSize
        
        while(nextSequence < windowSize):
            window.append(f.read(1000))
            inWindow[nextSequence] = nextSequence
            windowIndex[nextSequence] = nextSequence 
            nextSequence = nextSequence + 1

        for i,sequence in enumerate(window):
            sendMsg = (6).to_bytes(2, 'big')
            sendMsg += (i).to_bytes(4,'big')    
            sendMsg += len(sequence).to_bytes(2, 'big')
            sendMsg += sequence
            udpSocket.sendto(sendMsg , (IP_ADDR, udpPort))
            timeout[i] = time.time()
        
        while(True):
            try:
                ack = s.recv(6)
                ackCode = int.from_bytes(ack[0:2], 'big')
                if (ackCode == 5):
                    code = 5
                    break 
                if (ackCode == 7):
                    ackSequenceNum = int.from_bytes(ack[2:6], 'big')
                    if(windowIndex[ackSequenceNum] != -1):

                        windowIndex[nextSequence] = windowIndex[ackSequenceNum]
                        
                        windowIndex[ackSequenceNum] = -1

                        window[ windowIndex[nextSequence] ] = f.read(1000)
                        if window[ windowIndex[nextSequence] ]:
                            inWindow[windowIndex[nextSequence]] = nextSequence
                            
                            sendMsg = (6).to_bytes(2, 'big')
                            sendMsg += nextSequence.to_bytes(4,'big')
                            sendMsg += (len(window[ windowIndex[nextSequence] ])).to_bytes(2, 'big') #Payload size
                            sendMsg += window[ windowIndex[nextSequence] ] 

                            #print("Cliente mandando ", repr(sendMsg))
                            
                            udpSocket.sendto(sendMsg , ('localhost', udpPort))
                            timeout[ windowIndex[nextSequence] ] = time.time()

                            

                            nextSequence = nextSequence + 1
            except:
                #break
                continue
            endTime = time.time()
            threshold = 1
            for i,t in enumerate(timeout):
                if(windowIndex[inWindow[i]] != -1):
                    if( endTime - t > threshold):
                        
                        sendMsg = (6).to_bytes(2, 'big')
                        sendMsg += inWindow[i].to_bytes(4, 'big')
                        sendMsg += len(window[i]).to_bytes(2, 'big')
                        sendMsg += window[i]
                        
                        udpSocket.sendto(sendMsg , ('localhost', udpPort))
                        timeout[i] = time.time()
                    

s.close()