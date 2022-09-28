import ply.lex as lex
import ply.yacc as yacc

class LexingError(Exception):
    pass

class NothingToParseError(Exception):
    pass

class ParserError(Exception):
    pass

modn = 1234577

tokens = (
    'NUM',
)

literals = ['+','-','*','/','^','(',')']

def t_comment(t):
    r'^\#.*'
    pass

def t_whitespace(t):
    r'[ \t]+'
    pass

def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value, 10)
    return t

def t_error(t):
    raise LexingError


precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('nonassoc', '^'),
)

def hmi(ddic, modul):
    if ddic["depth"] == 0:
        rpnline[ddic["numidx"]] = str(ddic["val"]%modul)

def p_resultp_empty(p):
    'resultp : empty'
    raise NothingToParseError

def p_resultp_full(p):
    'resultp : exp'
    p[0] = p[1]
    hmi(p[0], modn)

def p_exp_num(p):
    'exp : NUM'
    p[0] = {"val": p[1], "depth": 0, "numidx": len(rpnline)}
    rpnline.append(str(p[1]))

def p_exp_plus(p):
    '''exp : exp '+' exp '''
    rpnline.append("+")
    hmi(p[1], modn)
    hmi(p[3], modn)
    p[0] = {"val": p[1]["val"] + p[3]["val"], "depth": 1}

def p_exp_sub(p):
    '''exp : exp '-' exp '''
    rpnline.append("-")
    hmi(p[1], modn)
    hmi(p[3], modn)
    p[0] = {"val": p[1]["val"] - p[3]["val"], "depth": 1}

def p_exp_mul(p):
    '''exp : exp '*' exp '''
    rpnline.append("*")
    hmi(p[1], modn)
    hmi(p[3], modn)
    p[0] = {"val": p[1]["val"] * p[3]["val"], "depth": 1}

def p_exp_div(p):
    '''exp : exp '/' exp '''
    rpnline.append("/")
    hmi(p[1], modn)
    hmi(p[3], modn)
    p[0] = {"val": p[1]["val"] * pow(p[3]["val"],-1,modn), "depth": 1}

def p_exp_pow(p):
    '''exp : exp '^' expexp'''
    rpnline.append("^")
    hmi(p[1], modn)
    hmi(p[3], modn-1)
    p[0] = {"val": pow(p[1]["val"],p[3]["val"],modn), "depth": 1}

def p_exp_prio(p):
    '''exp : '(' exp ')' '''
    hmi(p[2], modn)
    p[0] = {"val": p[2]["val"], "depth": 1}

def p_exp_unarymin(p):
    '''exp : '-' exp %prec UMINUS'''
    if p[2]["depth"] == 0:
        p[0] = {"val": -p[2]["val"], "depth": 0, "numidx": p[2]["numidx"]}
    else:
        rpnline.append("~")
        p[0] = {"val": -p[2]["val"], "depth": 1}
######
def p_expexp_num(p):
    'expexp : NUM'
    p[0] = {"val": p[1], "depth": 0, "numidx": len(rpnline)}
    rpnline.append(str(p[1]))

def p_expexp_plus(p):
    '''expexp : expexp '+' expexp '''
    rpnline.append("+")
    hmi(p[1], modn-1)
    hmi(p[3], modn-1)
    p[0] = {"val": p[1]["val"] + p[3]["val"], "depth": 1}

def p_expexp_sub(p):
    '''expexp : expexp '-' expexp '''
    rpnline.append("-")
    hmi(p[1], modn-1)
    hmi(p[3], modn-1)
    p[0] = {"val": p[1]["val"] - p[3]["val"], "depth": 1}

def p_expexp_mul(p):
    '''expexp : expexp '*' expexp '''
    rpnline.append("*")
    hmi(p[1], modn-1)
    hmi(p[3], modn-1)
    p[0] = {"val": p[1]["val"] * p[3]["val"], "depth": 1}

def p_expexp_div(p):
    '''expexp : expexp '/' expexp '''
    rpnline.append("/")
    hmi(p[1], modn-1)
    hmi(p[3], modn-1)
    p[0] = {"val": p[1]["val"] * pow(p[3]["val"],-1,modn-1), "depth": 1}

def p_expexp_prio(p):
    '''expexp : '(' expexp ')' '''
    hmi(p[2], modn-1)
    p[0] = {"val": p[2]["val"], "depth": 1}

def p_expexp_unarymin(p):
    '''expexp : '-' expexp %prec UMINUS'''
    if p[2]["depth"] == 0:
        p[0] = {"val": -p[2]["val"], "depth": 0, "numidx": p[2]["numidx"]}
    else:
        rpnline.append("~")
        p[0] = {"val": -p[2]["val"], "depth": 1}
######

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    raise ParserError

lex.lex()
yacc.yacc()

processing = True
while processing:
    inputtxt = ""
    while True:
        try:
            inputtxt += input()
            if inputtxt.endswith('\\'):
                inputtxt = inputtxt[:-1]
            else:
                break
        except EOFError:
            processing = False
            break
    rpnline = []
    try:
        results = yacc.parse(inputtxt)
        print(" ".join(rpnline))
        print("Wynik:", results["val"]%modn)
    except NothingToParseError:
        pass
    except ParserError:
        print("Błąd.")
    except LexingError:
        print("Błąd.")
