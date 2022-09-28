import sys

asmfil = sys.argv[1]
fil = open(asmfil, "rb")
data = fil.read()
fil.close()

print("{", end="")
for ind in range(len(data)):
    print(hex(data[ind]), end="")
    if ind < len(data)-1:
        print(",", end="")
print("}")
