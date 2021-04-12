#include <pthread.h>
#include "utils.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <list>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <mutex>
#include <regex>
using namespace std;

#define BUFSZ 1024

std::vector<string> mensagens; //Armazenara todas as mensagens enviadas por clientes possibilitando parsing pela thread de cada cliente
std::mutex m1; //Sera utilizado para travar acesso ao vetor mensagens
int kill = 1; //Variavel usada em loops while para detectar a ocorrencia do comando ##kill

struct client_data //Dados que serão passados de thread mães para threads filhas
{
    int csock;
    struct sockaddr_storage storage;
    std::vector<std::string> subs; //Vetor que armazena as tag de interesse do cliente
};

void *client_receive_thread(void *data) //Thread responsavel por receber mensagens dos clientes e coloca-las no vector mensagens
{

    struct client_data *cdata = (struct client_data *)data;
    struct sockaddr *caddr = (struct sockaddr *)(&cdata->storage);
    char caddrstr[BUFSZ];
    addrtostr(caddr, caddrstr, BUFSZ);

    char buf[BUFSZ];
    char *nextMessage = NULL; //Apontador a mensagem que sera processada em cada interação do while abaixo
    char receiver[BUFSZ]; //Buffer que recebe dados do recv 

    while (kill != 0)
    {

        memset(buf, 0, BUFSZ);

        if (nextMessage != NULL) //Se NextMassage não for null isso signica que no ultimo recv recebemos parte de uma mensagem que não foi finaliza nele mesmo
            strcpy(buf, nextMessage); //Carrega em buf o inicio da mensagem que veio da ultima execução do recv

        size_t count;

        count = recv(cdata->csock, receiver, BUFSZ - 1, 0);
        printf("[msg received] %s, %d bytes: %s \n", caddrstr, (int)count, receiver);
        if (count == 0)
        {
            std::cout << "O soquete foi fechado" << cdata->csock;
            break; //Soquete foi fechado
        }
        if (memchr(receiver, 10, 500) == NULL) //Garante que exista pelo menos um \n entre os primeiros 500 bytes recebidos no recv
        {
            std::cout << "A mensagem não tem barra n em seus primeiros 500 bytes\n";
            break; //Se não existir esse \n, desencadea a eliminação do cliente
        }
        receiver[count] = '\0';


        strcpy(buf, receiver); //Concatena o segmento de mensagem do recv anterior com os novos dados recebidos em recv


        int carryOn = 1; //Variavel responsavel por indicar se apos um recv teremos um segmento de mensagem que devera ser passado à frente para a proxima iteração
        if (buf[count - 1] == '\n') //isso ocorre quando os ultimos bytes recebidos no recv não terminam em \n
        {
            carryOn = 0;
        }
        else
        {
            carryOn = 1;
        }

        nextMessage = strtok(buf, "\n"); //Separa o token que representa a proxima mensagem a ser processada

        char *nextNextMessage; //Variavel que apontara para mensagem que sera processada na proxia iteração

        while (nextMessage != NULL) 
        {
            nextNextMessage = strtok(NULL, "\n"); 
            if ((carryOn == 1) && (nextNextMessage == NULL)) //Se não existir uma mensagem após a corrente e temos bytes para a proxima iteração ...
            {

                break; //Signica que os dados carregos atualmente em nextMessage não constiuem uma mensagem completa e portanto não devem ser processados
            }
            if (strcmp(nextMessage, "##kill") == 0) 
            {
                kill = 0;
                system("./cliente 127.0.0.1 5151"); //Cria-se uma novo processo apenas para que no loop while na main saia do accept e avalie a condição do while referente ao kill
                break;
            }
            else if (nextMessage[0] == '+') //A mensagem atual começa com +
            {

                if (strspn(nextMessage + 1, "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") == strlen(nextMessage + 1)) //Verificação de validade dos caracters na mensagem
                {

                    if (std::find(cdata->subs.begin(), cdata->subs.end(), nextMessage + 1) != cdata->subs.end()) //Verifica que a tag sendo adiciona ja consta no vetor de tags de interesse do cliente
                    {

                        std::string temp(nextMessage);
                        std::string mensagem = "already subscribed to " + temp + "\n";
                        size_t count = send(cdata->csock, mensagem.c_str(), mensagem.length(), 0); //o +1 é pq o \0, que não eh contado no strlen, de fato vai ser mandado na rede
                        if (count != (mensagem.length()))
                        {
                            std::cout << "Mensagem de sub para cliente nao enviada";
                        }
                    }
                    else
                    {
                        cdata->subs.push_back(nextMessage + 1);
                    }
                }
            }
            else if (nextMessage[0] == '-') //Simetrico ao de cima
            {
                if (strspn(nextMessage + 1, "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") == strlen(nextMessage + 1))
                {

                    if (std::find(cdata->subs.begin(), cdata->subs.end(), nextMessage + 1) != cdata->subs.end())
                    {

                        std::vector<string>::iterator position = std::find(cdata->subs.begin(), cdata->subs.end(), nextMessage + 1);
                        if (position != cdata->subs.end()) // == myVector.end() means the element was not found
                            cdata->subs.erase(position);
                    }
                    else
                    {

                        std::string temp(nextMessage);
                        std::string mensagem = "not subscribed " + temp + "\n";
                        size_t count = send(cdata->csock, mensagem.c_str(), mensagem.length(), 0); //o +1 é pq o \0, que não eh contado no strlen, de fato vai ser mandado na rede
                        if (count != (mensagem.length()))
                        {
                            std::cout << "Mensagem de sub para cliente nao enviada";
                        }
                    }
                }
            }
            else
            {

                if (strspn(nextMessage, "1234567890 qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.?!:;+-*/=@#$%()[]{}\n") == strlen(nextMessage))
                {
                    m1.lock();
                    mensagens.push_back(nextMessage);
                    m1.unlock();
                }
            }
            nextMessage = nextNextMessage;
        }
    }
    pthread_exit(EXIT_SUCCESS);
}

void *client_send_thread(void *data) //Thread responsavel por vigiar o vector global de mensagens para ver se existem novas mensagens que podem ter que ser enviadas para o cliente
{
    struct client_data *cdata = (struct client_data *)data;
    size_t latest_read = 0; //Variavel que armazena qual é o indice da ultima mensagem processada para o cliente desta thread

    struct sockaddr *caddr = (struct sockaddr *)(&cdata->storage);
    char caddrstr[BUFSZ];
    addrtostr(caddr, caddrstr, BUFSZ);

    while (1)
    {
        if (mensagens.size() > latest_read) //Se o vector tiver um numero de posicoes maior do que o indice de leitura, entao existem novas mensagem ainda não processadas
        {

            std::string mensagem = mensagens[latest_read]; //Extrai a proxima mensagem a ser processada
            latest_read++;
            for (auto i = cdata->subs.begin(); i != cdata->subs.end(); ++i) //Itera sobre cada tag de interesse deste cliente
            {
                string HashTag("#");
                HashTag.append(*i); //Variavel utilizada para tentar dar match nos tokens da mensagem sendo processada

                char ParsingMessage[mensagem.length() + 1]; //Essa variavel vai apontar para a mensagem convertida de string para array de chars para uso no strtok
                strcpy(ParsingMessage, mensagem.c_str()); 
                char *NextWord = strtok(ParsingMessage, " "); //Recebe o primeiro token da mensagem, sendo que tokens são chars separados entre si por espaço
                while (NextWord != NULL)
                {

                    if (HashTag.compare(NextWord) == 0) //verifica se houve match entre a tag de interesse atual e o token corrente (que esta em hashtag)
                    {

                        mensagem.append("\n"); //Assegura que o fim da mensagem sera demarcado por um \n
                        size_t count = send(cdata->csock, mensagem.c_str(), mensagem.length(), 0); //o +1 é pq o \0, que não eh contado no strlen, de fato vai ser mandado na rede

                        if (count != (mensagem.length()))
                        {
                            std::cout << "Mensagem de sub para cliente nao enviada";
                        }
                        i = cdata->subs.end(); //Se deu match, pulamos para o fim do vetor de tags de interesse pois a mensagem ja foi enviada e não queremos duplicatas
                        i--; //Isso é feito para que o for consiga incrementar para o fim e cessar sua execução
                        break;
                    }
                    NextWord = strtok(NULL, " "); //Não deu match, pega o proximo token
                }
            }
        }
    }

    char buf[BUFSZ];
    memset(buf, 0, BUFSZ);
    pthread_exit(EXIT_SUCCESS);
}

void *client_thread(void *data) //Thread mãe do cliente responsavel por criar as threads de recebimento e envio de mensagems para o cliente
{
    struct client_data *cdata = (struct client_data *)data;
    struct sockaddr *caddr = (struct sockaddr *)(&cdata->storage);
    char caddrstr[BUFSZ];
    addrtostr(caddr, caddrstr, BUFSZ);
    printf("[log] connection from %s\n", caddrstr);

    char buf[BUFSZ];
    memset(buf, 0, BUFSZ);

    pthread_t tid_receive;
    pthread_create(&tid_receive, NULL, client_receive_thread, cdata);
    pthread_t tid_send;
    pthread_create(&tid_send, NULL, client_send_thread, cdata);

    pthread_join(tid_receive, NULL); //Se o join for superado, significa que algo aconteceu dentro da thread de receive que justica a terminação do cliente, seja uma mensagem inadequada ou um comando ##kill

    pthread_cancel(tid_send); 
    close(cdata->csock);
    pthread_exit(EXIT_SUCCESS);
}

int main(int argc, char **argv)
{
    struct sockaddr_storage storage;
    if (0 != server_sockaddr_init(argv[1], &storage))
    {
        printf("storage parse failure");
    }
    int s;
    s = socket(storage.ss_family, SOCK_STREAM, 0);
    if (s == -1)
    {
        logexit("socket");
    } //verifica retorno das funções

    int enable = 1;

    if (0 != setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int)))
    {
        logexit("setsockopt");
    }
    struct sockaddr *addr = (struct sockaddr *)(&storage);
    if (0 != bind(s, addr, sizeof(storage)))
    { //associa o socket s com o endereço especificado pela estrutura de endereço apontada por addr
        logexit("bind");
    }

    if (0 != listen(s, 10))
    { //Efetivamente abre o socket para receber conexoes, colocando-as numa fila
        logexit("listen");
    }

    char addrstr[BUFSZ];
    addrtostr(addr, addrstr, BUFSZ);
    printf("[log] bound to %s, awaiting connection \n", addrstr);

    while (kill != 0)
    {

        struct sockaddr_storage cstorage;
        struct sockaddr *caddr = (struct sockaddr *)(&cstorage); //A aplicação não precisa de identificar exatamente o tipo de IP do cliente, entao usamos sockaddr e não sockaddr_in ou sockaddr_in6, a rede sabe que esta na outra ponta
        socklen_t caddrlen = sizeof(cstorage);

        //printf("To aqui\n") ;
        int csock = accept(s, caddr, &caddrlen); //Cria um novo socket dedicado para a primeira conexao na fila do socket s
        //Podemos entao entender o socket s como sendo um front-end, ele serve apenas como uma porta acessivel por outros processo..
        //... Dai uma vez que o processo faz uma requisição no soquete s e ela é aceita pelo accept, cria-se esse novo socket para fazer conexão,uma "sessão", especificamente com o socket dentro do connect no client
        //printf("Nao To aqui") ;
        if (csock == -1)
        {
            logexit("accept");
        }

        struct client_data *cdata = (struct client_data *)malloc(sizeof(*cdata));
        if (!cdata)
        {
            logexit("malloc");
        }
        cdata->csock = csock;
        memcpy(&(cdata->storage), &cstorage, sizeof(cstorage));
        //cstorage contem informações de endereço do soquete client aceito no accept

        pthread_t tid;
        pthread_create(&tid, NULL, client_thread, cdata);
    }

    exit(EXIT_SUCCESS);
}
