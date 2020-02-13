import sys
from pyspark import SparkContext

devicestatus = sc.textFile("/final/devicestatus.txt")
seperateFile = devicestatus.map(lambda line: (line[19],line)).map(lambda l: l[1].split(l[0]))
checkNumber = seperateFile.filter(lambda count: len(count) == 14)
changeOrder = checkNumber.map(lambda vals: (float(vals[12]), float(vals[13]),vals[0], vals[1], vals[3]))
zeroPoint = changeOrder.filter(lambda latlong: (latlong[0] != 0 and latlong[1] != 0))
changeFormat = zeroPoint.map(lambda mm:(mm[0],mm[1],mm[2],mm[3].split(" ")[0],mm[3].split(" ")[1],mm[4])).map(lambda line:(line[0],line[1],line[2],"manufacturer "+line[3],"model "+line[4],line[5]))


