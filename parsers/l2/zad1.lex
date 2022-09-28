
%{
int word_count = 0;
int line_count = 0;
%}

%%
^[ \t\r\v\f]+
[ \t\r\v\f]+ {
                char next = input();
                unput(next);
                if (next == EOF || next == 0){
                    yyterminate();
                }
                else if (next != '\n'){
                    REJECT;
                }
            }
[ \t]+  putchar(' ');
\n/[^\n]*[^ \t\r\v\f\n]+ line_count++; ECHO;
\n
[^ \t\r\v\f\n]+ word_count++; ECHO;
%%

int main(int argc, char** argv){
    if (argc > 1){
        yyin = fopen(argv[1], "r" );
        yylex();
        fprintf( stderr, "%d %d\n", line_count, word_count);
    }
}
