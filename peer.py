
import sys
import socket 
import os

temp = sys.argv[1]
localIp = temp.split(":")[0]
localPort = int(temp.split (":")[1])
keyValuesFileName = sys.argv[2]
neighbors = sys.argv[3:]

print("Este peer escuta no IP", localIp, "\n")
print("Na porta", localPort, "\n")
print("Seu arquivo keyValues é o", keyValuesFileName, "\n")
print("E seus vizinhos são", neighbors, "\n")

keyValuesFile = open(keyValuesFileName, "r")

localStorage = dict()

for chunk in keyValuesFile:
    chunkId = int(chunk[0])
    chunkString = chunk.split(": ")[1]
    localStorage[chunkId] = chunkString.strip("\n ") 

#print(localStorage.keys())
#print(localStorage.values())
#print(localStorage)

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind((localIp, localPort))


#Peers precisam conseguir lidar com varias consultas ao mesmo tempo
#Peers precisam conseguir transmitir varios chinks a clientes diferentes ao mesmo tempo




while True:
    receivedData, udpAddr = udpSocket.recvfrom(1024) 
    print("Peer recebeu mensagem de", udpAddr)
    dataSenderIp = udpAddr[0]
    dataSenderPort = udpAddr[1]
    msgType = receivedData[1]
    print("De tipo:", msgType)
    if (msgType == 1):  #hello de um cliente
        sendMsg = (2).to_bytes(2,'big')
        for byte in dataSenderIp.split('.'):
            sendMsg+= (int(byte)).to_bytes(1,'big')
        sendMsg+= (dataSenderPort).to_bytes(2, 'big')
        sendMsg += (3).to_bytes(2, 'big')
        chunckCount = receivedData[2:4]
        sendMsg += chunckCount
        chunckList = receivedData[4:]
        sendMsg += chunckList
        for neighbor in neighbors:
            neighborIp = neighbor.split(":")[0]
            neighborPort = int(neighbor.split(":")[1])
            print("Peer mandando query pra seu vizinho", neighborIp,neighborPort) 
            udpSocket.sendto(sendMsg , (neighborIp, neighborPort))
        #print(sendMsg) #Ta certin

        #Respondendo ao cliente: chunck info
        sendMsg = (3).to_bytes(2 , 'big')
        chuncksInStorage = []
        for cId in chunckList:
            if(int(cId) in localStorage.keys()):
                chuncksInStorage.append(int(cId))
        sendMsg += (len(chuncksInStorage)).to_bytes(2, 'big')

        print("Peer tem os seguintes chunks:", chuncksInStorage)
        for i in chuncksInStorage:
            sendMsg += (i).to_bytes(2, 'big')  
        print("Peer verificou seus chuncks e respondeu chunck info:" , sendMsg)
        udpSocket.sendto(sendMsg, (dataSenderIp, dataSenderPort) )   

    if (msgType == 2): #Recebeu query de vizinho, responder cliente e retransmitir pra vizinhos com ttl menor

        print("Peer recebeu a query ", receivedData)

        if(int.from_bytes(receivedData[8:10], 'big') > 1):
            sendMsg = receivedData[:8]
            sendMsg += (int.from_bytes(receivedData[8:10], 'big') - 1).to_bytes(2, 'big')
            sendMsg += receivedData[10:]
            #sendMsg[8:10] = (int.from_bytes(receivedData[8:10], 'big') - 1).to_bytes(2, 'big')


            #Transmitindo pra vizinhos
            for neighbor in neighbors:
                neighborIp = neighbor.split(":")[0]
                neighborPort = int(neighbor.split(":")[1])
                if(neighborIp != dataSenderIp and neighborPort != dataSenderPort):
                    print("Peer mandando query pra seu vizinho", neighborIp,neighborPort) 
                    udpSocket.sendto(sendMsg , (neighborIp, neighborPort))


        #respondendo chunck info para cliente apartir de query
        chunckList = []
        queryChunkCount = int.from_bytes(receivedData[10:12], 'big')
        queryIdList = receivedData[12:]

        for i in range(0,(queryChunkCount*2)-1,2): 
            #chunckList.append(int.from_bytes(queryIdList[i],'big'))
            chunckList.append(int.from_bytes(queryIdList[i:i+2], 'big'))
        print("Peer identificou na query os chunks ", chunckList)

        sendMsg = (3).to_bytes(2 , 'big')
        chuncksInStorage = []
        for chunckId in chunckList:
            if(int(chunckId) in localStorage.keys()):
                chuncksInStorage.append(int(chunckId))
        sendMsg += (len(chuncksInStorage)).to_bytes(2, 'big')

        print("Peer QUERY tem os seguintes chunks:", chuncksInStorage)
        for i in chuncksInStorage:
            sendMsg += (i).to_bytes(2, 'big')  
        print("Peer QUERY verificou seus chuncks e  vai responder chunck info:" , sendMsg)
        queryIp = ""
        for byte in receivedData[2:6]:
            #queryIp += int.from_bytes(byte, 'big')
            queryIp += str(byte)
            queryIp += "."
        queryIp = queryIp[:-1]
        
        queryPort = int.from_bytes(receivedData[6:8],'big')

        print("Para ", queryIp,queryPort)

        udpSocket.sendto(sendMsg,(queryIp,queryPort))

    if (msgType == 4): #Recebeu get do cliente
        
        requestedChunk = int.from_bytes(receivedData[4:6], 'big')
        print("Peer recebeu GET do cliente, pedindo chunk",requestedChunk, "\n")

        sendMsg = (5).to_bytes(2, 'big') 
        sendMsg += requestedChunk.to_bytes(2,'big')
        sendMsg += os.path.getsize(localStorage[requestedChunk]).to_bytes(2,'big')
        f2 = open(localStorage[requestedChunk], "rb")
        #print("Abrir", localStorage[requestedChunk])
        sendMsg +=  f2.read(1024)

        #print("Peer enviando mensagem," , sendMsg)

        udpSocket.sendto(sendMsg, udpAddr)
            
        



        #Problema ate segunda ordem: vizinho chamar vizinhos que o chamam e isso ficar em loop e floodar o buffer




#     print(data)
#     print(udpAddr)
#     sendMsg = (1).to_bytes(2,'big') 
#     udpSocket.sendto(sendMsg , (udpAddr))
