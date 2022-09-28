import sys

pattern = sys.argv[1]
filename = sys.argv[2]

characters = []
for char in pattern:
    if characters.count(char) == 0:
        characters.append(char)

FA = [[0 for i in range(len(characters))] for j in range(len(pattern)+1)]

for i in range(len(characters)):
    if characters[i] == pattern[0]:
        FA[0][i] = 1

lps = 0
for state in range(1,len(pattern)+1,1):
    FA[state] = FA[lps].copy()
    if state < len(pattern):
        for i in range(len(characters)):
            if characters[i] == pattern[state]:
                FA[state][i] = state+1
                lps = FA[lps][i]
                break

state = 0
file = open(filename, "rt")
text = file.read()

for idx, symbol in enumerate(text):
    try:
        charidx = characters.index(symbol)
        state = FA[state][charidx]
        if state == len(pattern):
            print("FOUND AT", idx-len(pattern)+1)
    except ValueError:
        state = 0
