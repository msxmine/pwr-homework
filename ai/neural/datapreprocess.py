import cv2
import numpy as np

griddim = 0.081
gridstartx = 0.15
gridstarty = 0.057


im = cv2.imread("mysamples.png")
dims = im.shape
samples = []

for i in range(10):
    digit = i
    dstartx = int(dims[1]*(gridstartx+i*griddim))
    dendx = int(dims[1]*(gridstartx+(i+1)*griddim))
    digitsamples = []
    for j in range(15):
        sample = j
        dstarty = int(dims[1]*(gridstarty+j*griddim))
        dendy = int(dims[1]*(gridstarty+(j+1)*griddim))
        im = cv2.rectangle(im, (dstartx, dstarty), (dendx, dendy), (0,0,0), 4)
        digitsamples.append(im[(dstarty+20):(dendy-20), (dstartx+20):(dendx-20)])
    samples.append(digitsamples)

finaldata = []
finallabels = []
for i in range(10):
    for j in range(15):
        hsv = cv2.cvtColor(samples[i][j], cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, (95,15,0), (135,255,255))
        maskpad = int(max(mask1.shape[0], mask1.shape[1])*0.2)
        mask1 = cv2.copyMakeBorder(mask1, maskpad, maskpad, maskpad, maskpad, cv2.BORDER_CONSTANT, value=(0,0,0))
        dilation_kernel = np.ones((5,5), np.uint8)
        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, dilation_kernel)
        mask1 = cv2.dilate(mask1, dilation_kernel, iterations=2)
        contours, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=lambda x: cv2.contourArea(x), reverse=True)
        for contidx in range(1,len(contours)):
            cv2.drawContours(mask1, contours, contidx, (0,0,0), -1)
        bbox = cv2.boundingRect(mask1)
        maxdim = max(bbox[2], bbox[3])
        marginx = int( (maxdim-bbox[2])/2.0 )
        marginy = int( (maxdim-bbox[3])/2.0 )
        isolated = mask1[(bbox[1]-marginy):(bbox[1]+bbox[3]+marginy), (bbox[0]-marginx):(bbox[0]+bbox[2]+marginx)]
        isolated = cv2.resize(isolated, (20,20), interpolation=cv2.INTER_LINEAR)
        final = cv2.copyMakeBorder(isolated, 4,4,4,4, cv2.BORDER_CONSTANT, value=(0,0,0))
        finaldata.append(np.array(final))
        finallabels.append(i)

finaldata = np.array(finaldata)
finallabels = np.array(finallabels)
mydataset = open("mydataset.npy","wb")
np.save(mydataset, finaldata)
np.save(mydataset, finallabels)
mydataset.close()
