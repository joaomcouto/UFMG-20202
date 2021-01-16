all:
	g++ -Wall -c utils.cpp 
	g++ -pthread -Wall client.cpp utils.o -o cliente
	#g++ -Wall server.cpp utils.o -o server 
	g++ -Wall -pthread server-mt.cpp utils.o -o servidor 