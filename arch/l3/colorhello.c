#include <stdio.h>

#define MESSAGE "Hello, World!"

int main(){
    //Podstawowe 16 kolorów
    for (int i = 0; i < 8; i++){
        printf("\x1b[0;%dm"MESSAGE"\n", i+30);
        printf("\x1b[0;%dm"MESSAGE"\n", i+90);
    }
    printf("\x1b[0m");
    //Rozszerzone 256 kolorów
    for (int i = 0; i < 256; i++){
        printf("\x1b[38;5;%dm"MESSAGE"\n", i);
    }
    //Truecolor RGB_888
    for (int red = 0; red < 256; red++){
    for (int green = 0; green < 256; green++){
    for (int blue = 0; blue < 256; blue++){
        printf("\x1b[38;2;%d;%d;%dm"MESSAGE"\n", red, green, blue);
    }
    }
    }
    return 0;
}

