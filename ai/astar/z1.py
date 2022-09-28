import random

def parity(perm):
    result = 0
    for i in range(len(perm)):
        for j in range(i+1,len(perm)):
            if perm[i]>perm[j]:
                result +=1
                result %=2
    return result

def pos(idx):
    return (idx%4, idx//4)

def revpos(coords):
    return coords[1]*4+coords[0]

def manhatan(perm):
    total = 0
    for i in range(len(perm)):
        if perm[i] != 16:
            cpos = pos(i)
            tpos = pos(perm[i]-1)
            total += abs(tpos[0] - cpos[0]) + abs(tpos[1] - cpos[1])
    return total

def misplaced(perm):
    total = 0
    for i in range(len(perm)):
        if perm[i] != 16:
            if (perm[i] != i+1):
                total += 1
    return total

def neighbours(perm):
    holeidx = perm.index(16)
    hole = pos(holeidx)
    result = []
    if hole[0] > 0:
        newsol = perm.copy()
        leftidx = revpos((hole[0]-1, hole[1]))
        newsol[holeidx] = newsol[leftidx]
        newsol[leftidx] = 16
        result.append(newsol)
    if hole[0] < 3:
        newsol = perm.copy()
        rightidx = revpos((hole[0]+1, hole[1]))
        newsol[holeidx] = newsol[rightidx]
        newsol[rightidx] = 16
        result.append(newsol)
    if hole[1] > 0:
        newsol = perm.copy()
        upidx = revpos((hole[0], hole[1]-1))
        newsol[holeidx] = newsol[upidx]
        newsol[upidx] = 16
        result.append(newsol)
    if hole[1] < 3:
        newsol = perm.copy()
        downidx = revpos((hole[0], hole[1]+1))
        newsol[holeidx] = newsol[downidx]
        newsol[downidx] = 16
        result.append(newsol)
    return result


startstate = [x for x in range(1,17)]
while True:
    random.shuffle(startstate)
    if parity(startstate) == 0:
        break

#startstate = [1,2,3,4,5,6,7,8,9,10,11,16,13,14,15,12]
#startstate = [1,3,7,4,6,16,2,10,5,9,12,8,13,14,11,15]
startstate = [1,2,4,8,9,7,16,5,13,3,6,11,10,15,14,12]

came_from = {}
cost_so_far = {}
toexamine = []

toexamine.append((manhatan(startstate),startstate))
cost_so_far[tuple(startstate)] = 0
came_from[tuple(startstate)] = None
ended = False

while len(toexamine) > 0:
    if ended:
        break
    toexamine.sort(key=lambda x:x[0])
    nextnode = toexamine.pop(0)[1]
    for succ in neighbours(nextnode):
        newrealcost = cost_so_far[tuple(nextnode)] + 1
        mandist = manhatan(succ)
        print(newrealcost, mandist)
        if mandist == 0:
            ended = True
        if tuple(succ) not in cost_so_far or newrealcost < cost_so_far[tuple(succ)]:
            cost_so_far[tuple(succ)] = newrealcost
            came_from[tuple(succ)] = nextnode
            toexamine.append((newrealcost+mandist, succ))

curnod = [x for x in range(1,17)]
while curnod != startstate:
    print(curnod, cost_so_far[tuple(curnod)])
    curnod = came_from[tuple(curnod)]

