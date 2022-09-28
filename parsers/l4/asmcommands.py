class RegisterInstr:
    def __init__(self, type, x):
        self.type = type
        self.x = x

    def gen(self):
        return self.type + " " + str(self.x)

class IoInstr:
    def __init__(self, type):
        self.type = type
    
    def gen(self):
        return self.type

class JumpInstr:
    def __init__(self, type, offset):
        self.type = type
        self.offset = offset
    
    def gen(self):
        return self.type + " " + str(int(self.offset))

class ADD(RegisterInstr):
    def __init__(self, x):
        super().__init__("ADD", x)

class SUB(RegisterInstr):
    def __init__(self, x):
        super().__init__("SUB", x)

class SHIFT(RegisterInstr):
    def __init__(self, x):
        super().__init__("SHIFT", x)

class SWAP(RegisterInstr):
    def __init__(self, x):
        super().__init__("SWAP", x)

class RESET(RegisterInstr):
    def __init__(self, x):
        super().__init__("RESET", x)

class INC(RegisterInstr):
    def __init__(self, x):
        super().__init__("INC", x)

class DEC(RegisterInstr):
    def __init__(self, x):
        super().__init__("DEC", x)

class LOAD(RegisterInstr):
    def __init__(self, x):
        super().__init__("LOAD", x)

class STORE(RegisterInstr):
    def __init__(self, x):
        super().__init__("STORE", x)

class GET(IoInstr):
    def __init__(self):
        super().__init__("GET")

class PUT(IoInstr):
    def __init__(self):
        super().__init__("PUT")

class HALT(IoInstr):
    def __init__(self):
        super().__init__("HALT")

class JUMP(JumpInstr):
    def __init__(self, j):
        super().__init__("JUMP", j)

class JPOS(JumpInstr):
    def __init__(self, j):
        super().__init__("JPOS", j)

class JZERO(JumpInstr):
    def __init__(self, j):
        super().__init__("JZERO", j)

class JNEG(JumpInstr):
    def __init__(self, j):
        super().__init__("JNEG", j)
