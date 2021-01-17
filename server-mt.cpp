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

std::vector<string> mensagens;
std::mutex m1;
int kill = 1;

struct client_data
{
    int csock;
    struct sockaddr_storage storage;
    std::vector<std::string> subs;
};

void *client_receive_thread(void *data)
{

    struct client_data *cdata = (struct client_data *)data;
    struct sockaddr *caddr = (struct sockaddr *)(&cdata->storage);
    char caddrstr[BUFSZ];
    addrtostr(caddr, caddrstr, BUFSZ);

    char buf[BUFSZ];
    char *nextMessage = NULL;
    char receiver[BUFSZ];

    while (kill != 0)
    {
        //for (auto i = cdata->subs.begin(); i != cdata->subs.end(); ++i)
        //    std::cout << *i << ' ';
        memset(buf, 0, BUFSZ);
        //sleep(2);
        //std::cout << "antes buf" << *buf ;
        if (nextMessage != NULL)
            strcpy(buf, nextMessage);
        // std::cout << "depois buf" << *buf ;
        size_t count;
        //sleep(1);
        //m.lock();
        //std::cout << "O count antes do recv eh " << count <<  "\n" ;
        count = recv(cdata->csock, receiver, BUFSZ - 1, 0);
        printf("[msg received] %s, %d bytes: %s \n", caddrstr, (int)count, receiver);
        if (count == 0)
        {
            std::cout << "O soquete foi fechado" << cdata->csock;
            break; //Soquete foi fechado
        }
        if (memchr(receiver, 10, 500) == NULL)
        {
            std::cout << "A mensagem não tem barra n em seus primeiros 500 bytes\n";
            break;
        }
        receiver[count] = '\0';
        //std::cout << "\n o len do receiver eh " << strlen(receiver) << "\n";

        strcpy(buf, receiver);

        //std::cout << "\n o len do buf eh " << strlen(buf) << "\n";
        int carryOn = 1;
        if (buf[count - 1] == '\n')
        {
            carryOn = 0;
        }
        else
        {
            carryOn = 1;
        }

        nextMessage = strtok(buf, "\n");
        //std::cout << "\n o len do next message eh " << strlen(nextMessage) << "\n";
        char *nextNextMessage;

        while (nextMessage != NULL)
        {
            nextNextMessage = strtok(NULL, "\n");
            if ((carryOn == 1) && (nextNextMessage == NULL))
            {
                //std::cout << "to brekando" ;
                break;
            }
            if (strcmp(nextMessage, "##kill") == 0)
            {
                kill = 0;
                system("./cliente 127.0.0.1 5151"); //Cria-se uma novo processo apenas para que no loop while na main saia do accept e avalie a condição do while referente ao kill
                break;
            }
            else if (nextMessage[0] == '+')
            {

                if (strspn(nextMessage + 1, "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") == strlen(nextMessage + 1))
                {

                    if (std::find(cdata->subs.begin(), cdata->subs.end(), nextMessage + 1) != cdata->subs.end())
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
            else if (nextMessage[0] == '-')
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

                    //for (auto i = mensagens.begin(); i != mensagens.end(); ++i)
                    //      std::cout << "- " << *i << ' ' << "\n";
                    m1.unlock();
                }
            }
            nextMessage = nextNextMessage;
        }
    }
    pthread_exit(EXIT_SUCCESS);
}

void *client_send_thread(void *data)
{
    struct client_data *cdata = (struct client_data *)data;
    size_t latest_read = 0;

    //LogOnly
    struct sockaddr *caddr = (struct sockaddr *)(&cdata->storage);
    char caddrstr[BUFSZ];
    addrtostr(caddr, caddrstr, BUFSZ);

    while (1)
    {
        if (mensagens.size() > latest_read)
        {

            std::string mensagem = mensagens[latest_read];
            latest_read++;
            for (auto i = cdata->subs.begin(); i != cdata->subs.end(); ++i)
            {
                string HashTag("#");
                HashTag.append(*i);

                char ParsingMessage[mensagem.length() + 1];
                strcpy(ParsingMessage, mensagem.c_str());
                char *NextWord = strtok(ParsingMessage, " ");
                while (NextWord != NULL)
                {

                    if (HashTag.compare(NextWord) == 0)
                    {

                        mensagem.append("\n");
                        size_t count = send(cdata->csock, mensagem.c_str(), mensagem.length(), 0); //o +1 é pq o \0, que não eh contado no strlen, de fato vai ser mandado na rede

                        if (count != (mensagem.length()))
                        {
                            std::cout << "Mensagem de sub para cliente nao enviada";
                        }
                        i = cdata->subs.end();
                        i--;
                        break;
                    }
                    NextWord = strtok(NULL, " ");
                }
            }
        }
    }

    char buf[BUFSZ];
    memset(buf, 0, BUFSZ);
    pthread_exit(EXIT_SUCCESS);
}

void *client_thread(void *data)
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

    pthread_join(tid_receive, NULL);

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
        //... Dai uma vez que o processo faz uma requisição no soquete s e ela é aceita pelo accept, cria-se esse novo socket para fazer conexão, "sessão" especificamente com o socket dentro do connect no client
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
