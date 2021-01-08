#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h> 
#include <sys/types.h>
#include <unistd.h>


void logexit(const char *msg){
    perror(msg);
    exit(EXIT_FAILURE);
}

#define BUFSZ 1024

void main(int arc, char **argv){
    int s;
    s = socket(AF_INET, SOCK_STREAM, 0);
    if (s = -1){
        logexit("socket");
    } //verifica retorno das funções

    if (0 != connect(s, addr, sizeof(addr))){
        logexit("connect");
    } 
    char addrstr[BUFSZ];

    addrtostr(addr, addstr, BUFSZ);

    printf("connected to %s\n");

    char buf[BUFSZ]);
    memset(buf, 0, BUFSZ);
    printf("mensagem> ");
    fgets(buf, BUFSZ-1, stdin);
    int count = send(s, buf, strlen(buf)+1,0 ); //+1 eh pq do \0

    if (count != strlen(buf+1)){
        logexit("send");
    }


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

    exit(EXIT_SUCCESS)
}
