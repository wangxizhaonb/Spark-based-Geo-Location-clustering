from pyspark import SparkContext
import numpy as np
import sys
from math import sqrt,pow
from geopy.distance import great_circle

def closestPoint(p, centers, func):
    # return the index of the closest center
    # p         point (x,y)
    # centers   [(x,y)....]
    # func      distance function
    data = []
    for c in centers:
        data.append(func(p,c))
    data = np.asarray(data)
    return np.argmin(data)

def addPoints(p1, p2):
    # return sum of two point
    # p         point (x,y)
    return p1[0] + p2[0], p1[1] + p2[1]

def EuclideanDistance(p1, p2):
    # return Euclidean Distance of two points
    # p         point (x,y)
    return sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))

def GreatCircleDistance(p1,p2):
    # return Great Circle Distance of two points
    # p         point (x,y)
    return great_circle(p1, p2).miles

def getDiff(newCenters, centers):
    # return the sum of distance of new and old centers
    # newCenters     [[i, (x,y)]...]
    # centers        [(x,y)....]
    sum = 0.0
    for (i, p) in newCenters:
        sum += EuclideanDistance(centers[i],p)
    return sum



def kmeans(data, tol, func, k):
    centers = data.takeSample(False, k)
    diff = 1.0
    while diff > tol:
        cluster = data.map(lambda p: (closestPoint(p, centers, func), [p, 1])) # (k, [(x,y),1]) k=cluster 1= count
        newCenters = cluster.reduceByKey(lambda p1,p2: (addPoints(p1[0],p2[0]), p1[1]+p2[1]) # (k, ((sum x, sum y), count))
                                 ).map(lambda l: (l[0], np.array(l[1][0]) / l[1][1])).collect() #  (k, (x,y))
        diff = getDiff(newCenters, centers)
        for (i, newCt) in newCenters:
            centers[i] = newCt

    clusters = data.map(lambda  p: (closestPoint(p, centers, func), p)).groupByKey().map(lambda l:(l[0], list(l[1])))
    return centers, clusters

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage k_means.py input output func k")
        exit(-1)
    sc = SparkContext()
    infile = sys.argv[1]
    # handle different format of input data,
    # we nemed the 3 data set provied by course data1-3
    # our realword application data is data4
    if infile == "data1":
        data = sc.textFile(infile).filter(lambda l: len(l) > 0).map(lambda o: o[1: len(o) - 1]).map(lambda o: o.split(',')).map(lambda o: (float(o[0]), float(o[1]))).cache()
    elif infile == "data2":
        data = sc.textFile(infile).filter(lambda l:len(l) > 0).map(lambda o: o.split('\t')).map(lambda o: (float(o[0]), float(o[1]))).cache()
    elif infile == "data3":
        data = sc.textFile(infile).filter(lambda l:len(l) > 0).map(lambda o: o.split(' ')).map(lambda o: (float(o[0]), float(o[1]))).cache()
    elif infile == "data4":
        data = sc.textFile(infile).filter(lambda l: len(l) > 0).map(lambda l: l.split(",")).map(lambda l: (float(l[5]), float(l[6]))).cache()
    else:
        print("wrong input,should be data1-4")
        exit(-1)

    if sys.argv[3] == "eu":
        func = EuclideanDistance
    elif sys.argv[3] == "gc":
        func = GreatCircleDistance
    else:
        print("wrong function shoule be eu or gc")
        exit(-1)
    centers, clusters = kmeans(data, 0.01, func, int(sys.argv[4]))
    clusters.saveAsTextFile(sys.argv[2])
    np.savetxt('cp.txt', centers, fmt="%.18f %.18f")
    sc.stop()

