all:
	nasm -f elf ./zad1.asm
	ld -m elf_i386 ./zad1.o -o ./zad1
	nasm -f elf ./zad2.asm
	ld -m elf_i386 ./zad2.o -o ./zad2
	nasm -f elf ./zad3.asm
	ld -m elf_i386 ./zad3.o -o ./zad3
	nasm -f elf ./zad7.asm
	ld -m elf_i386 ./zad7.o -o ./zad7
	gcc -masm=intel -O2 zad6.c `sdl-config --cflags --libs` -lSDL_image -o ./zad6
