#include <linux/kernel.h>
#include <linux/module.h>
#include <asm/unistd.h>

asmlinkage long hello_log(void){
	printk("Hello World!");
	return 0;
}
