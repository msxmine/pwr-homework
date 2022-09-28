all:
	gcc -Wall hamming.c -o hamming.o -c
	gcc -Wall coder.c -o coder.o -c
	gcc -Wall decoder.c -o decoder.o -c
	gcc -Wall test.c -o test.o -c
	gcc -Wall noise.c -o noise.o -c
	gcc -Wall check.c -o check.o -c
	gcc -Wall -o coder hamming.o coder.o
	gcc -Wall -o decoder hamming.o decoder.o
	gcc -Wall -o test hamming.o test.o
	gcc -Wall -o noise noise.o
	gcc -Wall -o check check.o
