section .data
newline db 10
symbols db '0123456789abcdef'

section .text
global _start

_start:

mov edi, 200 ; Liczba do wyswietlenia

ror edi, 4
mov esi, edi
and esi, 0xf
add esi, symbols
mov edx, 1 ; Len 1 
mov ecx, esi
mov ebx, 1 ; FD 1 - STDOUT
mov eax, 4 ; Syscall 4 - write()
int 80h
rol edi, 4
mov esi, edi
and esi, 0xf
add esi, symbols
mov edx, 1 ; Len 1 
mov ecx, esi
mov ebx, 1 ; FD 1 - STDOUT
mov eax, 4 ; Syscall 4 - write()
int 80h
mov edx, 1 ; Len 1 
mov ecx, newline
mov ebx, 1 ; FD 1 - STDOUT
mov eax, 4 ; Syscall 4 - write()
int 80h


mov ebx, 0
mov eax, 1
int 80h
