import math

def reg(name):
    regs = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    return regs[name]

class maszyna:
    def __init__(self):
        pass
    
    def loadprog(self, prog):
        self.addr = -1
        self.prog = prog
        self.registers = [0,0,0,0,0,0,0,0]
        self.memory = {}

    def run(self):
        while True:
            #print(self.registers)
            #print(self.memory)
            self.addr += 1
            curline  = self.prog.splitlines()[self.addr].split(" ")
            #print(curline)
            instr = curline[0]
            if instr == "GET":
                self.registers[0] = int(input())
            elif instr == "PUT":
                print(self.registers[0])
            elif instr == "LOAD":
                self.registers[0] = self.memory[self.registers[reg(curline[1])]]
            elif instr == "STORE":
                self.memory[self.registers[reg(curline[1])]] = self.registers[0]
            elif instr == "ADD":
                self.registers[0] += self.registers[reg(curline[1])]
            elif instr == "SUB":
                self.registers[0] -= self.registers[reg(curline[1])]
            elif instr == "SHIFT":
                self.registers[0] = math.floor(self.registers[0] * (2**self.registers[reg(curline[1])]))
            elif instr == "SWAP":
                self.registers[0], self.registers[reg(curline[1])] = self.registers[reg(curline[1])], self.registers[0]
            elif instr == "RESET":
                self.registers[reg(curline[1])] = 0
            elif instr == "INC":
                self.registers[reg(curline[1])] += 1
            elif instr == "DEC":
                self.registers[reg(curline[1])] -= 1
            elif instr == "JUMP":
                self.addr += (int(curline[1]) - 1)
            elif instr == "JPOS":
                if self.registers[0] > 0:
                    self.addr += (int(curline[1]) - 1)
            elif instr == "JZERO":
                if self.registers[0] == 0:
                    self.addr += (int(curline[1]) - 1)
            elif instr == "JNEG":
                if self.registers[0] < 0:
                    self.addr += (int(curline[1]) - 1)
            elif instr == "HALT":
                break
            #input()



