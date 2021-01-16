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
    while (1)
    {
        sleep(1);
        //for (auto i = cdata->subs.begin(); i != cdata->subs.end(); ++i)
        //    std::cout << *i << ' ';
        memset(buf, 0, BUFSZ);
        //sleep(2);
        size_t count = recv(cdata->csock, buf, BUFSZ - 1, 0);
        //std::cout << "O buf é " << buf << "\n" ;
        if (buf[0] == '+')
        {
            char *pos;
            if ((pos = strchr(buf, '\n')) != NULL)
                *pos = '\0'; //remove \n
            //std::cout << "O buf é " << buf << "\n" ;
            //printf("O buf é %s", buf);
            //std::cout << "O strlen de buf+1 é " << strlen(buf+1) << "\n" ;
            //std::cout << "o verificador retorna" << strspn(buf+1, "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") << "\n";
            if (strspn(buf+1, "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") == strlen(buf+1))
            {

                //std::cout << "passei na verificação\n" ;
                if (std::find(cdata->subs.begin(), cdata->subs.end(), buf + 1) != cdata->subs.end())
                {
                    std::cout << "detectou que ja tem"
                              << "\n";
                    std::string temp(buf);
                    std::string mensagem = "already subscribed to " + temp;
                    size_t count = send(cdata->csock, mensagem.c_str(), mensagem.length() + 1, 0); //o +1 é pq o \0, que não eh contado no strlen, de fato vai ser mandado na rede
                    if (count != (mensagem.length() + 1))
                    {
                        std::cout << "Mensagem de sub para cliente nao enviada";
                    }
                }
                else
                {
                    cdata->subs.push_back(buf + 1);
                }
            }
            //for (auto i = cdata->subs.begin(); i != cdata->subs.end(); ++i)
            //  std::cout << "adicionei " << *i << ' ';
        }
        else if (buf[0] == '-')
        {

            char *pos;
            if ((pos = strchr(buf, '\n')) != NULL)
                *pos = '\0'; //remove \n
            if (strspn(buf+1, "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") == strlen(buf+1))
            {

                if (std::find(cdata->subs.begin(), cdata->subs.end(), buf + 1) != cdata->subs.end())
                {

                    std::vector<string>::iterator position = std::find(cdata->subs.begin(), cdata->subs.end(), buf + 1);
                    if (position != cdata->subs.end()) // == myVector.end() means the element was not found
                        cdata->subs.erase(position);
                    for (auto i = cdata->subs.begin(); i != cdata->subs.end(); ++i)
                        std::cout << "sobreviveu " << *i << ' ';
                }
                else
                {
                    std::cout << "detectou que nao tem"
                              << "\n";
                    std::string temp(buf);
                    std::string mensagem = "not subscribed " + temp;
                    size_t count = send(cdata->csock, mensagem.c_str(), mensagem.length() + 1, 0); //o +1 é pq o \0, que não eh contado no strlen, de fato vai ser mandado na rede
                    if (count != (mensagem.length() + 1))
                    {
                        std::cout << "Mensagem de sub para cliente nao enviada";
                    }
                }
            }
        }
        else
        {
            if (strspn(buf, "1234567890 qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.?!:;+-*/=@#$%()[]{}\n") == strlen(buf)){
                m1.lock();
                mensagens.push_back(buf);
                std::cout << "o vector global recebeu " << mensagens[0];
                m1.unlock();
            }
        }

        //printf("[msg] %s, %d bytes: %s \n", caddrstr, (int)count, buf);
    }
    pthread_exit(EXIT_SUCCESS);
}

void *client_send_thread(void *data)
{
    struct client_data *cdata = (struct client_data *)data;
    struct sockaddr *caddr = (struct sockaddr *)(&cdata->storage);
    size_t latest_read = 0;
    //std::cout << "A thread send ta funcionando \n" ;
    //std::cout << mensagens.size() << "\n";
    while (1)
    {
        sleep(1);
        //std::cout << mensagens.size() << "\n";
        if (mensagens.size() > latest_read)
        {
            //std::cout << "Novas mensagens detectadas " << cdata->csock << "\n";
            std::string mensagem = mensagens[latest_read];
            latest_read++;
            for (auto i = cdata->subs.begin(); i != cdata->subs.end(); ++i)
            {
                std::string expr = ".*#";
                expr.append(*i).append("[ \n]");
                std::string expr2 = "^#";
                expr2.append(*i).append(" \\.*");
                //std::cout << expr << "\n";
                //std::cout << expr2 << "\n";
                if (regex_match(mensagem, regex(expr)) || regex_match(mensagem, regex(expr2)))
                {
                    std::cout << "Deu match na: " << mensagem;

                    size_t count = send(cdata->csock, mensagem.c_str(), mensagem.length() + 1, 0); //o +1 é pq o \0, que não eh contado no strlen, de fato vai ser mandado na rede
                    //break ;
                    if (count != (mensagem.length() + 1))
                    {
                        std::cout << "Mensagem de sub para cliente nao enviada";
                    }
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
    //size_t count = recv(cdata->csock, buf, BUFSZ - 1, 0) ; //passado
    //printf("[msg] %s, %d bytes: %s \n", caddrstr, (int) count, buf) ;  //passado
    pthread_t tid_receive;
    pthread_create(&tid_receive, NULL, client_receive_thread, cdata);
    pthread_t tid_send;
    pthread_create(&tid_send, NULL, client_send_thread, cdata);
    //cdata->subs.push_back("ola funcionou");

    //sprintf(buf, "remote endpoint: %.1000s\n", caddrstr) ;
    //count = send(cdata->csock, buf , strlen(buf)+1, 0 ); //o +1 é pq o \0, que não eh contado no strlen, de fato vai ser mandado na rede
    //if (count != (strlen(buf)+1) ){
    //    logexit("send");
    //}

    pthread_join(tid_receive, NULL);
    close(cdata->csock);
    pthread_exit(EXIT_SUCCESS);
}

int main(int argc, char **argv)
{

    struct sockaddr_storage storage;
    if (0 != server_sockaddr_init(argv[1], argv[2], &storage))
    {
        printf("deu pau no storage parse");
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
    printf("bound to %s, waiting connection \n", addrstr);

    while (1)
    {
        sleep(1);
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
