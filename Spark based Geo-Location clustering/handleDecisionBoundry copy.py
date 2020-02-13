import numpy as np
import pandas as pd
from math import radians, sin, cos
from geopy.distance import great_circle

def euclidean_distance(p1, p2):
    """
    calculate the eculidean distance between two points
    :param p1: pair of coordinate
    :param p2: pair of coordinate
    :return: eculidean distance
    """
    return np.sqrt(np.sum((np.array(p2) - np.array(p1)) ** 2, axis=1))

def closest_point(p, ps, m):
    """
    given a (latitude/longitude) point
    and an array of current center points
    returns the index in the array of
    the center closest to the given poin
    :param p:  given point
    :param ps: center points
    :param m:  distance functions
    :return:   the index of the closest center point
    """
    ps = np.asarray(ps)
    # print(m(p, ps))
    return np.argmin(m(p, ps))

def closest_point2(p, ps, m):
    """
    given a (latitude/longitude) point
    and an array of current center points
    returns the index in the array of
    the center closest to the given poin
    :param p:  given point
    :param ps: center points
    :param m:  distance functions
    :return:   the index of the closest center point
    """
    # ps = np.asarray(ps)
    data = []
    for c in ps:
        data.append(m(p,c))
    data = np.asarray(data)
    # print(m(p, ps))
    return np.argmin(data)

def great_circle_distance(p1, p2):
    lat1, lon1 = radians(p1[1]), radians(p1[0])
    lat2, lon2 = np.radians(p2[:, 1]), np.radians(p2[:, 0])

    sin_lat1, cos_lat1 = sin(lat1), cos(lat1)
    sin_lat2, cos_lat2 = np.sin(lat2), np.cos(lat2)

    d_lon = np.subtract(lon2, lon1)
    cos_d_lon, sin_d_lon = np.cos(d_lon), np.sin(d_lon)

    return np.arctan2(np.sqrt((cos_lat2 * sin_d_lon) ** 2 +
                              (cos_lat1 * sin_lat2 -
                               sin_lat1 * cos_lat2 * cos_d_lon) ** 2),
                      sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_d_lon)

def GreatCircleDistance(from_point, to_point):
    return great_circle(from_point, to_point).miles

def generate():
    file = open("cp.txt", 'r')
    centers = []
    data = []
    i = 0
    l = file.readline()

    centerData = []
    eu = euclidean_distance
    gc = great_circle_distance
    gc2 = GreatCircleDistance
    while l:
        p = l.split(" ")
        centers.append([float(p[0]),float(p[1])])
        centerData.append([float(p[0]),float(p[1]),i,1])
        i+=1
        l = file.readline()
    # print(centers)

    # for i in np.arange(25, 49, 0.12):
    #     for j in np.arange(-130, -67, 0.12):
    #         # print(closest_point([i,j], centers, euclidean_distance))
    #         data.append([i,j,closest_point([i,j], centers,  gc),0.01])

    for i in np.arange(-90, 90, 0.5):
        for j in np.arange(-180, 180, 0.5):
            # print(closest_point([i,j], centers, euclidean_distance))
            data.append([i,j,closest_point2([i,j], centers, gc2),0.01])

    # for i,j in centers:
    #     data.append([i,j,closest_point([i,j], centers, eu),1])

    arr = [[], [], [],[]]  # lat ,lon, center ,isCenter


    # print(data)
    for l in data:
        for i in range(4):
            arr[i].append(l[i])
    # 字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'lat': arr[0], 'long': arr[1], 'cluster': arr[2], 'isCenter': arr[3]})

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("data1Boundry.csv", index=False, sep=',')

    arr = [[], [], [], []]

    for l in centerData:
        for i in range(4):
            arr[i].append(l[i])
    # 字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'lat': arr[0], 'long': arr[1], 'cluster': arr[2], 'isCenter': arr[3]})

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("centerData.csv", index=False, sep=',')






generate()