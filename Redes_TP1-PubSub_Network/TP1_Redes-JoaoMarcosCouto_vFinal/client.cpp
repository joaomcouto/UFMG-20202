#include <pthread.h>
#include "utils.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <list>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <mutex>
#include <regex>
using namespace std;

#define BUFSZ 1024
void *client_receive_thread(void *data)

{

    int *s = (int *)data;
    char buf[BUFSZ];
    while (1)
    {
        memset(buf, 0, BUFSZ);
        unsigned total = 0;

        total = recv(*s, buf + total, BUFSZ - total, 0);
        if (total == 0)
        {
            std::cout << "Cliente detectou fechamento da conexao\n";
            break;
        }

        //Buf + total esta simplesmente deslocando o local (adicionando um delta em relacao ao local apontando pelo ponteiro buf) em que o recv vai escrever a proxima parte ("pacote") da mensagem
        //... Alem disso reduzimos o numero de bytes maximo que ele deve receber do "pacote", pois o buf tem tamanho limitado BUFSZ
        // ... Assim se a mensagem tiver sido espalhada em multiplos "pacotes", só escrevemos o que ainda couber no buf

       
        if (strlen(buf) != 0)
            puts(strcat(buf, "\n")); 
    }
    pthread_exit(EXIT_SUCCESS);
}

void *client_send_thread(void *data)
{
    int * s = (int *)data ; 
    char buf[BUFSZ]; 
    while (1)
    {
        memset(buf, 0, BUFSZ);
        printf("mensagem> ");
        fgets(buf, BUFSZ - 1, stdin);

        if (strspn(buf, "1234567890 qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.?!:;+-*/=@#$%()[]{}\n") == strlen(buf)) //verificação de validade de caracters sendo enviados
        {
            size_t count = send(*s, buf, strlen(buf), 0);
            if (count != (strlen(buf)))
            {
                logexit("send");
            }
        }

        //Send recebe o socket, o buffer e o tamanho maximo de leitura: necessario porque do contrario o send é interrompido com
        //size_t : tamanho maximo de endereços memória que depende do ambiente em que se pretende executa o programa, todavia isso é definido no momento de compilação
        //.. Então por exemplo, se estamos fazendo um programa pra rodar embarcado, deve-se cuidar para incluir headers que apropriadamente definam o ambiente embarco, inlucindo a definição do size_t
        // ...
        //O terceiro parametro de send é simplesmente o numero de bytes que ele deve ler no local apontado pelo pointer no segundo parametro
        //O strlen para de contar o numero de bytes no momento que bater em um \0,
 
    }

    pthread_exit(EXIT_SUCCESS);
}

int main(int argc, char **argv)
{

    struct sockaddr_storage storage;
    if (0 != addrparse(argv[1], argv[2], &storage))
    {
        printf("falha storage parse");
    }

    int s;
    s = socket(storage.ss_family, SOCK_STREAM, 0);
    if (s == -1)
    {
        logexit("socket");
    } 

    struct sockaddr *addr = (struct sockaddr *)(&storage); //"um pointer pra estrutura de endereço que o socket possa usar"

    if (0 != connect(s, addr, sizeof(storage))) //conecta o socket criado com o endereço/porta apontado pelo addr
    {
        logexit("connect");
    }

    char addrstr[BUFSZ]; // Só armazena o endereço em formato de leitura humana
    addrtostr(addr, addrstr, BUFSZ);
    // Porque não utilizar o endereço recebido no argv?
    //Bem, acredito que o pattern aqui é ter essa função addrstr que faz o caminho de volta (isto eh, pega o addr que o socket ta usando e passa de volta pra string legivel)..
    // ... permite ao programador ter certeza de que o que foi entendido pelas funções que utilizaram a entrada argv de fato é o que se esperava..
    //.. Se utilizase direto do argv estaria meio que trapacendo, existiria a chance de que o sockets e afins estão usando outro algo que não o endereço recebido como parametro pro programa..,
    //... Isso é particularmente importante à medida que a camada de rede vai ficando mais densa com traduções de endereços, nics virtuais, offloads de network (em hardware dedicados para manejo da rede por ex)

    printf("connected to %s\n", addrstr);
    pthread_t tid_receive;
    pthread_create(&tid_receive, NULL, client_receive_thread, &s);

    pthread_t tid_send;
    pthread_create(&tid_send, NULL, client_send_thread, &s);

    pthread_join(tid_receive, NULL) ;

    pthread_cancel(tid_send); //Como a thread receive retornou, a conexão foi interrompida pelo servido dai basta cancelar a send tambem

    close(s);

    exit(EXIT_SUCCESS);
}
