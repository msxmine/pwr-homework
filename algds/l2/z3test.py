#!/usr/bin/python3
import random
import subprocess

def genarray(order, num):
    if order == "sorted":
        return list(range(0,num))
    if order == "reverse":
        return list(range(num-1,-1,-1))
    if order == "random":
        tmp = list(range(0,num))
        random.shuffle(tmp)
        return tmp


algos = ["quick", "dualpivot"]
sizes = [10, 50, 100]
orders = ["sorted", "reverse", "random"]

for alg in algos:
    for size in sizes:
        for order in orders:
            print("ALGO",alg,"SIZE",size,"ORDER",order)
            data = genarray(order,size)
            #print(*data)
            process = subprocess.Popen(["./z3.py", "--type", alg, "--comp", "<="],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       encoding="utf8")
            indata = str(size) + "\n" + (" ").join(str(v) for v in data) + "\n"
            stdoutdata,stderrdata = process.communicate(input=indata)
            print(stderrdata.splitlines()[-1])
