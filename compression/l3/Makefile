all:
	gcc -Wall lzw.c -o lzw.o -c
	gcc -Wall universal.c -o universal.o -c
	gcc -Wall fileio.c -o fileio.o -c
	gcc -Wall decompress.c -o decompress.o -c
	gcc -Wall -o decompress lzw.o universal.o fileio.o decompress.o
	gcc -Wall entropystats.c -o entropystats.o -c
	gcc -Wall compress.c -o compress.o -c
	gcc -Wall -o compress lzw.o universal.o fileio.o entropystats.o compress.o -lm
