import socket
import random
import time
import os
import threading
import sys


def get_free_port(): #Função utilizada para encontrar portas vazias
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port

def udp(connSocket, udpSocket, fileSize,fileName): #Utilizada pelas threads UDP para efetivar a transmissão do arquivo uma vez que o "OK" for enviado
    fileDict = dict() #Dicicionario para armazenar, em ordem, os fragmentos do arquivo
    totalBytes = 0 #Contador de número de bytes recebidos em diferentes número de sequencia
    while totalBytes < fileSize: #Condição de parada da transferencia do arquivo
        data, udpAddr = udpSocket.recvfrom(1024) #Recebe a próxima mensagem vinda do cliente


        sequenceNum = int.from_bytes(data[2:6], 'big') #Captura o número de sequencia da mensagem
        payloadSize = int.from_bytes(data[6:8], 'big') #Captura o tamanho do payload contido na mensagem
        
        payload = data[8:] #Captura os bytes associados com a mensagem

        if sequenceNum not in fileDict: #Assegura que apenas novos número de sequencia são contabilizados no total de bytes
            totalBytes = totalBytes + payloadSize             
            fileDict[sequenceNum] = payload #Se o número de sequencia for inédito, armazena o payload na respectiva posição do dicionario

        sendMsg = (7).to_bytes(2, 'big') #Inicio da criação da mensagem de resposta: acknowledge
        sendMsg += (data[2:6]) #Adicionamos 
        #time.sleep(random.uniform(0.5,1.5)) #Para simular timetouts, basta descomentar essa linha, causando um delay forçado no envio do acknowledge
        connSocket.sendall(sendMsg) #Envio do acknowledge pelo canal TCP

    sendMsg = (5).to_bytes(2, 'big') #Quando a condição de parada for alcançado, o arquivo foi transmitido com sucesso: podemos então enviar uma mensagem código 5 para encerrar o TCP
    connSocket.sendall(sendMsg)

    f2 = open("output_" + fileName, "wb") #Arquivo de output
    for i in range (len(fileDict)): #Navega em todas as posições do fileDict e reconstroi o arquivo sob o nome output_nome_do_arquivo
        f2.write(fileDict[i]) 
    f2.close()

def file_transaction(connSocket): #Instanciada para todo novo cliente: recebe uma mensagem, a decodifica e toma as ações apropridadas para cada tipificador
    while True:
        receiveMsg = bytearray()
        data = connSocket.recv(1024) #Fica travado aqui até receber bytes ou 0 (socket dead)
        if not data:
            break
        else:
            receiveMsg.extend(data)
        print('Tamanho da mensagem recebida:', len(receiveMsg))
        code = receiveMsg[1]

        if (code==1): #Codigo 1 == Hello vindo do cliente
            
            #Cria-se um thread para o UDP ipv6 e outra para o UDP ipv4 já que não sabemos a priori como o cliente se comunicara
            udpSocketv6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            udpSocketv6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            udpSocketv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpSocketv4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            udpPort = get_free_port() #Pega alguma porta disponivel no SO
            udpSocketv4.bind(('localhost', udpPort))
            udpSocketv6.bind(('localhost', udpPort))

            sendMsg = (2).to_bytes(2,'big') #Envia o código 2 "CONNECTION" para o cliente com a porta UDP com que ele deve ser comunicar
            sendMsg += (udpPort).to_bytes(4, 'big')

            connSocket.sendall(sendMsg)

        if(code==3):#Codigo 3 "INFO FILE"= metadados sobre o arquivo que o cliente enviara
    
            fileName = receiveMsg[2:17].decode().replace('\x00', '') #Remove os bits vazios do espaço reservado para o nome do arquivo
            fileSize = int.from_bytes(receiveMsg[17:25], 'big') #Extrai o tamanho do arquivo declarado pelo cliente

            sendMsg = (4).to_bytes(2,'big')
            connSocket.sendall(sendMsg) #Envio do código 4 "OK"
            #Inicialização das threads de transferencia do arquivo via UDP 
            v4 = threading.Thread(target=udp, args= (connSocket,udpSocketv6,fileSize,fileName))
            v4.start()
            v6 = threading.Thread(target=udp, args= (connSocket,udpSocketv4, fileSize, fileName))
            v6.start()

    connSocket.close()

TCP_PORT = int(sys.argv[1])

s = socket.create_server(('', TCP_PORT), family=socket.AF_INET6, dualstack_ipv6=True) #Instancia e faz bind de um soquete TCP que aceita tanto chamadas ipv4 quanto ipv6 (REQUER PYTHON 3.8)

while True: #Fica continuamente recebendo novos clientes
    s.listen()
    conn,addr = s.accept()
    print('Connected by', addr)
    eg = threading.Thread(target=file_transaction, args= (conn,)) #Inicia a thread central de estabelecimento de conexão e posterior transferencia dos bytes do arquivo
    eg.start()





    