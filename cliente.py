import sys 
import socket
import time
import random

temp = sys.argv[1]
pocPeerIp = temp.split(":")[0]
pocPeerPort = int(temp.split (":")[1])

print("POC IP:", pocPeerIp, "\n")
print("POC port:", pocPeerPort, "\n")

desiredChunks = [int(a) for a in sys.argv[2].split(",")] #trata-se de uma lista de inteiros que em cada cliente armazena os índices dos chunks 
#que o cliente deseja receber. É utilizado em dois momentos principais no código. 
#Primeiramente é utilizado na construção da mensagem HELLO enviada para o peer POC do cliente. 
#Posterior é utilizado também para definir as chaves do dicionário chunkPeers descrito abaixo

print("Desired Chunks:", desiredChunks, "\n")


sendMsg = (1).to_bytes(2,'big') 
sendMsg += (len(desiredChunks)).to_bytes(2,'big') 
for chunkId in desiredChunks:
    sendMsg += (chunkId).to_bytes(2,'big') 

print(sendMsg) 

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.sendto(sendMsg , (pocPeerIp, pocPeerPort)) #Ponto de contato inicial
udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udpSocket.setblocking(0)


chunkPeers = {k:[] for k in desiredChunks} #trata-se um dicionário indexado pelos índices dos chunks que o cliente deseja receber 
#presentes na lista desiredChunks. Para cada um desses chunks, 
#este dicionário armazena uma lista de tuplas (IP, porta) 
#onde cada tupla representa um peer que informou ao cliente via um transmissão CHUNK_INFO que tem este chunk disponível para requisições via GET.
#É utilizado em dois momentos: o primeiro é quando o cliente está recebendo pacotes CHUNCK_INFO que são processados 
#para identificar em quais posições do dicionario cada peer deve entrar de acordo com a lista de chunks presente em seu CHUNK\_INFO . 
#Posteriormente o chunkPeers é utilizados para decidir aleatoriamente para qual peer as requisições GET serão enviadas para cada chunk


start = time.time()
timeOut = 5
while True: #Loop recebimento chunk info
    receivedData = bytes()
    try:
        receivedData, udpAddr  = udpSocket.recvfrom(1024)
        if(receivedData[1] == 3):
            dataSenderIp = udpAddr[0]
            dataSenderPort = udpAddr[1]
            
            print("Cliente recebeu os bytes chunck data:") #Correto
            print(receivedData) #Correto

            matchedChunkCount = int.from_bytes(receivedData[2:4], 'big')
            matchedChunkList = receivedData[4:] #Problema: se id do chunck usar 2 bytes.. olhar isso dps, no peer tambem, tu ta olhando os zeros

            #Itera de id em id
            for i in range(0,(matchedChunkCount*2)-1,2): 
                matchedChunkId = int.from_bytes(matchedChunkList[i:i+2], 'big')
                chunkPeers[matchedChunkId].append(udpAddr)
    except:

        pass



    end = time.time()
    if( (end - start) > timeOut):
        break 


print("Peer de cada chunk ficou: ", chunkPeers) #correto

peerIndexPerChunk = [] #uma lista que guarda o índice do peer dentro de cada lista de peers associada com um chunk no dicionário chunkPeers, 
#que sera utilizado como destino da requisição GET que posteriormente sera chamada para cada chunk desejeado pelo cliente. 
#A construção dessa lista é randomica: para cada chunk selecionamos um peer qualquer dentre as opções presentes no chunkPeers 
#e guardamos o indice dele nesta lista.
        



for key in chunkPeers.keys():
    if(len(chunkPeers[key]) > 0):
        peerIndexPerChunk.append(random.randint(0, len(chunkPeers[key])-1))
    else:
        peerIndexPerChunk.append(-1)

for i,key in enumerate(chunkPeers.keys()):
    if(peerIndexPerChunk[i] != -1):
        print("acessando peers da key," , key, "\n")
        print("que são", chunkPeers[key])
        print("pegaremos o de index", i, "ou seja, " ,  peerIndexPerChunk[i]) #Ta correto era erro no random

        addrForGet = chunkPeers[key][peerIndexPerChunk[i]]
        sendMsg = (4).to_bytes(2, 'big')
        sendMsg += (1).to_bytes(2,'big') # O get é de apenas um chunk por vez
        sendMsg += (key).to_bytes(2, 'big')
        print("Cliente mandou get para", addrForGet , "\n")
        print("Pedindo chunk", key, "\n")
        print("Via mensagem", sendMsg)
        udpSocket.sendto(sendMsg , addrForGet) #Mandou GET

start = time.time()
timeOut = 5
f = open("output-" + udpSocket.getsockname()[0] + ".log" , "w")
while True: #Loop recebimento de chunks
    receivedData = bytes()

    try:
        receivedData, udpAddr  = udpSocket.recvfrom(1024)

        dataSenderIp = udpAddr[0]
        dataSenderPort = udpAddr[1]

        print("Cliente recebeu chunk ", int.from_bytes(receivedData[2:4],'big') ,"de", udpAddr, "\n")
        #print("A mensagem:", receivedData)

        if(receivedData[1] == 5):
            receivedChunkId = int.from_bytes(receivedData[2:4],'big')
            f.write("{}:{} - {}\n".format(dataSenderIp,dataSenderPort,receivedChunkId))
    except:
        pass
    end = time.time()
    if( (end - start) > timeOut):
        break 

for i,key in enumerate(chunkPeers.keys()):
    if(peerIndexPerChunk[i] == -1):
        f.write("{}:{} - {}\n".format("0.0.0.0","0",key))


f.close()

