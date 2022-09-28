import sys

pattern = sys.argv[1]
filename = sys.argv[2]

lps = [0 for i in pattern]

lenlps = 0 #Obecna dlugosc lps
i = 1 #Pozycja we wzorcu
while i < len(pattern):
    if pattern[i] == pattern[lenlps]:
        lenlps += 1
        lps[i] = lenlps
        i += 1
    else:
        if lenlps != 0:
            lenlps = lps[lenlps-1] #Sproboj ponownie z krotzym
        else:
            lps[i] = 0
            i += 1

file = open(filename, "rt")
text = file.read()
patmatch = 0
idx = 0
while idx < len(text):
    if text[idx] == pattern[patmatch]:
        patmatch += 1
        if patmatch == len(pattern):
            patmatch = lps[len(pattern)-1]
            print("FOUND AT", idx-len(pattern)+1)
    else:
        if patmatch != 0:
            patmatch = lps[patmatch-1]
            continue
    idx += 1


    
