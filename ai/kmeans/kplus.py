import numpy as np
import tensorflow.keras.datasets as ds
from collections import defaultdict
import matplotlib.pyplot as plt

rng = np.random.default_rng()

def disq(p1, p2):
    return np.sum((p1-p2)**2)

def initializeplus(data, knum):
    centers = np.zeros((knum, 28*28))
    centers[0] = rng.choice(data)
    mindist = np.array([disq(centers[0], x) for x in data])
    for kidx in range(1,knum):
        pnorm = mindist / np.sum(mindist)
        centers[kidx] = rng.choice(data, p=pnorm)
        mindist = np.array([ min(x, disq(centers[kidx], data[xidx])) for xidx, x in enumerate(mindist)])
    return centers

def assigncluster(points, centers):
    point_dict = defaultdict(list)
    for point in points:
        distances = np.array([disq(point, x) for x in centers])
        point_dict[np.argmin(distances)].append(point)
    return point_dict

def calcmeans(point_dict, knum):
    return np.array([np.mean(point_dict[k], axis=0) for k in range(knum)])

def inertia(point_dict, centers):
    inertiaret = 0.0
    for cidx, center in enumerate(centers):
        inertiaret += np.sum([disq(center,point) for point in point_dict[cidx]])
    return inertiaret

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


(x_train, y_train), (x_test, y_test) = ds.mnist.load_data()
data = np.reshape(x_train/255.0, (len(x_train), 28*28))

classesnum = 12

centers = initializeplus(data, classesnum)
for e in range(25):
    pdic = assigncluster(data, centers)
    centers = calcmeans(pdic, classesnum)
    print(inertia(pdic, centers))
    print(accuracy(data, centers, y_train))


centersimg = np.reshape(centers, (classesnum,28,28))
centersimg = centersimg*255
fig, axs = plt.subplots(1,classesnum)
for classidx in range(classesnum):
    axs[classidx].imshow(centersimg[classidx], cmap="gray_r", vmin=0, vmax=255)

astab = assigned(data, centers, y_train)
for clusteridx in range(len(astab)):
    for realdigit in range(len(astab[clusteridx])):
        print(astab[clusteridx][realdigit], ", ", end="")
    print("")
plt.show()

plik = open("./centroidymulti.npy", "wb")
np.save(plik, centers)
plik.close()
