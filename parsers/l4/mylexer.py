from sly import Lexer

class LexerError(Exception):
    pass

class MyLexer(Lexer):
    tokens = { "NUM", "PIDENTIFIER", 
    "EQ", "NEQ", "LE", "GE", "LEQ", "GEQ",
    "PLUS", "MINUS", "TIMES", "DIV", "MOD",
    "ASSIGN", "IF", "THEN", "ELSE", "ENDIF", "WHILE", "DO", "ENDWHILE", "REPEAT", "UNTIL", 
    "FOR", "FROM", "TO", "ENDFOR", "DOWNTO", "READ", "WRITE",
    "VAR", "BEGIN", "END"
    }
    literals = { ',', '[', ':', ']', ';'}

    ENDWHILE = r'ENDWHILE'
    ASSIGN = r'ASSIGN'
    REPEAT = r'REPEAT'
    ENDFOR = r'ENDFOR'
    DOWNTO = r'DOWNTO'
    MINUS = r'MINUS'
    TIMES = r'TIMES'
    ENDIF = r'ENDIF'
    WHILE = r'WHILE'
    UNTIL = r'UNTIL'
    WRITE = r'WRITE'
    BEGIN = r'BEGIN'
    PLUS = r'PLUS'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FROM = r'FROM'
    READ = r'READ'
    NEQ = r'NEQ'
    LEQ = r'LEQ'
    GEQ = r'GEQ'
    DIV = r'DIV'
    MOD = r'MOD'
    FOR = r'FOR'
    VAR = r'VAR'
    END = r'END'
    EQ = r'EQ'
    LE = r'LE'
    GE = r'GE'
    IF = r'IF'
    DO = r'DO'
    TO = r'TO'

    ignore = ' \t'
    ignore_comment = r'\([^)]*\)'

    PIDENTIFIER = r'[_a-z]+'

    @_(r'-?\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        raise LexerError("Błąd lexera:\nNieznany znak w linii %d : '%s'" % (self.lineno, t.value[0]))



