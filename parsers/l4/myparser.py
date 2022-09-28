from sly import Parser
from mylexer import MyLexer
import astdef

class ParserError(Exception):
    pass

class MyParser(Parser):
    tokens = MyLexer.tokens

    @_('VAR declarations BEGIN commands END')
    def program(self, p):
        myvars = astdef.VariableStore(p.declarations)
        mycommands = p.commands
        thisprog = astdef.Program(myvars, mycommands)
        thisprog.children = [myvars, mycommands]
        return thisprog

    @_('BEGIN commands END')
    def program(self, p):
        myvars = astdef.VariableStore([])
        mycommands = p.commands
        thisprog = astdef.Program(myvars, mycommands)
        thisprog.children = [myvars, mycommands]
        return thisprog
    

    @_('declarations "," PIDENTIFIER')
    def declarations(self, p):
        newvar = astdef.Variable(p.lineno, p.PIDENTIFIER)
        p.declarations.append(newvar)
        return p.declarations

    @_('declarations "," PIDENTIFIER "[" NUM ":" NUM "]"')
    def declarations(self, p):
        newvar = astdef.VariableArray(p.lineno, p.PIDENTIFIER, p.NUM0, p.NUM1)
        p.declarations.append(newvar)
        return p.declarations

    @_('PIDENTIFIER')
    def declarations(self, p):
        newdec = []
        newvar = astdef.Variable(p.lineno, p.PIDENTIFIER)
        newdec.append(newvar)
        return newdec

    @_('PIDENTIFIER "[" NUM ":" NUM "]"')
    def declarations(self, p):
        newdec = []
        newvar = astdef.VariableArray(p.lineno, p.PIDENTIFIER, p.NUM0, p.NUM1)
        newdec.append(newvar)
        return newdec
    
    @_('commands command')
    def commands(self, p):
        p.commands.append(p.command)
        return p.commands

    @_('command')
    def commands(self, p):
        newcommands = []
        newcommands.append(p.command)
        return newcommands

    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        cm = astdef.CommandAssign(p.lineno, p.identifier, p.expression)
        cm.children = [p.identifier, p.expression]
        return cm

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        cm = astdef.CommandIf(p.lineno, p.condition, p.commands0, p.commands1)
        cm.children = [p.condition, p.commands0, p.commands1]
        return cm

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        cm = astdef.CommandIf(p.lineno, p.condition, p.commands)
        cm.children = [p.condition, p.commands]
        return cm

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        cm = astdef.CommandWhile(p.lineno, p.condition, p.commands)
        cm.children = [p.condition, p.commands]
        return cm

    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):
        cm = astdef.CommandRepeat(p.lineno, p.condition, p.commands)
        cm.children = [p.condition, p.commands]
        return cm

    @_('FOR PIDENTIFIER FROM value TO value DO commands ENDFOR')
    def command(self, p):
        cm = astdef.CommandFor(p.lineno, p.PIDENTIFIER, p.value0, p.value1, False, p.commands)
        cm.children = [p.value0, p.value1, p.commands]
        return cm

    @_('FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        cm = astdef.CommandFor(p.lineno, p.PIDENTIFIER, p.value0, p.value1, True, p.commands)
        cm.children = [p.value0, p.value1, p.commands]
        return cm

    @_('READ identifier ";"')
    def command(self, p):
        cm = astdef.CommandRead(p.lineno, p.identifier)
        cm.children = [p.identifier]
        return cm

    @_('WRITE value ";"')
    def command(self, p):
        cm =  astdef.CommandWrite(p.lineno, p.value)
        cm.children = [p.value]
        return cm

    @_('value')
    def expression(self, p):
        return p.value

    @_('value PLUS value')
    def expression(self, p):
        ex = astdef.ExpressionPlus(p.lineno, p.value0, p.value1)
        ex.children = [p.value0, p.value1]
        return ex

    @_('value MINUS value')
    def expression(self, p):
        ex = astdef.ExpressionMinus(p.lineno, p.value0, p.value1)
        ex.children = [p.value0, p.value1]
        return ex

    @_('value TIMES value')
    def expression(self, p):
        ex = astdef.ExpressionTimes(p.lineno, p.value0, p.value1)
        ex.children = [p.value0, p.value1]
        return ex

    @_('value DIV value')
    def expression(self, p):
        ex = astdef.ExpressionDiv(p.lineno, p.value0, p.value1)
        ex.children = [p.value0, p.value1]
        return ex

    @_('value MOD value')
    def expression(self, p):
        ex = astdef.ExpressionMod(p.lineno, p.value0, p.value1)
        ex.children = [p.value0, p.value1]
        return ex

    @_('value EQ value')
    def condition(self, p):
        co = astdef.ConditionEq(p.lineno, p.value0, p.value1)
        co.children = [p.value0, p.value1]
        return co

    @_('value NEQ value')
    def condition(self, p):
        co = astdef.ConditionNeq(p.lineno, p.value0, p.value1)
        co.children = [p.value0, p.value1]
        return co

    @_('value LE value')
    def condition(self, p):
        co = astdef.ConditionLe(p.lineno, p.value0, p.value1)
        co.children = [p.value0, p.value1]
        return co

    @_('value GE value')
    def condition(self, p):
        co = astdef.ConditionGe(p.lineno, p.value0, p.value1)
        co.children = [p.value0, p.value1]
        return co

    @_('value LEQ value')
    def condition(self, p):
        co = astdef.ConditionLeq(p.lineno, p.value0, p.value1)
        co.children = [p.value0, p.value1]
        return co

    @_('value GEQ value')
    def condition(self, p):
        co = astdef.ConditionGeq(p.lineno, p.value0, p.value1)
        co.children = [p.value0, p.value1]
        return co

    @_('NUM')
    def value(self, p):
        return astdef.ValueLiteral(p.lineno, p.NUM)

    @_('identifier')
    def value(self, p):
        va = astdef.ValueVar(p.identifier.det, p.identifier)
        va.children = [p.identifier]
        return va

    @_('PIDENTIFIER')
    def identifier(self, p):
        return astdef.IdentifierVar(p.lineno, p.PIDENTIFIER)

    @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    def identifier(self, p):
        return astdef.IdentifierArrVar(p.lineno, p.PIDENTIFIER0, p.PIDENTIFIER1)

    @_('PIDENTIFIER "[" NUM "]"')
    def identifier(self, p):
        return astdef.IdentifierArrConst(p.lineno, p.PIDENTIFIER, p.NUM)

    def error(self, p):
        if p:
            raise ParserError("Parser error:\nLine: {0}, Unexpected token: {1}".format(p.lineno, p.value))
        else:
            raise ParserError("Parser error:\nUnexpected end of file")
