import asmhelpers as ah
import asmcommands as ac

class ProgramError(Exception):
    pass

class Program:
    def __init__(self, vars, commands):
        self.vars = vars
        self.prevvars = None
        self.commands = commands

    def genasm(self):
        asm = []
        mainaloc = ah.regaloc(0)
        asm += ah.unwrapAsmList(self.commands, self, mainaloc)
        asm += [ac.HALT()]
        return asm

    def wrapVars(self):
        parent = self.vars
        newprev = {}
        newprev["prev"] = self.prevvars
        newprev["actual"] = self.vars
        self.prevvars = newprev
        newvars = LocalStore(parent)
        self.vars = newvars

    def unWrapVars(self):
        if self.prevvars == None:
            raise ValueError("Compiler bug: Exiting global scope")
        self.vars = self.prevvars["actual"]
        self.prevvars = self.prevvars["prev"]

class Variable:
    def __init__(self, det, name):
        self.det = det
        self.name = name
        self.memstart = None

class VariableArray:
    def __init__(self, det, name, startidx, endidx):
        self.det = det
        arrlen = (endidx-startidx) + 1
        if arrlen < 1:
            raise ProgramError("Program error:\nTablica o długości < 1\nLinia: {0}, Nazwa: {1}".format(det, name))
        self.name = name
        self.indxstart = startidx
        self.leng = arrlen
        self.memstart = None

class VariableStore:
    def __init__(self, vars):
        self.variables = {}
        self.nextmem = 0
        for nvar in vars:
            if isinstance(nvar, Variable):
                self.addVar(nvar)
            if isinstance(nvar, VariableArray):
                self.addVarArray(nvar)

    def declared(self, nvar):
        return nvar.name in self.variables

    def addVar(self, nvar):
        if self.declared(nvar):
            raise ProgramError("Program Error:\nVariable redeclaration:\nline: {0}, name: {1}".format(nvar.det, nvar.name))
        self.variables[nvar.name] = nvar
        nvar.memstart = self.nextmem
        self.nextmem += 1

    def addVarArray(self, nvar):
        if self.declared(nvar):
            raise ProgramError("Program Error:\nVariable redeclaration:\nline: {0}, name: {1}".format(nvar.det, nvar.name))
        self.variables[nvar.name] = nvar
        nvar.memstart = self.nextmem
        self.nextmem += nvar.leng

    def isLocal(self, vname):
        return False

    def getVar(self, vname, errline):
        if vname not in self.variables:
            raise ProgramError("Program Error:\nNo such variable:\nline: {0}, name: {1}".format(errline, vname))
        if not isinstance(self.variables[vname], Variable):
            raise ProgramError("Program Error:\nUsing array as var:\nline: {0}, name: {1}".format(errline, vname))
        return self.variables[vname].memstart

    def gArrMem(self, arrname, errline):
        if arrname not in self.variables:
            raise ProgramError("Program Error:\nNo such variable:\nline: {0}, name: {1}".format(errline, arrname))
        if not isinstance(self.variables[arrname], VariableArray):
            raise ProgramError("Program Error:\nUsing var as array:\nline: {0}, name: {1}".format(errline, arrname))
        return self.variables[arrname].memstart

    def gArrFirst(self, arrname, errline):
        if arrname not in self.variables:
            raise ProgramError("Program Error:\nNo such variable:\nline: {0}, name: {1}".format(errline, arrname))
        if not isinstance(self.variables[arrname], VariableArray):
            raise ProgramError("Program Error:\nUsing var as array:\nline: {0}, name: {1}".format(errline, arrname))
        return self.variables[arrname].indxstart

class LocalStore:
    def __init__(self, parent):
        self.parent = parent
        self.nextmem = parent.nextmem
        self.variables = {}

    def declared(self, nvar):
        if nvar.name in self.variables:
            return True
        return self.parent.declared(nvar)

    def addVar(self, nvar):
        if not isinstance(nvar,Variable):
            raise ValueError("Compiler bug: local addVar is array")
        if self.declared(nvar):
            raise ProgramError("Program Error:\nVariable redeclaration:\nline: {0}, name: {1}".format(nvar.det, nvar.name))
        self.variables[nvar.name] = nvar
        nvar.memstart = self.nextmem
        self.nextmem += 1

    def isLocal(self, vname):
        if vname in self.variables:
            return True
        else:
            return self.parent.isLocal(vname)

    def getVar(self, vname, errline):
        if vname in self.variables:
            return self.variables[vname].memstart
        else:
            return self.parent.getVar(vname, errline)

    def gArrMem(self, arrname, errline):
        if arrname in self.variables:
            raise ProgramError("Program Error:\nUsing array as var:\nline: {0}, name: {1}".format(errline, arrname))
        return self.parent.gArrMem(arrname, errline)

    def gArrFirst(self, arrname, errline):
        if arrname in self.variables:
            raise ProgramError("Program Error:\nUsing array as var:\nline: {0}, name: {1}".format(errline, arrname))
        return self.parent.gArrFirst(arrname, errline)

    def getInternalMem(self):
        res = self.nextmem
        self.nextmem += 1
        return res



class IdentifierVar:
    def __init__(self, det, vname):
        self.det = det
        self.vname = vname

    def isLocal(self, prog):
        return prog.vars.isLocal(self.vname)

    def genasm(self, prog, ra):
        target = prog.vars.getVar(self.vname, self.det)
        asm = []
        asm += ah.genConst(target, ra.reg(0))
        return asm


class IdentifierArrVar:
    def __init__(self, det, arrname, vname):
        self.det = det
        self.arrname = arrname
        self.vname = vname

    def isLocal(self, prog):
        return False

    def genasm(self, prog, ra):
        target = prog.vars.gArrMem(self.arrname, self.det)
        target -= prog.vars.gArrFirst(self.arrname, self.det)
        positaddr = prog.vars.getVar(self.vname, self.det)
        asm = []
        asm += ah.genConst(positaddr, ra.reg(0))
        asm.append(ac.LOAD(ra.reg(0)))
        asm.append(ac.SWAP(ra.reg(0)))
        asm += ah.genConst(target, ra.reg(1))
        asm.append(ac.SWAP(ra.reg(0)))
        asm.append(ac.ADD(ra.reg(1)))
        asm.append(ac.SWAP(ra.reg(0)))
        return asm

class IdentifierArrConst:
    def __init__(self, det, arrname, offs):
        self.det = det
        self.arrname = arrname
        self.offs = offs

    def isLocal(self, prog):
        return False
    
    def genasm(self, prog, ra):
        target = prog.vars.gArrMem(self.arrname, self.det)
        targetshift = prog.vars.gArrFirst(self.arrname, self.det)
        target += (self.offs-targetshift)
        asm = []
        asm += ah.genConst(target, ra.reg(0))
        return asm

class ExpressionPlus:
    def __init__(self, det, vf, vs):
        self.det = det
        self.vf = vf
        self.vs = vs
    
    def genasm(self, prog, ra):
        asm = []
        asm += self.vf.genasm(prog,ra.subal(0))
        asm += self.vs.genasm(prog,ra.subal(1))
        asm.append(ac.SWAP(ra.reg(1)))
        asm.append(ac.ADD(ra.reg(0)))
        asm.append(ac.SWAP(ra.reg(0)))
        return asm

class ExpressionMinus:
    def __init__(self, det, vf, vs):
        self.det = det
        self.vf = vf
        self.vs = vs
    
    def genasm(self, prog, ra):
        asm = []
        asm += self.vf.genasm(prog,ra.subal(0))
        asm += self.vs.genasm(prog,ra.subal(1))
        asm.append(ac.SWAP(ra.reg(0)))
        asm.append(ac.SUB(ra.reg(1)))
        asm.append(ac.SWAP(ra.reg(0)))
        return asm

class ExpressionTimes:
    def __init__(self, det, vf, vs):
        self.det = det
        self.vf = vf
        self.vs = vs
    
    def genasm(self, prog, ra):
        asm = []
        lh = ah.labelHelper()
        asm += self.vf.genasm(prog,ra.subal(0))
        asm += self.vs.genasm(prog,ra.subal(1))
        asm += [
        ac.RESET("a"),
        ac.SUB(ra.reg(1)),
        ac.JNEG(lh.lab("nosignmod")),
        ac.SWAP(ra.reg(1)),
        ac.RESET("a"),
        ac.SUB(ra.reg(0)),
        ac.SWAP(ra.reg(0)),

        lh.lab("nosignmod"),
        ac.RESET(ra.reg(2)), #1
        ac.INC(ra.reg(2)),
        ac.RESET(ra.reg(3)), #-1
        ac.DEC(ra.reg(3)),
        ac.RESET(ra.reg(4)), #wynik

        lh.lab("mulloop"),
        ac.RESET("a"),
        ac.ADD(ra.reg(1)),
        ac.SHIFT(ra.reg(3)),
        ac.SHIFT(ra.reg(2)),
        ac.SUB(ra.reg(1)), #ostatni bit
        ac.JZERO(lh.lab("zerobit")),
        #Dodaj do wyniku
        ac.RESET("a"),
        ac.ADD(ra.reg(4)),
        ac.ADD(ra.reg(0)),
        ac.SWAP(ra.reg(4)),
        #Przemnoz skladnik
        lh.lab("zerobit"),
        ac.RESET("a"),
        ac.ADD(ra.reg(0)),
        ac.SHIFT(ra.reg(2)),
        ac.SWAP(ra.reg(0)),
        #Przesun mnoznik
        ac.RESET("a"),
        ac.ADD(ra.reg(1)),
        ac.SHIFT(ra.reg(3)),
        ac.JZERO(lh.lab("endmul")),
        ac.SWAP(ra.reg(1)),
        ac.JUMP(lh.lab("mulloop")),

        lh.lab("endmul"),
        ac.SWAP(ra.reg(4)),
        ac.SWAP(ra.reg(0))]
        return asm

class ExpressionDiv:
    def __init__(self, det, vf, vs):
        self.det = det
        self.vf = vf
        self.vs = vs
    
    def genasm(self, prog, ra):
        asm = []
        lh = ah.labelHelper()
        asm += self.vf.genasm(prog,ra.subal(0))
        asm += self.vs.genasm(prog,ra.subal(1))
        asm += [ac.RESET(ra.reg(2))] #Result
        asm += [ac.RESET(ra.reg(3))] #shifted
        asm += [ac.RESET(ra.reg(4))] #sign

        asm += [ac.RESET("a")]
        asm += [ac.SUB(ra.reg(1))]
        asm += [ac.JZERO(lh.lab("enddivswap"))]

        #check sign
        asm += [
            ac.JNEG(lh.lab("oneplus")), #1 is ok (pos)
            ac.SWAP(ra.reg(1)),
            #oneminus
            ac.RESET("a"),
            ac.SUB(ra.reg(0)),
            ac.JNEG(lh.lab("difsign")), #1 ujemne, 0 dodatnie
            ac.SWAP(ra.reg(0)),
            ac.JUMP(lh.lab("samesign")),
            lh.lab("oneplus"),
            #oneplus
            ac.RESET("a"),
            ac.SUB(ra.reg(0)),
            ac.JNEG(lh.lab("samesign")), #1 dodatnie, 0 dodatnie
            ac.SWAP(ra.reg(0)),
            #difsign
            lh.lab("difsign"),
            ac.INC(ra.reg(4)),
            #samesign
            lh.lab("samesign")
        ]

        #alignloop
        asm += [
            lh.lab("alignloop"),
            ac.RESET("a"),
            ac.ADD(ra.reg(1)),
            ac.SUB(ra.reg(0)),
            ac.JPOS(lh.lab("exitalign")), #mloop
            ac.RESET("a"),
            ac.INC("a"),
            ac.SWAP(ra.reg(1)),
            ac.SHIFT(ra.reg(1)),
            ac.SWAP(ra.reg(1)),
            ac.INC(ra.reg(3)),
            ac.JUMP(lh.lab("alignloop")),
            lh.lab("exitalign")
        ]

        #mloop
        asm += [
            lh.lab("mloop"),
            ac.RESET("a"),
            ac.ADD(ra.reg(3)),
            ac.JZERO(lh.lab("endmloop")), #endmloop
            ac.RESET("a"),
            ac.INC("a"),
            ac.SWAP(ra.reg(2)),
            ac.SHIFT(ra.reg(2)),
            ac.SWAP(ra.reg(2)),
            ac.RESET("a"),
            ac.DEC("a"),
            ac.SWAP(ra.reg(1)),
            ac.SHIFT(ra.reg(1)),
            ac.SWAP(ra.reg(1)),
            ac.DEC(ra.reg(3)),
            ac.RESET("a"),
            ac.ADD(ra.reg(1)),
            ac.SUB(ra.reg(0)),
            ac.JPOS(lh.lab("mloop")),
            ac.INC(ra.reg(2)),
            ac.RESET("a"),
            ac.ADD(ra.reg(0)),
            ac.SUB(ra.reg(1)),
            ac.SWAP(ra.reg(0)),
            ac.JUMP(lh.lab("mloop")),
            lh.lab("endmloop")
        ]

        asm += [
            ac.SWAP(ra.reg(4)),
            ac.JZERO(lh.lab("endsigncor")),
            ac.RESET("a"),
            ac.SUB(ra.reg(2)),
            ac.SWAP(ra.reg(2)),
            ac.SWAP(ra.reg(0)),
            ac.JZERO(lh.lab("endsigncor")),
            ac.DEC(ra.reg(2)),
            lh.lab("endsigncor")
        ]

        asm += [
            ac.SWAP(ra.reg(2)),
            lh.lab("enddivswap"),
            ac.SWAP(ra.reg(0))
        ]
        return asm

class ExpressionMod():
    def __init__(self, det, vf, vs):
        self.det = det
        self.vf = vf
        self.vs = vs
    
    def genasm(self, prog, ra):
        asm = []
        lh = ah.labelHelper()
        asm += self.vf.genasm(prog,ra.subal(0))
        asm += self.vs.genasm(prog,ra.subal(1))
        asm += [ac.RESET("a")] #diviscpy
        asm += [ac.ADD(ra.reg(1))]
        asm += [ac.SWAP(ra.reg(2))]
        asm += [ac.RESET(ra.reg(3))] #shifted
        asm += [ac.RESET(ra.reg(4))] #sign

        asm += [ac.RESET("a")]
        asm += [ac.SUB(ra.reg(1))]
        asm += [ac.JZERO(lh.lab("endmodswap"))] #endmloop

        #check sign
        asm += [
            ac.JNEG(lh.lab("oneplus")), #1 is ok (pos)
            ac.SWAP(ra.reg(1)),
            #oneminus
            ac.RESET("a"),
            ac.SUB(ra.reg(0)),
            ac.JNEG(lh.lab("difsign")), #1 ujemne, 0 dodatnie
            ac.SWAP(ra.reg(0)),
            ac.JUMP(lh.lab("samesign")),
            lh.lab("oneplus"),
            ac.RESET("a"),
            ac.SUB(ra.reg(0)),
            ac.JNEG(lh.lab("samesign")), #1 dodatnie, 0 dodatnie
            ac.SWAP(ra.reg(0)),
            lh.lab("difsign"),
            ac.INC(ra.reg(4)),
            lh.lab("samesign")
        ]

        #alignloop
        asm += [
            lh.lab("alignloop"),
            ac.RESET("a"),
            ac.ADD(ra.reg(1)),
            ac.SUB(ra.reg(0)),
            ac.JPOS(lh.lab("mloop")),
            ac.RESET("a"),
            ac.INC("a"),
            ac.SWAP(ra.reg(1)),
            ac.SHIFT(ra.reg(1)),
            ac.SWAP(ra.reg(1)),
            ac.INC(ra.reg(3)),
            ac.JUMP(lh.lab("alignloop"))
        ]

        #mloop
        asm += [
            lh.lab("mloop"),
            ac.RESET("a"),
            ac.ADD(ra.reg(3)),
            ac.JZERO(lh.lab("endmloop")),
            ac.RESET("a"),
            ac.DEC("a"),
            ac.SWAP(ra.reg(1)),
            ac.SHIFT(ra.reg(1)),
            ac.SWAP(ra.reg(1)),
            ac.DEC(ra.reg(3)),
            ac.RESET("a"),
            ac.ADD(ra.reg(1)),
            ac.SUB(ra.reg(0)),
            ac.JPOS(lh.lab("mloop")),
            ac.RESET("a"),
            ac.ADD(ra.reg(0)),
            ac.SUB(ra.reg(1)),
            ac.SWAP(ra.reg(0)),
            ac.JUMP(lh.lab("mloop")),
            lh.lab("endmloop")
        ]

        asm += [
            ac.SWAP(ra.reg(4)),
            ac.JZERO(lh.lab("norevers")), 
            ac.RESET("a"),
            ac.ADD(ra.reg(0)),
            ac.JZERO(lh.lab("endmod")),
            ac.RESET("a"),
            ac.ADD(ra.reg(2)),
            ac.JNEG(lh.lab("ujemnypath")),
            ac.SUB(ra.reg(0)),
            ac.JUMP(lh.lab("reversdone")),
            lh.lab("ujemnypath"),
            ac.ADD(ra.reg(0)),
            ac.SWAP(ra.reg(4)),
            ac.RESET("a"),
            ac.SUB(ra.reg(4)),
            lh.lab("reversdone"),
            ac.SWAP(ra.reg(0)),

            lh.lab("norevers"),
            ac.SWAP(ra.reg(2)),
            ac.JPOS(lh.lab("endmod")),
            ac.RESET("a"),
            ac.SUB(ra.reg(0)),
            lh.lab("endmodswap"),
            ac.SWAP(ra.reg(0)),
            lh.lab("endmod")
        ]
        return asm

class ValueLiteral():
    def __init__(self, det, val):
        self.det = det
        self.val = val
    def genasm(self, prog, ra):
        asm = []
        asm += ah.genConst(self.val, ra.reg(0))
        return asm

class ValueVar():
    def __init__(self, det, ident):
        self.det = det
        self.ident = ident
    def genasm(self, prog, ra):
        asm = []
        asm += self.ident.genasm(prog, ra.subal(0))
        asm += [
            ac.LOAD(ra.reg(0)),
            ac.SWAP(ra.reg(0))
        ]
        return asm


class ConditionEq():
    def __init__(self, det, vu, vd):
        self.det = det
        self.vu = vu
        self.vd = vd

    def genasm(self, prog, ra, falseLabel):
        asm = []
        asm += self.vu.genasm(prog, ra.subal(0))
        asm += self.vd.genasm(prog, ra.subal(1))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.SUB(ra.reg(1)),
            ac.JPOS(falseLabel),
            ac.JNEG(falseLabel)
        ]
        return asm

class ConditionNeq():
    def __init__(self, det, vu, vd):
        self.det = det
        self.vu = vu
        self.vd = vd

    def genasm(self, prog, ra, falseLabel):
        asm = []
        asm += self.vu.genasm(prog, ra.subal(0))
        asm += self.vd.genasm(prog, ra.subal(1))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.SUB(ra.reg(1)),
            ac.JZERO(falseLabel)
        ]
        return asm

class ConditionLe():
    def __init__(self, det, vu, vd):
        self.det = det
        self.vu = vu
        self.vd = vd

    def genasm(self, prog, ra, falseLabel):
        asm = []
        asm += self.vu.genasm(prog, ra.subal(0))
        asm += self.vd.genasm(prog, ra.subal(1))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.SUB(ra.reg(1)),
            ac.JPOS(falseLabel),
            ac.JZERO(falseLabel)
        ]
        return asm

class ConditionGe():
    def __init__(self, det, vu, vd):
        self.det = det
        self.vu = vu
        self.vd = vd

    def genasm(self, prog, ra, falseLabel):
        asm = []
        asm += self.vu.genasm(prog, ra.subal(0))
        asm += self.vd.genasm(prog, ra.subal(1))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.SUB(ra.reg(1)),
            ac.JNEG(falseLabel),
            ac.JZERO(falseLabel)
        ]
        return asm

class ConditionLeq():
    def __init__(self, det, vu, vd):
        self.det = det
        self.vu = vu
        self.vd = vd

    def genasm(self, prog, ra, falseLabel):
        asm = []
        asm += self.vu.genasm(prog, ra.subal(0))
        asm += self.vd.genasm(prog, ra.subal(1))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.SUB(ra.reg(1)),
            ac.JPOS(falseLabel)
        ]
        return asm


class ConditionGeq():
    def __init__(self, det, vu, vd):
        self.det = det
        self.vu = vu
        self.vd = vd

    def genasm(self, prog, ra, falseLabel):
        asm = []
        asm += self.vu.genasm(prog, ra.subal(0))
        asm += self.vd.genasm(prog, ra.subal(1))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.SUB(ra.reg(1)),
            ac.JNEG(falseLabel)
        ]
        return asm

class CommandAssign():
    def __init__(self, det, ident, expres):
        self.det = det
        self.ident = ident
        self.expres = expres

    def genasm(self, prog, ra):
        asm = []
        asm += self.expres.genasm(prog, ra.subal(0))
        asm += self.ident.genasm(prog, ra.subal(1))
        if self.ident.isLocal(prog):
            raise ProgramError("Program error:\nAssigning into local variable:\nLine: {0}".format(self.det))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.STORE(ra.reg(1))
        ]
        return asm

class CommandIf():
    def __init__(self, det, condition, trueCommands, falseCommands=None):
        self.det = det
        self.condition = condition
        self.trueCommands = trueCommands
        self.falseCommands = falseCommands

    def genasm(self, prog, ra):
        asm = []
        lh = ah.labelHelper()
        asm += self.condition.genasm(prog,ra.subal(0),lh.lab("NOTTRUE"))
        asm += ah.unwrapAsmList(self.trueCommands, prog, ra)
        if self.falseCommands != None:
            asm += [ac.JUMP(lh.lab("ENDIF"))]
            asm += [lh.lab("NOTTRUE")]
            asm += ah.unwrapAsmList(self.falseCommands, prog, ra)
            asm += [lh.lab("ENDIF")]
        else:
            asm += [lh.lab("NOTTRUE")]
        return asm

class CommandWhile():
    def __init__(self, det, condition, commands):
        self.det = det
        self.condition = condition
        self.commands = commands

    def genasm(self, prog, ra):
        asm = []
        lh = ah.labelHelper()
        asm += [lh.lab("WHILESTART")]
        asm += self.condition.genasm(prog, ra.subal(0), lh.lab("EXITWHILE"))
        asm += ah.unwrapAsmList(self.commands, prog, ra.subal(0))
        asm += [ac.JUMP(lh.lab("WHILESTART"))]
        asm += [lh.lab("EXITWHILE")]
        return asm

class CommandRepeat():
    def __init__(self, det, condition, commands):
        self.det = det
        self.condition = condition
        self.commands = commands

    def genasm(self, prog, ra):
        asm = []
        lh = ah.labelHelper()
        asm += [lh.lab("REPEATSTART")]
        asm += ah.unwrapAsmList(self.commands, prog, ra.subal(0))
        asm += self.condition.genasm(prog, ra.subal(0), lh.lab("REPEATSTART"))
        return asm

class CommandRead():
    def __init__(self, det, ident):
        self.det = det
        self.ident = ident

    def genasm(self, prog, ra):
        asm = []
        asm += self.ident.genasm(prog, ra.subal(0))
        if self.ident.isLocal(prog):
            raise ProgramError("Program error:\nReading into local variable:\nLine: {0}".format(self.det))
        asm += [
            ac.GET(),
            ac.STORE(ra.reg(0))
        ]
        return asm

class CommandWrite():
    def __init__(self, det, val):
        self.det = det
        self.val = val

    def genasm(self, prog, ra):
        asm = []
        asm += self.val.genasm(prog, ra.subal(0))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.PUT()
        ]
        return asm

class CommandFor:
    def __init__(self, det, itername, startval, endval, goingDown, commands):
        self.det = det
        self.itername = itername
        self.startval = startval
        self.endval = endval
        self.goingDown = goingDown
        self.commands = commands

    def genasm(self, prog, ra):
        prog.wrapVars()
        prog.vars.addVar(Variable(self.det, self.itername))
        endvalcopyaddr = prog.vars.getInternalMem()

        asm = []
        lh = ah.labelHelper()

        #Copy start->iter, end->endcopy
        asm += self.startval.genasm(prog, ra.subal(0))

        asm += ah.genConst(prog.vars.getVar(self.itername, self.det), ra.reg(1))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.STORE(ra.reg(1))
        ]

        asm += self.endval.genasm(prog, ra.subal(0))
        asm += ah.genConst(endvalcopyaddr, ra.reg(1))
        asm += [
            ac.SWAP(ra.reg(0)),
            ac.STORE(ra.reg(1))
        ]

        #Check end condition
        asm += ah.genConst(prog.vars.getVar(self.itername, self.det), ra.reg(0))
        asm += [
            ac.LOAD(ra.reg(0)),
            lh.lab("FOREVAL"),
            ac.SWAP(ra.reg(0))
        ]
        asm += ah.genConst(endvalcopyaddr, ra.reg(1))
        asm += [
            ac.LOAD(ra.reg(1)),
            ac.SUB(ra.reg(0))
        ]

        if not self.goingDown:
            asm += [
                ac.JNEG(lh.lab("EXITFOR"))
            ]
        else:
            asm += [
                ac.JPOS(lh.lab("EXITFOR"))
            ]

        asm += ah.unwrapAsmList(self.commands, prog, ra.subal(0))


        #INCREMENT COUNTER
        asm += ah.genConst(prog.vars.getVar(self.itername, self.det), ra.reg(0))
        asm += [ac.LOAD(ra.reg(0))]
        if not self.goingDown:
            asm += [ac.INC("a")]
        else:
            asm += [ac.DEC("a")]
        asm += [ac.STORE(ra.reg(0))]

        asm += [
            ac.JUMP(lh.lab("FOREVAL")),
            lh.lab("EXITFOR")
        ]


        prog.unWrapVars()
        return asm
