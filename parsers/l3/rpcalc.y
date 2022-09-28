%{
#include <stdio.h>
#include <gmp.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include "rpcalc.h"

int yylex(void);
void yyerror(const char*);
 
struct solelem {
 char op;
 int num;
 int isop;
};

struct solelem* rpnform = NULL;
size_t rpnlen;
size_t rpnidx;

int appendvalrpn(int val){
    rpnform[rpnidx].isop = 0;
    rpnform[rpnidx].num = val;
    rpnlen += 1;
    rpnidx += 1;
    rpnform = realloc(rpnform, sizeof(struct solelem)*rpnlen);
    return rpnidx-1;
}

void appendoprpn(char op){
    rpnform[rpnidx].isop = 1;
    rpnform[rpnidx].op = op;
    rpnlen += 1;
    rpnidx += 1;
    rpnform = realloc(rpnform, sizeof(struct solelem)*rpnlen);
}

void resetrpn(){
    rpnlen = 30;
    rpnidx = 0;
    rpnform = realloc(rpnform, sizeof(struct solelem)*rpnlen);
}

void printrpn(){
    for (size_t elemidx = 0; elemidx < rpnidx; elemidx++){
        if (rpnform[elemidx].isop == 1){
            printf("%c ", rpnform[elemidx].op);
        } else {
            printf("%d ", rpnform[elemidx].num);
        }
    }
}

void add(mpz_t target, mpz_t a, mpz_t b){
    appendoprpn('+');
    mpz_init(target);
    mpz_add(target, a, b);
    mpz_clear(a);
    mpz_clear(b);
}
void substract(mpz_t target, mpz_t a, mpz_t b){
    appendoprpn('-');
    mpz_init(target);
    mpz_sub(target, a, b);
    mpz_clear(a);
    mpz_clear(b);
}
void multiply(mpz_t target, mpz_t a, mpz_t b){
    appendoprpn('*');
    mpz_init(target);
    mpz_mul(target, a, b);
    mpz_clear(a);
    mpz_clear(b);
}
void divide(mpz_t target, mpz_t a, mpz_t b, int mb){
    appendoprpn('/');
    mpz_init(target);

    mpz_t modbase;
    mpz_init(modbase);
    mpz_set_ui(modbase, mb);
    
    mpz_invert(b, b, modbase);
    mpz_mul(target, a, b);
    
    mpz_clear(a);
    mpz_clear(b);
    mpz_clear(modbase);
}
void negate(mpz_t target, mpz_t victim){
    mpz_init(target);
    mpz_neg(target, victim);
    mpz_clear(victim);
}

void power(mpz_t target, mpz_t a, mpz_t b, int mb){
    appendoprpn('^');

    mpz_init(target);

    mpz_t modbase;
    mpz_init(modbase);
    mpz_set_ui(modbase, mb);
    
    mpz_powm(target, a, b, modbase);

    mpz_clear(a);
    mpz_clear(b);
    mpz_clear(modbase);
}

void copy(mpz_t target, mpz_t victim){
    mpz_init(target);
    mpz_set(target, victim);
    mpz_clear(victim);
}

int getinteger(mpz_t victim){
    mpz_mod_ui(victim, victim, modn);
    int res = mpz_get_si(victim);
    mpz_clear(victim);
    return res;
}
 
void ats(struct BigInt* val, int modbase){
    if (val->depth == 0){
        mpz_t temp;
        mpz_init(temp);
        mpz_mod_ui(temp, val->i, modbase);
        rpnform[val->reftorpn].num = mpz_get_si(temp);
        mpz_clear(temp);
    }
}

void handleminus(int dep){
    if (dep != 0){
        appendoprpn('~');
    }
}
 
%}

%code requires {
 #include <gmp.h>
 #include "rpcalc.h"
}

%union {
 char* strval;
 int rnum;
 struct BigInt bnum;
}


%define parse.error detailed
%token NUM
%type <bnum> NUM exp expwykl


%left '-' '+'
%left '*' '/'
%precedence NEG
%nonassoc '^'

%%

input:
  %empty
| input line
;

line:
  '\n'
| exp '\n' { ats(&$1, modn); printrpn(); printf("\nWynik: %d\n", getinteger($1.i)); resetrpn();}
| error '\n' {yyerrok; resetrpn();}
;

exp:
  NUM { copy($$.i,$1.i); $$.reftorpn = appendvalrpn(mpz_get_si($$.i)); $$.depth = 0;}
| exp '+' exp { ats(&$1, modn); ats(&$3, modn); add($$.i,$1.i,$3.i); $$.depth = 1;}
| exp '-' exp { ats(&$1, modn); ats(&$3, modn); substract($$.i,$1.i,$3.i); $$.depth = 1;}
| exp '*' exp { ats(&$1, modn); ats(&$3, modn); multiply($$.i,$1.i,$3.i); $$.depth = 1; }
| exp '/' exp { ats(&$1, modn); ats(&$3, modn); divide($$.i,$1.i,$3.i, modn); $$.depth = 1;}
| exp '^' expwykl { ats(&$1, modn); ats(&$3, modn-1); power($$.i,$1.i,$3.i, modn); $$.depth = 1;}
| '(' exp ')' { ats(&$2, modn); copy($$.i, $2.i); $$.depth = 1;}
| '-' exp %prec NEG { negate($$.i, $2.i); $$.reftorpn = $2.reftorpn; $$.depth = $2.depth; handleminus($$.depth);}
;

expwykl:
  NUM { copy($$.i,$1.i); $$.reftorpn = appendvalrpn(mpz_get_si($$.i)); $$.depth = 0;}
| expwykl '+' expwykl { ats(&$1, modn-1); ats(&$3, modn-1); add($$.i,$1.i,$3.i); $$.depth = 1;}
| expwykl '-' expwykl { ats(&$1, modn-1); ats(&$3, modn-1); substract($$.i,$1.i,$3.i); $$.depth = 1;}
| expwykl '*' expwykl { ats(&$1, modn-1); ats(&$3, modn-1); multiply($$.i,$1.i,$3.i); $$.depth = 1; }
| expwykl '/' expwykl { ats(&$1, modn-1); ats(&$3, modn-1); divide($$.i,$1.i,$3.i, modn-1); $$.depth = 1;}
| '(' expwykl ')' { ats(&$2, modn-1); copy($$.i, $2.i); $$.depth = 1;}
| '-' expwykl %prec NEG { negate($$.i, $2.i); $$.reftorpn = $2.reftorpn; $$.depth = $2.depth; handleminus($$.depth);}
;

%%

void yyerror(const char* s){
    printf("Błąd.\n");
}

int main(){
    resetrpn();
    yyparse();
    free(rpnform);
    return 0;
}
