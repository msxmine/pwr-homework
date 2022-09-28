import itertools

pchar = {"ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ż": "z", "ź": "z"}

def plnorm(plstr):
    letters = []
    for char in plstr:
        if char in pchar:
            letters.append(pchar[char])
        else:
            letters.append(char)
    return "".join(letters)

words = {}

def fill_trie(file):
    for line in file:
        word = plnorm(line.rstrip().lower())
        current_dict = words
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict["_end_"] = "_end_"

def check_word(wordraw):
    word = plnorm(wordraw.rstrip().lower())
    current_dict = words
    for letter in word:
        if letter in current_dict:
            current_dict = current_dict[letter]
        else:
            return 0
    if "_end_" in current_dict:
        return 2
    else:
        return 1

feng = open("engdict.txt", "r")
fpol = open("poldict.txt", "r")

fill_trie(feng)
fill_trie(fpol)

feng.close()
fpol.close()

#separators = [".", "?", ",", ":", ";", " ", "(", ")", "-", "!", "\""]
separators = [".", "?", ",", ":", " ", "-", "!", "\""]
def separate(intext):
    result = []
    word = []
    for char in intext:
        if char in separators:
            if len(word) > 0:
                result.append("".join(word))
            result.append(str(char))
            word = []
        else:
            word.append(char)
    if len(word) > 0:
        result.append("".join(word))
    return result

def containsweirdchars(text):
    for char in text:
        if ord(char) in itertools.chain(range(0,10), range(12,32)):
            return 1
    return 0

sentencecache = {}

def sentenceerrcnt(sentence):
    global sentencecache
    if len(sentencecache) > 1000:
        sentencecache = {}
    errors = 0
    sentarr = separate(sentence)
    #print(sentarr)
    if len(sentarr) > 5: 
        sentprefix = "".join(sentarr[:-2])
        if sentprefix in sentencecache:
            errors = sentencecache[sentprefix]
            if check_word(sentarr[-2]) != 2 and sentarr[-2] not in separators:
                errors += 1
            if containsweirdchars(sentarr[-2]) == 1:
                errors += 10
            sentencecache["".join(sentarr[:-1])] = errors
            if check_word(sentarr[-1]) == 0 and sentarr[-1] not in separators:
                errors += 1
            if containsweirdchars(sentarr[-1]) == 1:
                errors += 10
            #print(sentence, errors)
            return errors
    for word in sentarr[:-1]:
        if check_word(word) == 0 and word not in separators:
            errors += 1#len(word)
        if containsweirdchars(word) == 1:
            errors += 10
    sentencecache["".join(sentarr[:-1])] = errors
    if check_word(sentarr[-1]) == 0 and sentarr[-1] not in separators:
        errors += 1
    if containsweirdchars(sentarr[-1]) == 1:
        errors += 10
    return errors

def xorarr(arr1, arr2):
    maxlen = max(len(arr1), len(arr2))
    return bytearray(a ^ b for (a, b) in zip(arr1[:maxlen], arr2[:maxlen]))

fmsg = open("messages.txt", "r")
messages = []
for msgstr in fmsg:
    messages.append(bytes([int(grp,2) for grp in msgstr.rstrip().split()]))

def keybadness(key):
    result = 0
    for msg in messages:
        try:
            result += sentenceerrcnt(xorarr(msg, key).decode())
        except UnicodeDecodeError:
            result += 999
    return result

def printmessages(key):
    for msg in messages:
        print("Wiadomosc")
        print(xorarr(msg, key).decode().rstrip("\r\n"))

msglens = []
for msg in messages:
    msglens.append(len(msg))

msglens.sort()
maybedecodable = msglens[-2]

keycands = [[]]

def consolidateKeychoice():
    global keycands
    oldkeypos = len(keycands)
    if oldkeypos > 0:
        curstep = len(keycands[0])
        for idx in range(len(keycands)):
            keycands[idx][:curstep-30] = keycands[0][:curstep-30]
            keycands[idx] = tuple(keycands[idx])
        keycands = list(set(keycands))
        for idx in range(len(keycands)):
            keycands[idx] = list(keycands[idx])
        newkeypos = len(keycands)
        print("Zmiana mozliwosci", oldkeypos, "na", newkeypos)


for i in range(maybedecodable):
    print(i)
    consolidateKeychoice()
    bestsc = 99999999
    newkeycands = []
    if len(keycands) > 128:
        print("Zbyt duza niepewnosc, rozkodowano", i, "bajtow")
        break
    for kprefix in keycands:
        ksuffixes = []
        for i in range(256):
            keycand = kprefix + [i]
            kbsc = keybadness(bytearray(keycand))
            if kbsc <= bestsc:
                if kbsc < bestsc:
                    bestsc = kbsc
                    newkeycands = []
                    ksuffixes = []
                ksuffixes.append(i)
        ksuffixesfinal = ksuffixes.copy()
        for (k1, k2) in itertools.combinations(ksuffixes, 2):
            if k1 ^ k2 == 32:
                ksuffixesfinal.remove(k2)
        for ksuffix in ksuffixesfinal:
            newkeycands.append(kprefix + [ksuffix])
    keycands = newkeycands

printmessages(keycands[0])

