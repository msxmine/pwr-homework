%{
#include <stdlib.h>
#include "rpcalc.tab.h"
#include <gmp.h>

void readmod(char*, mpz_t);
%}

%%
^"#"(.*(\\\n)*)*[\n]
"\\"[\n]
[ \t]+
[0-9]+ { readmod(yytext, yylval.bnum.i); return NUM;}
.|\n { return yytext[0];}
%%

void readmod(char* strrep, mpz_t targetpointer){
    mpz_init(targetpointer);
    mpz_set_str(targetpointer, strrep, 10);
}
