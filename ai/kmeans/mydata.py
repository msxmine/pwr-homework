import numpy as np
from collections import defaultdict

mydataset = open("./mydataset.npy", "rb")
mydata = np.load(mydataset)
mylabels = np.load(mydataset)
mydataset.close()
mydata = np.reshape(mydata/255.0, (len(mydata), 28*28))

mycentroids = open("./centroidyd.npy", "rb")
centers = np.load(mycentroids)
mycentroids.close()

def disq(p1, p2):
    return np.sum((p1-p2)**2)

def accuracy(points, centers, labels):
    all = 0
    good = 0
    point_dict = defaultdict(list)
    for pidx, point in enumerate(points):
        distances = np.array([disq(point, x) for x in centers])
        point_dict[np.argmin(distances)].append(labels[pidx])
    for cluster in point_dict:
        labelsgr, counts = np.unique(point_dict[cluster], return_counts=True)
        bestclass = labelsgr[np.argmax(counts)]
        for label in point_dict[cluster]:
            all += 1
            if label == bestclass:
                good += 1
    return (good, all)

def assigned(points, centers, labels):
    result = np.zeros((len(centers),10), dtype=np.int64)
    for pidx, point in enumerate(points):
        distances = np.array([disq(point, x) for x in centers])
        bestclust = np.argmin(distances)
        reallabel = labels[pidx]
        result[bestclust][reallabel] += 1
    return result

def inertia(points, centers):
    inertiaret = 0.0
    for point in points:
        distances = np.array([disq(point, x) for x in centers])
        inertiaret += np.amin(distances)
    return inertiaret

print(accuracy(mydata, centers, mylabels), inertia(mydata, centers))
astab = assigned(mydata, centers, mylabels)
for clusteridx in range(len(astab)):
    for realdigit in range(len(astab[clusteridx])):
        print(astab[clusteridx][realdigit], ", ", end="")
    print("")


