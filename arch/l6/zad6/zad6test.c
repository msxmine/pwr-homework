#include <unistd.h>
#include <stdio.h>

int main(){
	int tes = syscall(456);
	printf("%d\n", tes);
	return 0;
}
