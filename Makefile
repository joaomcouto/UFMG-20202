all:
	gcc -Wall -c utils.c 
	gcc -Wall client.c utils.o -o client
	gcc -Wall server.c utils.o -o server