%{
#include <stdbool.h>
#include <string.h>

bool doc_enabled = false;
bool print_comment = false;

bool in_preproc = false;
%}

%x multiline
%x singleline
%x stringliteral
%x pathliteral


%%
<pathliteral,stringliteral>\\\n ECHO;
<singleline,multiline>\\\n if(print_comment){ECHO;}
<pathliteral,stringliteral,singleline>\n ECHO; in_preproc = false; BEGIN(0); print_comment = false;
^[ \t]*"#" in_preproc = true; ECHO;
"<" { ECHO; if(in_preproc){BEGIN(pathliteral);}}
<pathliteral>">" ECHO; BEGIN(0);
\" ECHO; BEGIN(stringliteral);
<stringliteral>\" ECHO; BEGIN(0);
"/"(\\\n)*"/"(\\\n)*"/" BEGIN(singleline); if (doc_enabled){ ECHO; print_comment = true; }
"/"(\\\n)*"/"(\\\n)*"!" BEGIN(singleline); if (doc_enabled){ ECHO; print_comment = true; }
"/"(\\\n)*"/" BEGIN(singleline);
<singleline>. if(print_comment){ECHO;}
"/"(\\\n)*"*"(\\\n)*"*" BEGIN(multiline); if (doc_enabled){ECHO; print_comment = true; }
"/"(\\\n)*"*"(\\\n)*"!" BEGIN(multiline); if (doc_enabled){ECHO; print_comment = true; }
"/"(\\\n)*"*" BEGIN(multiline);
<multiline>"*"(\\\n)*"/" if(print_comment){ECHO;} BEGIN(0); print_comment = false;
<multiline>.|(\n) if(print_comment){ECHO;} in_preproc = false;
\n ECHO; in_preproc = false;
%%

int main(int argc, char** argv){
    if (argc > 1){
        if (argc > 2){
            if (strcmp(argv[2], "--keepdoc") == 0){
                doc_enabled = true;
            }
        }
        yyin = fopen(argv[1], "r" );
        yylex();
    }
}
