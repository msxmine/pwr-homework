%{
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

bool errored = false;
void push(int data);
int pop();
bool doop(char op);
void finish();
%}

%%
"-"{0,1}[0-9]+ push(strtol(yytext, NULL, 10));
[+\-*/^%] if (!errored){ errored = !doop(yytext[0]); }
[ \t]+
\n finish();
. printf("Nieznany symbol %s\n", yytext); errored = true;
%%

int stack[8000];
int slot = 0;

void push(int data){
    if(slot+1 < 8000){
        stack[slot] = data;
        slot++;
    }
}

int pop(){
    if (slot > 0){
        slot--;
        return stack[slot];
    }
    return 0;
}

bool doop(char op){
    if (slot < 2){
        fprintf(stderr, "Za mała liczba argumentow dla operatora %c\n", op);
        return false;
    }
    int argtwo = pop();
    int argone = pop();
    int result = 0;
    switch(op){
        case '+':
            result = argone + argtwo;
            break;
        case '-':
            result = argone - argtwo;
            break;
        case '*':
            result = argone * argtwo;
            break;
        case '^':
            if (argtwo < 0){
                fprintf(stderr, "Ujemne wykładniki nie są obsługiwane: %d ^ %d\n", argone, argtwo);
                return false;
            }
            result = lround(pow(argone,argtwo));
            break;
        case '/':
            if (argtwo == 0){
                fprintf(stderr, "Dzielenie przez 0\n");
                return false;
            }
            result = argone / argtwo;
            break;
        case '%':
            if (argtwo == 0){
                fprintf(stderr, "Dzielenie przez 0\n");
                return false;
            }
            result = argone % argtwo;
            break;
    }
    push(result);
    return true;
}

void finish(){
    if (!errored){
        if (slot != 1){
            fprintf(stderr, "Za mało operatorów, %d elementów na stosie\n", slot);
        }
        else {
            printf("= %d\n", pop());
        }
    }
    slot = 0;
    errored = false;
}

int main(int argc, char** argv){

        yylex();


}
