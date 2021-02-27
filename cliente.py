import socket
import sys
import os
import time

fileName = sys.argv[3]
TCP_PORT = int(sys.argv[2])
IP_ADDR = sys.argv[1]

if ':' in IP_ADDR: #Identificação da familia de enderaçamento que sera utilizada para comunicar com o servidor
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.connect((IP_ADDR, TCP_PORT))
s.setblocking(0) #Optei por tornar o TCP non-blocking para posteriormente conseguir averiguar se existem novos acknowledges e, caso contrario, prosseguir com a verificação de timeouts da janela
#PS: aqui estou chamando de timeout toda transmissão feita sem o recebimento de um acknowledge a tempo de um threshold de 1 segundo

msg = (1).to_bytes(2, 'big') #Envio do "HELLO"
s.sendall(msg) 
code = 0

while True: #Logica similar ao servidor: recebe uma mensagem, verifica qual o tipificador, toma ações apropriadas, repeat.
    receiveMsg = bytearray()
    if (code == 5): #Posicionado antes da leitura de uma nova mensagem pois sua verificação necesaria na saida do loop de transferencia do arquivo
        break

    while(True):#Como consequencia da transformação do soquete TCP em non-blocking, foi necessário um loop de tentativas recv para assegurar a leitura de mensagens
        try:
            data = s.recv(1024) 
            break 
        except:
            continue
    if not data: 
        break
    else:
        receiveMsg.extend(data) 
    code = receiveMsg[1]


    if (code == 2): #Recebimento do número da porta UDP

        udpPort = int.from_bytes(receiveMsg[2:6], 'big')

        if (len(fileName) > 15 or len(fileName.split('.')) != 2 or not all(ord(c) < 128 for c in fileName) or len(fileName.split('.')[1]) > 3 ): #Verifica que o nome do arquivo está dentro dos limites
            print("Nome não permitido")

        msg = (3).to_bytes(2, 'big')
        padSize = 15 - len(fileName) #Padding de zeros necessario caso o nome do arquivo ocupe menos que 15 bytes
        msg += (0).to_bytes(padSize, 'big')

        for c in fileName: #Navega de char em char dentro do nome do arquivo e posiciona sua codificação no arquivo
            msg += (ord(c)).to_bytes(1,'big')

        msg += os.path.getsize(fileName).to_bytes(8,'big') #Extrai o tamanho do arquivo e coloca no cabeçalho

        s.sendall(msg)
    if (code==4): #Tipificador "OK"
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        if ':' in IP_ADDR: #Verifica se o endereço do servidor está em ipv6 ou ipv4 para instanciar o soquete UDP correto
            udpSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        else:
            udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        nextSequence = 0 #Guarda o próximo número de sequencia cujo payload a janela deslizante deve tentar enviar
        windowSize = 4 #Controla o tamanho da janela deslizante
        f = open(fileName, 'rb')
        window = [] #Guarda os bytes das sequencias sendo transmitidas em dado momento de tempo
        windowIndex = dict() #Mapea os números das sequencias com o espaço que atualmente ocupam na janela. -1 significa que já receberam acknowledge

        
        timeout = [0] * windowSize #Guarda o tempo em que cada sequencia na janela atual foi enviado para verificação de timeout
        inWindow = [0] * windowSize #Guarda quais são os número de sequencia atualmente na janela deslizante
        
        while(nextSequence < windowSize): #Transfere para a janela os bytes das primeiras windowSize sequencias do arquivo
            window.append(f.read(1000))
            inWindow[nextSequence] = nextSequence
            windowIndex[nextSequence] = nextSequence 
            nextSequence = nextSequence + 1

        for i,sequence in enumerate(window): #Transmite as windowSize primeiras sequencias do arquivo
            sendMsg = (6).to_bytes(2, 'big')
            sendMsg += (i).to_bytes(4,'big')    
            sendMsg += len(sequence).to_bytes(2, 'big')
            sendMsg += sequence
            udpSocket.sendto(sendMsg , (IP_ADDR, udpPort))
            timeout[i] = time.time()
        
        while(True):
            try:
                ack = s.recv(6) #Recebe os 6 primeiros bytes do stream de controle TCP ,
                ackCode = int.from_bytes(ack[0:2], 'big')  #Extrai o tipificador da mensagem recebida
                if (ackCode == 5): #Verifica se os bytes recebidos são um comando de tipificador "5" associado com a ordem de terminar a conexão TCP pois o arquivo foi integralmente recebido
                    code = 5 #Atualiza o código utilizado fora do loop de transmissão do arquivo. Veja que no while exterior a este, se o code for 5, a conexão é terminada.
                    break 
                if (ackCode == 7): #No caso do código ser de acknowledge...
                    ackSequenceNum = int.from_bytes(ack[2:6], 'big') #Extrai o numero de sequencia do acknowledge recebido
                    if(windowIndex[ackSequenceNum] != -1): #Verifica se este acknowledge já não foi recebido antes (pode acontecer durante retransmissões de um acknolwedge repetido chegar)

                        windowIndex[nextSequence] = windowIndex[ackSequenceNum] #Armazena o fato de que o proximo número de sequencia vai ocupar o slot na janela que era ocupado pela sequencia para a qual acabamos de receber acknowledge
                        
                        windowIndex[ackSequenceNum] = -1

                        window[ windowIndex[nextSequence] ] = f.read(1000) 
                        if window[ windowIndex[nextSequence] ]: #Verifica que a proxima sequencia não é um EOF, isto é, verifica se ainda realmente existem bytes do arquivo a serem enviados
                            #Sendo o caso, então atualizados as estruras de dados
                            inWindow[windowIndex[nextSequence]] = nextSequence 
                            
                            #Criamos a mensagem a ser enviada (com os dados da NOVA sequencia)
                            sendMsg = (6).to_bytes(2, 'big')
                            sendMsg += nextSequence.to_bytes(4,'big')
                            sendMsg += (len(window[ windowIndex[nextSequence] ])).to_bytes(2, 'big') #Payload size
                            sendMsg += window[ windowIndex[nextSequence] ] 

                            #Enviamos a mensagem
                            udpSocket.sendto(sendMsg , ('localhost', udpPort))
                            timeout[ windowIndex[nextSequence] ] = time.time()

                            nextSequence = nextSequence + 1
            except:
                #break
                continue

            #Neste ponto possiveis novos acknowledges já foram tratados
            endTime = time.time() #Marcamos o tempo novamente
            threshold = 1 #Threshold para o envio de uma mensagem e o recebimento de seu acknowledge
            for i,t in enumerate(timeout): #Loop para verificar para cada mensagem na janela, se o threshold foi atingido
                if(windowIndex[inWindow[i]] != -1): #Verifica se o acknowledge dela NÃO foi recebido (windowIndex diferente de -1)
                    if( endTime - t > threshold): #Se o threshold foi atingido então.. 
                        
                        sendMsg = (6).to_bytes(2, 'big')
                        sendMsg += inWindow[i].to_bytes(4, 'big')
                        sendMsg += len(window[i]).to_bytes(2, 'big')
                        sendMsg += window[i]

                        udpSocket.sendto(sendMsg , ('localhost', udpPort)) #...Retransmite a mensagem cujo acknowledge não foi recebido a tempo
                        timeout[i] = time.time() #Marca o tempo novamente, reinicinado o timer pra essa posição da janela
                    

s.close()