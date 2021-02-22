import socket
import sys
import os
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5555))
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
    print('Tamanho da mensagem recebida:', len(receiveMsg))
    print('Client Received', repr(receiveMsg))
    code = receiveMsg[1]


#print("Cliente prestes a receber mensage")
#data = s.recv(6)
#print('Received', repr(data))
    if (code == 2): #REceber porta UDP

        udpPort = int.from_bytes(receiveMsg[2:6], 'big')
        print(udpPort)

        fileName = sys.argv[3]
        if (len(fileName) > 15 or len(fileName.split('.')) != 2 or not all(ord(c) < 128 for c in fileName) or len(fileName.split('.')[1]) > 3 ):
            print("Nome não permitido")

        msg = (3).to_bytes(2, 'big')

        padSize = 15 - len(fileName)
        msg += (0).to_bytes(padSize, 'big')

        for c in fileName:
            msg += (ord(c)).to_bytes(1,'big')

        msg += os.path.getsize(fileName).to_bytes(8,'big')

        #print(len(msg))
        s.sendall(msg)
    if (code==4):
        print("Cliente vai iniciar transferencia")
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        nextSequence = 0
        windowSize = 4
        f = open(fileName, 'rb')
        window = []
        windowIndex = dict()

        
        #awaitingAck = [0] * windowSize
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
            print("Cliente mandando INIT", repr(sendMsg))
            udpSocket.sendto(sendMsg , ('localhost', udpPort))
            timeout[i] = time.time()
        
        while(True):
            try:
                #print("Cliente vai tentar ler ack")
                ack = s.recv(6)
                ackCode = int.from_bytes(ack[0:2], 'big')
                #print("Cliente leu ack code ", ackCode)
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

                            print("Cliente mandando ", repr(sendMsg))
                            
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

                        print("Cliente REmandando ", repr(sendMsg))

                        udpSocket.sendto(sendMsg , ('localhost', udpPort))
                        timeout[i] = time.time()
                    



                    

            





        
        



            #awaitingAck[i] = 1
        

        
        







        #udpSocket.sendto("banana".encode() , ('localhost', udpPort))


#data = s.recv(2)


s.close()