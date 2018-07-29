from numpy import *
from math import log
import operator


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inx, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    # 计算距离
    diffMat = tile(inx, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    # 选择距离最小的k个点
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel , 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), ket=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]