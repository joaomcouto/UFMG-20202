#include "utils.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFSZ 1024

int main(int argc, char **argv)
{

    struct sockaddr_storage storage;
    if (0 != addrparse(argv[1], argv[2], &storage))
    {
        printf("deu pau no storage parse");
    }

    int s;
    s = socket(storage.ss_family, SOCK_STREAM, 0);
    if (s == -1)
    {
        logexit("socket");
    } //verifica retorno das funções

    struct sockaddr *addr = (struct sockaddr *)(&storage); //"Só um pointer pra estrutura de enreço pro socket usar"

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

    char buf[BUFSZ]; //Armazena a mensagem do usuario que sera mandada pela rede no send

    memset(buf, 0, BUFSZ);
    printf("mensagem> ");
    fgets(buf, BUFSZ - 1, stdin);
    size_t count = send(s, buf, strlen(buf) + 1, 0); //Send recebe o socket, o buffer e o tamanho maximo de leitura: necessario porque do contrario o send é interrompido com
    //size_t : tamanho maximo de endereços memória que depende do ambiente em que se pretende executa o programa, todavia isso é definido no momento de compilação
    //.. Então por exemplo, se estamos fazendo um programa pra rodar embarcado, deve-se cuidar para incluir headers que apropriadamente definam o ambiente embarco, inlucindo a definição do size_t
    // ...
    //O terceiro parametro de send é simplesmente o numero de bytes que ele deve ler no local apontado pelo pointer no segundo parametro
    //O strlen para de contar o numero de bytes no momento que bater em um \0,

    if (count != (strlen(buf) + 1))
    {
        logexit("send");
    }

    //printf("AAAAAAAAAAAAAAA ") ;

    memset(buf, 0, BUFSZ);
    unsigned total = 0;
    //unsigned: na ausencia de int, é entendido como unsigned int por default
    while (1)
    {
        count = recv(s, buf + total, BUFSZ - total, 0);
        //Buf + total esta simplesmente deslocando o local (adicionando um delta em relacao ao local apontando pelo ponteiro buf) em que o recv vai escrever a proxima parte ("pacote") da mensagem
        //... Alem disso reduzimos o numero de bytes maximo que ele deve receber do "pacote", pois o buf tem tamanho limitado BUFSZ
        // ... Assim se a mensagem tiver sido espalhada em multiplos "pacotes", só escrevemos o que ainda couber no buf

        if (count == 0)
        { //implies connection termination
            break;
        }
        total += count;
    }
    close(s);
    printf("Received %u bytes \n", total);
    puts(buf); //printa no stdout a mensagem salva no buffer pelo recv

    exit(EXIT_SUCCESS);
}
