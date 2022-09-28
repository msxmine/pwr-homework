all:
	gcc -Wall lbgcluster.c -o lbgcluster.o -c
	gcc -Wall tgaread.c -o tgaread.o -c
	gcc -Wall tgawrite.c -o tgawrite.o -c
	gcc -Wall lab.c -o lab.o -c
	gcc -Wall -o lab lab.o tgaread.o lbgcluster.o tgawrite.o -lm
