section .data
newline db 10
numbers dd 0,0,0,0,0,0,0,0
symbols db '0123456789abcdef'

section .text
global _start

atoi:
mov eax, 0
atoi_convert:
movzx esi, byte [edi]
cmp esi, 0
je atoi_exit
sub esi, '0'
imul eax, 10
add eax, esi
inc edi
jmp atoi_convert
atoi_exit:
ret

printreg:
mov esi, 8
rol edi, 4
reglp:
cmp esi, 0
jz endpr
mov ecx, edi
and ecx, 0xf
add ecx, symbols
mov edx, 1
mov ebx, 1
mov eax, 4
int 80h
dec esi
rol edi, 4
jmp reglp
endpr:
ret


_start:
cmp dword [esp], 2
jnz exit
mov edi, [esp+8]
call atoi


mov dword [numbers], 1
movd xmm1, [numbers] ; result

mulloop:
cmp eax, 0
jz calcdone

mov [numbers], eax
movd xmm0, [numbers] ; current num

;(a1*b4), (a2*b3)
pshufd xmm2, xmm0, 11111010b
pshufd xmm3, xmm1, 00000101b
pmuludq xmm2, xmm3
pxor xmm3, xmm3
movsd xmm3, xmm2
pshufd xmm2, xmm2, 11101110b
paddq xmm3, xmm2
movsd xmm4, xmm3

pshufd xmm2, xmm0, 01010000b
pshufd xmm3, xmm1, 10101111b
pmuludq xmm2, xmm3
pxor xmm3, xmm3
movsd xmm3, xmm2
pshufd xmm2, xmm2, 11101110b
paddq xmm3, xmm2
paddq xmm4, xmm3

pshufd xmm4, xmm4, 00000000b
pxor xmm5, xmm5
movsd xmm5, xmm4
pshufd xmm5, xmm5, 11100011b

pshufd xmm2, xmm0, 10100101b
pshufd xmm3, xmm1, 00000101b
pmuludq xmm2, xmm3
pxor xmm3, xmm3
movsd xmm3, xmm2
pshufd xmm2, xmm2, 11101110b
paddq xmm3, xmm2
movsd xmm4, xmm3

pshufd xmm2, xmm0, 00000000b
pshufd xmm3, xmm1, 10101010b
pmuludq xmm2, xmm3
paddq xmm4, xmm2

pxor xmm3, xmm3
movsd xmm3, xmm4
paddq xmm5, xmm3
pshufd xmm5, xmm5, 01001111b


pshufd xmm2, xmm0, 00000000b
pshufd xmm3, xmm1, 00000000b
pmuludq xmm2, xmm3
pxor xmm4, xmm4
movsd xmm4, xmm2
pshufd xmm4, xmm4, 11011100b
movsd xmm5, xmm4
pshufd xmm4, xmm4, 11111110b
pxor xmm6, xmm6
movsd xmm6, xmm4

pshufd xmm2, xmm0, 01010000b
pshufd xmm3, xmm1, 00000101b
pmuludq xmm2, xmm3
pxor xmm3, xmm3
movsd xmm3, xmm2
pshufd xmm3, xmm3, 11011100b
pshufd xmm2, xmm2, 01001110b
pxor xmm4, xmm4
movsd xmm4, xmm2
pshufd xmm4, xmm4, 11011100b
paddq xmm4, xmm3
paddq xmm4, xmm6

pxor xmm2, xmm2
pxor xmm3, xmm3
pxor xmm6, xmm6

movsd xmm2, xmm4
pshufd xmm2, xmm2, 11011111b
paddq xmm4, xmm2

pxor xmm2, xmm2
movsd xmm2, xmm4
pshufd xmm2, xmm2, 11110011b
movsd xmm4, xmm2
paddq xmm5, xmm4

movdqa xmm1, xmm5
dec eax
jmp mulloop

calcdone:
movdqa xmm2, xmm1
pshufd xmm2, xmm2, 00011011b
movd edi, xmm2
call printreg
pshufd xmm2, xmm2, 00111001b
movd edi, xmm2
call printreg
pshufd xmm2, xmm2, 00111001b
movd edi, xmm2
call printreg
pshufd xmm2, xmm2, 00111001b
movd edi, xmm2
call printreg

mov edx, 1 ; Len 1 
mov ecx, newline
mov ebx, 1 ; FD 1 - STDOUT
mov eax, 4 ; Syscall 4 - write()
int 80h

exit:
mov ebx, 0
mov eax, 1
int 80h
