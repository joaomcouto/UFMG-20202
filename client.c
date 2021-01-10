#include "utils.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h> 
#include <sys/types.h>
#include <unistd.h>
#include <arpa/inet.h>


#define BUFSZ 1024

int main(int argc, char **argv){
    

    struct sockaddr_storage storage;
    if(0!= addrparse(argv[1], argv[2], &storage)){
        printf("deu pau no storage parse") ;
    }

    int s;
    s = socket(storage.ss_family, SOCK_STREAM, 0);
    if (s == -1){
        logexit("socket");
    } //verifica retorno das funções

    struct sockaddr *addr = (struct sockaddr *)(&storage) ;

    if (0 != connect(s, addr, sizeof(storage))){
        logexit("connect");
    } 
    
    char addrstr[BUFSZ];
    addrtostr(addr, addrstr, BUFSZ);

    printf("connected to %s\n",addrstr);

    char buf[BUFSZ];
    memset(buf, 0, BUFSZ);
    printf("mensagem> ");
    fgets(buf, BUFSZ-1, stdin);
    size_t count = send(s, buf, strlen(buf)+1,0 ); //+1 eh pq do \0


    if (count != (strlen(buf)+1)){
        logexit("send");
    }

     //printf("AAAAAAAAAAAAAAA ") ; 
    

    memset(buf, 0, BUFSZ);
    unsigned total = 0 ;
    while(1){
        count = recv(s, buf + total, BUFSZ - total, 0) ;
        if(count == 0){ //implies connection termination
            break ; 
        } 
        total += count; 
    }
    close(s);
    printf("Received %u bytes \n", total) ; 
    puts(buf) ;

    exit(EXIT_SUCCESS) ;
}
