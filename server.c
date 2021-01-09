#include "utils.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h> 
#include <sys/types.h>
#include <unistd.h>


#define BUFSZ 1024

int main(int argc, char ** argv){

    struct sockaddr_storage storage;
    if(0!= server_sockaddr_init(argv[1], argv[2], &storage)){
        printf("deu pau no storage parse") ;
    }

    int s;
    s = socket(storage.ss_family, SOCK_STREAM, 0);
    if (s == -1){
        logexit("socket");
    } //verifica retorno das funções

    struct sockaddr *addr = (struct sockaddr *)(&storage) ;
    if (0 != bind(s,addr, sizeof(storage))){
        logexit("bind") ;
    }

    if (0 != listen (s, 10)){
        logexit("listen") ;
    }

    char addrstr[BUFSZ];
    addrtostr(addr, addrstr, BUFSZ);
    printf("bound to %s, waiting connection \n", addrstr);

    while(1){
        struct sockaddr_storage cstorage;
        struct sockaddr *caddr = (struct sockaddr *)(&cstorage) ;
        socklen_t caddrlen  = sizeof(cstorage) ; 

        int csock = accept( s, caddr, &caddrlen) ; 

        if(csock == -1){
            logexit("accept") ;
        } 

        char caddrstr[BUFSZ];
        addrtostr(caddr, caddrstr, BUFSZ);
        printf("[log] connection from %s\n", caddrstr);

        char buf[BUFSZ];
        memset(buf, 0 , BUFSZ);
        size_t count = recv(csock, buf, BUFSZ, 0) ;
        printf("[msg] %s, %d bytes: %s \n", caddrstr, (int) count, buf) ; 

        sprintf(buf, "remote endpoint: %.1000s\n", caddrstr) ; 
        count = send(csock, buf , strlen(buf)+1, 0 );
        if (count != strlen(buf+1)){
            logexit("send");
        }
        close(csock) ;
    }

    exit(EXIT_SUCCESS) ;
    
}