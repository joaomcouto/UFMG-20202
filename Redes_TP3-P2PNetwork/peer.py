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

localStorage = dict() #Trata-se de um dicionário indexado pelos índices de chunks que um dado peer tem disponível localmente. 
#Cada indice de chunk é então mapeado para uma string que guarda o nome do arquivo associado com o chunk. 
#É utilizado para verificar quais arquivos estão presentes no armazenamento local do peer

for chunk in keyValuesFile:
    chunkId = int(chunk.split(": ")[0])
    chunkString = chunk.split(": ")[1]
    localStorage[chunkId] = chunkString.strip("\n ") 

print("Ele tem os chunks", localStorage.keys())

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind((localIp, localPort))


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

        #Respondendo ao cliente: chunck info
        sendMsg = (3).to_bytes(2 , 'big')

        chuncksInStorage = [] #Uma lista utilizada na construção de mensagens de CHUNK_INFO: 
        #dada uma lista de chunks desejados por um cliente, seja via QUERY, seja via HELLO, 
        #o peer verifica a presença de cada chunk nas chaves do dicionário localStorage. 
        #Os chunks que estiverem presentes estão disponiveis localmente no peer portanto têm seus índice apendados a esta lista. 
        #Assim ao final temos uma lista de chunks para os quais houve casamento entre os chunks requisitados por um cliente 
        #e os chunks presentes no peer.

        print("POC recebeu do cliente a lista", chunckList)
        temp=[]

        for ch in range(0,(int.from_bytes(chunckCount,'big')*2)-1,2):
            temp.append(int.from_bytes(chunckList[ch:ch+2], 'big'))
            if(int.from_bytes(chunckList[ch:ch+2], 'big') in localStorage.keys()):
                chuncksInStorage.append(int.from_bytes(chunckList[ch:ch+2], 'big'))
        sendMsg += (len(chuncksInStorage)).to_bytes(2, 'big')

        print("Que tem os chunks," , temp)

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


        #Respondendo chunck info para cliente apartir de query

        chunckList = [] #apenas uma lista auxiliar utilizada para armazenar os índices dos chunks extraídos de uma query. 
        #É utilizada para iteramos sobre os chunks da query e então verificar se estão presents no localStorage do peer, 
        #auxiliando na construção de transmissões do tipo CHUNCK_INFO

        queryChunkCount = int.from_bytes(receivedData[10:12], 'big')
        queryIdList = receivedData[12:]

        for i in range(0,(queryChunkCount*2)-1,2): 
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
        sendMsg +=  f2.read(1024)

        udpSocket.sendto(sendMsg, udpAddr)
        f2.close()
            