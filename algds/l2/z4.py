#!/usr/bin/python3
import argparse
import numpy as np
import sys
from time import process_time

parser = argparse.ArgumentParser(description="Zadanie 1")
gr1 = parser.add_argument_group()
gr1.add_argument("--type", choices=["insert", "merge", "quick", "dualpivot", "hybridquick"], required=True)
gr1.add_argument("--comp", choices=[">=", "<="], required=True)
parser.add_argument("--stat", nargs=2)
args = parser.parse_args()

def statprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    pass

def insertionsort(array, compare):
    compnum = 0
    movenum = 0
    for idx in range(1,len(array)):
        for pos in range(idx,0,-1):
            compnum += 1
            #statprint("porównuje", array[pos], "i", array[pos-1])
            if compare(array[pos], array[pos-1]):
                movenum += 1
                #statprint("zamieniam", array[pos], "i", array[pos-1])
                array[pos], array[pos-1] = array[pos-1], array[pos]
            else:
                break
    return compnum,movenum

def mergesort(array, compare):
    compnum = 0
    movenum = 0
    size = len(array)
    if size > 1:
        result = np.empty_like(array)
        mid = size//2
        subcmp1, submov1 = mergesort(array[:mid],compare)
        subcmp2, submov2 = mergesort(array[mid:],compare)
        compnum += (subcmp1 + subcmp2)
        movenum += (submov1 + submov2)
        
        lidx = 0
        ridx = mid
        
        for idx in range(0,size):
            if lidx == mid:
                for pos,i in enumerate(range(ridx, size),idx):
                    movenum += 1
                    #statprint("zapisuje", array[i], "do tablicy tymczasowej")
                    result[pos] = array[i]
                break
            if ridx == size:
                for pos,i in enumerate(range(lidx, mid),idx):
                    movenum += 1
                    #statprint("zapisuje", array[i], "do tablicy tymczasowej")
                    result[pos] = array[i]
                break
            compnum += 1
            #statprint("porównuje", array[lidx], "i", array[ridx])
            if compare(array[lidx], array[ridx]):
                movenum += 1
                #statprint("zapisuje", array[lidx], "do tablicy tymczasowej")
                result[idx] = array[lidx]
                lidx += 1
            else:
                movenum += 1
                #statprint("zapisuje", array[ridx], "do tablicy tymczasowej")
                result[idx] = array[ridx]
                ridx += 1
        #statprint("Kopiuje tablice tymczasowa do wyniku ,wielkosc:", size)
        array[:] = result
    return compnum, movenum

def quicksort(array, compare):
    compnum = 0
    movenum = 0
    size = len(array)
    if size > 1:
        movenum += 1
        #statprint("zamieniam", array[size//2], "i", array[size-1])
        array[size//2], array[size-1] = array[size-1], array[size//2]
        pivval = array[size-1]
        swapslot = 0
        for i in range(0,size-1):
            compnum += 1
            #statprint("porównuje", array[i], "i", pivval)
            if compare(array[i], pivval):
                movenum += 1
                #statprint("zamieniam", array[swapslot], "i", array[i])
                array[swapslot], array[i] = array[i], array[swapslot]
                swapslot += 1
        movenum += 1
        #statprint("zamieniam", array[swapslot], "i", array[size-1])
        array[swapslot], array[size-1] = array[size-1], array[swapslot]
        subcmp1, submov1 = quicksort(array[:swapslot], compare)
        subcmp2, submov2 = quicksort(array[swapslot+1:], compare)
        compnum += (subcmp1 + subcmp2)
        movenum += (submov1 + submov2)
    return compnum, movenum

def dpqsort(array, compare):
    compnum = 0
    movenum = 0
    size = len(array)
    if size > 1:
        compnum += 1
        #statprint("porównuje", array[size-1], "i", array[0])
        if compare(array[size-1], array[0]):
            movenum += 1
            #statprint("zamieniam", array[0], "i", array[size-1])
            array[0], array[size-1] = array[size-1], array[0]
        pnum = 0
        qnum = 0
        i = 1
        while i < (size-1-qnum):
            if qnum > pnum:
                compnum += 1
                #statprint("porównuje", array[size-1], "i", array[i])
                if compare(array[size-1], array[i]):
                    movenum += 1
                    #statprint("zamieniam", array[i], "i", array[size-2-qnum])
                    array[i], array[size-2-qnum] = array[size-2-qnum], array[i]
                    qnum += 1
                    continue
                compnum += 1
                #statprint("porównuje", array[i], "i", array[0])
                if compare(array[i], array[0]):
                    movenum += 1
                    #statprint("zamieniam", array[i], "i", array[1+pnum])
                    array[i], array[1+pnum] = array[1+pnum], array[i]
                    pnum += 1
                    i += 1
                    continue
            else:
                compnum += 1
                #statprint("porównuje", array[i], "i", array[0])
                if compare(array[i], array[0]):
                    movenum += 1
                    #statprint("zamieniam", array[i], "i", array[1+pnum])
                    array[i], array[1+pnum] = array[1+pnum], array[i]
                    pnum += 1
                    i += 1
                    continue
                compnum += 1
                #statprint("porównuje", array[size-1], "i", array[i])
                if compare(array[size-1], array[i]):
                    movenum += 1
                    #statprint("zamieniam", array[i], "i", array[size-2-qnum])
                    array[i], array[size-2-qnum] = array[size-2-qnum], array[i]
                    qnum += 1
                    continue
            i += 1
        movenum += 2
        #statprint("zamieniam", array[0], "i", array[pnum])
        array[0], array[pnum] = array[pnum], array[0]
        #statprint("zamieniam", array[size-1], "i", array[size-1-qnum])
        array[size-1], array[size-1-qnum] = array[size-1-qnum], array[size-1]
        subcmp1, submov1 = dpqsort(array[:pnum], compare)
        subcmp2, submov2 = dpqsort(array[pnum+1:size-1-qnum], compare)
        subcmp3, submov3 = dpqsort(array[size-qnum:size], compare)
        compnum += (subcmp1 + subcmp2 + subcmp3)
        movenum += (submov1 + submov2 + submov3)
        
    return compnum, movenum

def hybridquicksort(array, compare, switchthr=8):
    compnum = 0
    movenum = 0
    size = len(array)
    if size <= switchthr:
        return insertionsort(array, compare)
    if size > 1:
        movenum += 1
        #statprint("zamieniam", array[size//2], "i", array[size-1])
        array[size//2], array[size-1] = array[size-1], array[size//2]
        pivval = array[size-1]
        swapslot = 0
        for i in range(0,size-1):
            compnum += 1
            #statprint("porównuje", array[i], "i", pivval)
            if compare(array[i], pivval):
                movenum += 1
                #statprint("zamieniam", array[swapslot], "i", array[i])
                array[swapslot], array[i] = array[i], array[swapslot]
                swapslot += 1
        movenum += 1
        #statprint("zamieniam", array[swapslot], "i", array[size-1])
        array[swapslot], array[size-1] = array[size-1], array[swapslot]
        subcmp1, submov1 = hybridquicksort(array[:swapslot], compare, switchthr)
        subcmp2, submov2 = hybridquicksort(array[swapslot+1:], compare, switchthr)
        compnum += (subcmp1 + subcmp2)
        movenum += (submov1 + submov2)
    return compnum, movenum

                
            
sortmet = insertionsort
if args.type == "insert":
    sortmet = insertionsort
if args.type == "merge":
    sortmet = mergesort
if args.type == "quick":
    sortmet = quicksort
if args.type == "dualpivot":
    sortmet = dpqsort
if args.type == "hybridquick":
    sortmet = hybridquicksort
    
cmpmet = lambda x,y: x <= y

if args.comp == ">=":
    cmpmet = lambda x,y: x >= y
if args.comp == "<=":
    cmpmet = lambda x,y: x <= y

if args.stat == None:

    n = int(input())

    inpnum = [int(x) for x in input().split()]
    inpnum = inpnum[:n]

    tosort = np.array(inpnum)


    starttim = process_time()
    por, prze = sortmet(tosort,cmpmet)
    stoptim = process_time()
    statprint("Porównania:", por, "Przestawienia:", prze, "Czas:", stoptim-starttim)

    goodsort = True
    for i in range(1, len(tosort)):
        if not cmpmet(tosort[i-1], tosort[i]):
            goodsort = False

    if not goodsort:
        print("ZŁE SORTOWANIE")
        
    print(len(tosort))
    print(tosort)
else:
    nazwapliku = args.stat[0]
    k = int(args.stat[1])
    plik = open(nazwapliku, "w")
    rng = np.random.default_rng() #PCG64 lepszy niż MT19937
    
    for n in range(100, 10001, 100):
        for i in range(0,k):
            tosort = rng.integers(-10000, high=10000, size=n, dtype=np.int64, endpoint=True)
            algos = [quicksort, dpqsort, hybridquicksort]
            for algo in algos:
                mycopy = tosort.copy()
                starttim = process_time()
                cnum, mnum = algo(mycopy, lambda x,y: x <= y)
                endtim = process_time()
                plik.write(str(n) + " " + str(cnum) + " " + str(mnum) + " " + str(endtim - starttim) + " " + algo.__name__ + "\n")
    plik.close()
                
            

