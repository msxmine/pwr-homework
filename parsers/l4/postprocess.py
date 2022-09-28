import asmhelpers
import asmcommands

def resolveLabels(extasm):
    linidx = 0
    while linidx < len(extasm):
        curcom = extasm[linidx]
        if isinstance(curcom, asmhelpers.asmLabel):
            curcom.setAddr(linidx)
            extasm.pop(linidx)
        else:
            linidx += 1

    for i in range(len(extasm)):
        curcom = extasm[i]
        if isinstance(curcom, asmcommands.JumpInstr):
            if isinstance(curcom.offset, asmhelpers.asmLabel):
                curcom.offset = (curcom.offset.getAddr() - i)

def assemble(asmlist):
    res = ""
    for i in asmlist:
        res += (i.gen() + "\n")
    return res
