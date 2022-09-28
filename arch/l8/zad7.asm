section .data
xa dq 123.45
xb dq 13.8
xc dq 12.1
xd dq 168.4

section .text
global _start

calca:
fld1
fxch
fyl2x
fldl2e
fdivp
ret

calcb:
fldl2e
fmulp ; log_2(e^x)
fld1
fscale ; 2 ^ INT(log_2(e^x))
fxch
fld1
fxch
fprem ; FRAC(log_2(e^x))
f2xm1 ; 2 ^ FRAC(log_2(e^x)) - 1
faddp ; 2 ^ FRAC(log_2(e^x))
fmulp ; e^x
ret

calcc:
fld st0
call calcb
fxch
fldz
fxch
fsubp
call calcb
fsubp
fld1
fld1
faddp
fdivp
ret

calcd:
fld st0
fmul st0, st1
fld1
faddp
fsqrt
faddp
call calca
ret


_start:

fld qword [xa]
call calca
fstp qword [xa]

fld qword [xb]
call calcb
fstp qword [xb]

fld qword [xc]
call calcc
fstp qword [xc]

fld qword [xd]
call calcd
fstp qword [xd]

exit:

mov ebx, 0
mov eax, 1
int 80h
