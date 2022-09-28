%x markuptag
%x markupproc
%x cdata

%%
"<!--"(([^-])|(-[^-]))*"-->"
"<" ECHO;BEGIN(markuptag);
"<?" ECHO;BEGIN(markupproc);
"<![CDATA[" ECHO;BEGIN(cdata);
<markuptag,markupproc,cdata>\"[^\"]*\" ECHO;
<markuptag>">" ECHO;BEGIN(0);
<markupproc>"?>" ECHO;BEGIN(0);
<cdata>"]]>" ECHO;BEGIN(0);
<markuptag,markupproc,cdata>(.|\n) ECHO;
%%

int main(int argc, char** argv){
    if (argc > 1){
        yyin = fopen(argv[1], "r" );
        yylex();
    }
}
