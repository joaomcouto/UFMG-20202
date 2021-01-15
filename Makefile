all:
	g++ -Wall -c utils.cpp 
	g++ -Wall client.cpp utils.o -o client
	g++ -Wall server.cpp utils.o -o server 
	g++ -Wall -pthread server-mt.cpp utils.o -o server-mt 