#include <stdlib.h>
#include <stdio.h>
#include <arpa/inet.h>
#include <string.h>

extern void logexit(const char *msg){
    perror(msg);
    exit(EXIT_FAILURE);
}


extern int addrparse(const char *addrstr, const char *portstr, struct sockaddr_storage *storage){
    if (addrstr == NULL || portstr == NULL){
        return -1 ;
    }

    uint16_t port = (uint16_t)atoi(portstr);
    
    if (port == 0 ){
        return -1 ;
    }

    port = htons(port); //prepara o port para um formato usavel em rede (search later: "endian")


    struct in_addr inaddr4 ; //32-bit ip addr
    if(inet_pton(AF_INET, addrstr, &inaddr4)){ //Converte a string com o ip de addrtstr e converte pra struct tipo in_addrt em binario e poe no inaddrt4 que tem que ser sizeof(in_addr)
        struct sockaddr_in * addr4 = (struct sockaddr_in *) storage;
        addr4->sin_family = AF_INET;
        addr4->sin_port = port;
        addr4->sin_addr = inaddr4 ;
        return 0;
    }

    struct in6_addr inaddr6 ; //128-bit ip addr
    if(inet_pton(AF_INET6, addrstr, &inaddr6)){
        struct sockaddr_in6 * addr6 = (struct sockaddr_in6 *) storage;
        addr6->sin6_family = AF_INET6;
        addr6->sin6_port = port;
        memcpy(&(addr6->sin6_addr), &inaddr6, sizeof(inaddr6)) ;
        return 0;
    }

    return -1;

}

extern void addrtostr (const struct sockaddr * addr , char * str, size_t strsize){
    int version;
    char addrstr[INET6_ADDRSTRLEN+1] = "";
    uint16_t port ;

    if(addr->sa_family == AF_INET){
        version = 4;
        struct sockaddr_in * addr4 = (struct sockaddr_in *) addr;
        if(!inet_ntop(AF_INET, &(addr4->sin_addr), addrstr, INET_ADDRSTRLEN+1 )){ //Converte o endereço em binario que esta em addr para formato de leitura humano e poe na string addrstr
            logexit("ntop") ;
        }
        port = ntohs(addr4->sin_port); //network to host short
    } else if (addr->sa_family == AF_INET6){
        version = 6;
        struct sockaddr_in6 * addr6 = (struct sockaddr_in6 *) addr;
        if(!inet_ntop(AF_INET6, &(addr6->sin6_addr), addrstr, INET_ADDRSTRLEN+1 )){
            logexit("ntop") ;
        }
        port = ntohs(addr6->sin6_port); //network to host short

    }  else {
        logexit("unknown protocol family") ;
    }
    if(str){
        snprintf(str, strsize,"IPV%d %s %hu", version, addrstr, port);
    }
}

//extern int server_sockaddr_init(const char *proto, const char *portstr, struct sockaddr_storage * storage){
extern int server_sockaddr_init( const char *portstr, struct sockaddr_storage * storage){
    uint16_t port = (uint16_t)atoi(portstr);
    
    if (port == 0 ){
        return -1 ;
    }
    port = htons(port);

    memset(storage, 0, sizeof(*storage)) ;

    //if (0 == strcmp(proto, "v4")){
    struct sockaddr_in * addr4 = (struct sockaddr_in *) storage;
    addr4->sin_family = AF_INET;
    addr4->sin_addr.s_addr = INADDR_ANY ; //Se colocasse 127.0.0.1 aqui significaria que apenas 
    addr4->sin_port = port;

    return 0;

    //} else if (0 == strcmp(proto, "v6")){
    //    struct sockaddr_in6 * addr6 = (struct sockaddr_in6 *) storage;
     //   addr6->sin6_family = AF_INET6;
     //   addr6->sin6_addr = in6addr_any ;
      //  addr6->sin6_port = port;

      //  return 0;

    //} else {
       // return -1 ;
    //}
}
