import mylexer
import myparser
import postprocess
import assignsanity
import sys

lexer = mylexer.MyLexer()
parser = myparser.MyParser()

infilename = sys.argv[1]
outfilename = sys.argv[2]

infile = open(infilename, "r")
inprogram = infile.read()
infile.close()

try:
    ast = parser.parse(lexer.tokenize(inprogram))
    exasm = ast.genasm()
    assignsanity.checkProgram(ast)
    postprocess.resolveLabels(exasm)
    asm = postprocess.assemble(exasm)
except Exception as err:
    print("{0}".format(err))
else:
    outfile = open(outfilename, "w")
    outfile.write(asm)
    outfile.close()


