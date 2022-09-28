import matplotlib.pyplot as plt
import numpy as np
import math

plik = open("./badheur.txt", "r")
lines = plik.readlines()
visited = {}
path = {}

vrv = []
prv = []

for rawline in lines:
    line = rawline.split()
    vn = int(line[0])
    pl = int(line[1])
    if vn != -1:
        vrv.append(vn)
        prv.append(pl)
    if vn in visited:
        visited[vn] += 1
    else:
        visited[vn] = 1
    if pl in path:
        path[pl] += 1
    else:
        path[pl] = 1

print(sum(vrv)/len(vrv))
print(sum(prv)/len(prv))

visitedx = []
visitedy = []
for elem in visited:
    if elem != -1:
        visitedx.append(elem)
        visitedy.append(visited[elem])

pathx = []
pathy = []
for elem in path:
    if elem != -1:
        pathx.append(elem)
        pathy.append(path[elem])

#plt.bar(pathx, pathy)
plt.scatter(prv, [math.log(x) for x in vrv])
plt.ylabel("log(odwiedzone)")
plt.xlabel("Długość rozwiązania")
plt.show()

