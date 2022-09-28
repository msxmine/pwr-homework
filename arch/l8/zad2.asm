section .data
endline db 10
space db ' '
symb db '01'
digits dd 0,0,0,0,0,11

section .text
global _start

_start:
mov esi, digits
add esi, 20
mov edi, 10 ; Do dzielenia przez 10

mov edx, 0
mov eax, 9234 ; Liczba do wyswietlenia
divloop:
cmp eax, 0
jz endloop
div edi
sub esi, 4
mov [esi], edx
mov edx, 0
jmp divloop
endloop:

digitsloop:
mov edi, [esi]
add esi, 4
push esi

cmp edi, 11
jz alldigits

ror edi, 3
mov esi, 4


onesloop:
cmp esi, 0
jz allones
mov ecx, edi
and ecx, 1
add ecx, symb
mov edx, 1
mov ebx, 1
mov eax, 4
int 80h
sub esi, 1
rol edi, 1
jmp onesloop
allones:
mov ecx, space
mov edx, 1
mov ebx, 1
mov eax, 4
int 80h

pop esi
jmp digitsloop

alldigits:
mov ecx, endline
mov edx, 1
mov ebx, 1
mov eax, 4
int 80h

mov ebx, 0
mov eax, 1
int 80h
