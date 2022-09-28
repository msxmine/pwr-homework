import mylexer
import myparser
import postprocess
import assignsanity
import interpreter

lexer = mylexer.MyLexer()
parser = myparser.MyParser()

f = open("./debug6.ret", "r")
prog = f.read()
f.close()


res = parser.parse(lexer.tokenize(prog))
ass = res.genasm()
assignsanity.checkProgram(res)
postprocess.resolveLabels(ass)
asm = postprocess.assemble(ass)

print(asm)

masz = interpreter.maszyna()
masz.loadprog(asm)
masz.run()
