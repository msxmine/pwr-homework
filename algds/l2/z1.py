#!/usr/bin/python3
import argparse
import numpy as np
import sys
from time import process_time

parser = argparse.ArgumentParser(description="Zadanie 1")
parser.add_argument("--type", choices=["insert", "merge", "quick"], required=True)
parser.add_argument("--comp", choices=[">=", "<="], required=True)
args = parser.parse_args()

n = int(input())

inpnum = [int(x) for x in input().split()]
inpnum = inpnum[:n]

tosort = np.array(inpnum)

def statprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def insertionsort(array, compare):
    compnum = 0
    movenum = 0
    for idx in range(1,len(array)):
        for pos in range(idx,0,-1):
            compnum += 1
            statprint("porównuje", array[pos], "i", array[pos-1])
            if compare(array[pos], array[pos-1]):
                movenum += 1
                statprint("zamieniam", array[pos], "i", array[pos-1])
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
                    statprint("zapisuje", array[i], "do tablicy tymczasowej")
                    result[pos] = array[i]
                break
            if ridx == size:
                for pos,i in enumerate(range(lidx, mid),idx):
                    movenum += 1
                    statprint("zapisuje", array[i], "do tablicy tymczasowej")
                    result[pos] = array[i]
                break
            compnum += 1
            statprint("porównuje", array[lidx], "i", array[ridx])
            if compare(array[lidx], array[ridx]):
                movenum += 1
                statprint("zapisuje", array[lidx], "do tablicy tymczasowej")
                result[idx] = array[lidx]
                lidx += 1
            else:
                movenum += 1
                statprint("zapisuje", array[ridx], "do tablicy tymczasowej")
                result[idx] = array[ridx]
                ridx += 1
        statprint("Kopiuje tablice tymczasowa do wyniku ,wielkosc:", size)
        array[:] = result
    return compnum, movenum

def quicksort(array, compare):
    compnum = 0
    movenum = 0
    size = len(array)
    if size > 1:
        movenum += 1
        statprint("zamieniam", array[size//2], "i", array[size-1])
        array[size//2], array[size-1] = array[size-1], array[size//2]
        pivval = array[size-1]
        swapslot = 0
        for i in range(0,size-1):
            compnum += 1
            statprint("porównuje", array[i], "i", pivval)
            if compare(array[i], pivval):
                movenum += 1
                statprint("zamieniam", array[swapslot], "i", array[i])
                array[swapslot], array[i] = array[i], array[swapslot]
                swapslot += 1
        movenum += 1
        statprint("zamieniam", array[swapslot], "i", array[size-1])
        array[swapslot], array[size-1] = array[size-1], array[swapslot]
        subcmp1, submov1 = quicksort(array[:swapslot], compare)
        subcmp2, submov2 = quicksort(array[swapslot+1:], compare)
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
    
cmpmet = lambda x,y: x <= y

if args.comp == ">=":
    cmpmet = lambda x,y: x >= y
if args.comp == "<=":
    cmpmet = lambda x,y: x <= y


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
