#include "hamming.h"
#include <stdio.h>

int main(){
    for (int i = 0; i < 16; i++){
        printf("%d %d\n", hencode(i), hdecode(hencode(i)));
    }
}
