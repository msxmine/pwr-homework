import asmcommands as ac

class asmLabel():
    def __init__(self):
        self.address = 0
    def setAddr(self, addr):
        self.address = addr
    def getAddr(self):
        if self.address == 0:
            raise ValueError("Compiler bug: bad jump offset")
        return self.address

class labelHelper():
    def __init__(self):
        self.labelstor = {}
    def lab(self, name):
        if name not in self.labelstor:
            self.labelstor[name] = asmLabel()
        return self.labelstor[name]

class regaloc():
    registers = ["h", "g", "f", "e", "d", "c", "b"]
    def __init__(self, regs):
        self.regs = regs
    def reg(self, x):
        return self.registers[self.regs+x]
    def subal(self, x):
        return regaloc(self.regs+x)

def genConst(num, toreg):
    absnum = abs(num)
    binstr = format(absnum, 'b')
    asm = []
    asm.append(ac.RESET("a"))
    asm.append(ac.RESET(toreg))
    asm.append(ac.INC("a"))
    asm.append(ac.SWAP(toreg))
    for charidx in range(len(binstr)):
        if binstr[charidx] == "1":
            if num < 0:
                asm.append(ac.DEC("a"))
            else:
                asm.append(ac.INC("a"))
        if charidx < len(binstr)-1:
            asm.append(ac.SHIFT(toreg))
    asm.append(ac.SWAP(toreg))
    return asm

def copyReg(rfrom, rto):
    fr = rfrom
    to = rto
    asm = []
    if fr != to:
        if fr == "a":
            asm.append(ac.SWAP(to))
            fr = rto
            to = rfrom
        asm.append(ac.RESET("a"))
        asm.append(ac.ADD(fr))
        if to != "a":
            asm.append(ac.SWAP(to))
    return asm

def unwrapAsmList(commands, prog, ra):
    asm = []
    for com in commands:
        asm += com.genasm(prog,ra)
    return asm


