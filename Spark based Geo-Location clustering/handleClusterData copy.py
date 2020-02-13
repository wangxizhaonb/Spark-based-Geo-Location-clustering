import pandas as pd

def trim(s):
    s = s[1:-2]
    # print(s)
    s=s.split(",",1)
    k = int(s[0])
    arr = s[1][3:-2]
    points = arr.split("), (")
    # print(arr)
    # print(points)
    data = []
    i = 0
    for point in points:
        i += 1
        # if i % 10 != 1:
        #     continue
        p = point.split(",")
        data.append([float(p[0]),float(p[1]),k,0.01])
    # print(data)
    return data

def toCsv(num = 100):
    arr = [[], [], [],[]]  # lat ,lon, center ,isCenter
    data = readFile("data1_1",num)
    data.extend(readFile("data1_2",num))

    # file = open("cp.txt", 'r')
    # l = file.readline()
    # i = 0
    # while l:
    #     p = l.split(" ")
    #     data.append([float(p[0]), float(p[1]), i, 1])
    #     i += 1
    #     l = file.readline()
    #
    # file.close()
    # print(data)
    for l in data:
        for i in range(4):
            arr[i].append(l[i])
    # 字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'lat': arr[0], 'long': arr[1], 'cluster': arr[2], 'isCenter': arr[3]})

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("data1.csv", index=False, sep=',')

def readFile(file, num):
    data = []

    file = open(file, 'r')
    l = file.readline()
    i = 0
    if num > 0:
        while l and i < num:
            i += 1
            data.extend(trim(l))
            # print(trim(l))
            l = file.readline()
    else:
        while l:
            i += 1
            data.extend(trim(l))
            # print(trim(l))
            l = file.readline()
    # print(data)

    file.close()
    return data


toCsv(-1)
# readFile(-1)