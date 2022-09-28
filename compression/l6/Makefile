all:
	gcc -Wall coding.c -o coding.o -c
	gcc -Wall tgaread.c -o tgaread.o -c
	gcc -Wall tgawrite.c -o tgawrite.o -c
	gcc -Wall quantfile.c -o quantfile.o -c
	gcc -Wall coder.c -o coder.o -c
	gcc -Wall decoder.c -o decoder.o -c
	gcc -Wall tester.c -o tester.o -c
	gcc -Wall -o coder coder.o tgaread.o coding.o tgawrite.o quantfile.o -lm
	gcc -Wall -o decoder decoder.o tgaread.o coding.o tgawrite.o quantfile.o -lm 
	gcc -Wall -o tester tester.o tgaread.o coding.o tgawrite.o quantfile.o -lm 
