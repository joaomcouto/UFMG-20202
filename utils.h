#ifndef UTILS
#define UTILS

#include <stdlib.h>

#include <arpa/inet.h>

extern int addrparse(const char *addrstr, const char *portstr, struct sockaddr_storage *storage) ;
extern void addrtostr (const struct sockaddr * addr , char * str, size_t strsize) ;

//extern int server_sockaddr_init(const char *proto, const char *portstr, struct sockaddr_storage * storage) ;
extern int server_sockaddr_init( const char *portstr, struct sockaddr_storage * storage) ;
extern void logexit(const char *msg) ;

#endif