# coding=UTF-8
from math   import log
import operator
# intiate the DataSet
def createDataSet():
    dataSet = [   # 列表嵌列表
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no surfacing', 'flippers'] # 特征 的 名字
    return dataSet, labels

# calculate the shannon entropy of the dataSet
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)  # 列表长度
    labelCounts = {}  # 字典
    for featVec in dataSet:
        currentLabel = featVec[-1]  # 当前列表, [1, 1, 'yes'] 最后一个， 'yes'
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0   # 用来 初始 化 字典
        labelCounts[currentLabel] += 1  # 对 每 一个 dataSet中 的 lable 计数
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries  # 该 类别 的 概率
        shannonEnt -= prob * log(prob, 2)  # 所有类别 所有 可能值 可能 出现 的 期望 值
    return shannonEnt


# [[1, 'yes'], [1, 'yes'], [0, 'no'], [0, 'no']]
#   指定 某列 值  来 分 割 数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []   # define a list
    for featVec in dataSet:   # 对于  dataSet 中 的 每 一个 列表
        if featVec[axis] == value:   # axis列元素 值 若 等于 value
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)   # 好像  去 除了 axis 列
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1  # 特征 数量
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):    # 闭开区间， 默认 从 0 开始
        featList = [example[i] for example in dataSet]  # 取到特征列表，（去除 'yes' 那列元素）
        uniqueVals = set(featList)  # 得到 set， 独 一 无二 的 值 集合
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)  # 对于每 一个 特征 列 ，用 set 里的 value 集合 分割
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy  # 此值越大 ，特征 越 好
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return  bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    # 按 count 从 大 到小 排序 reverse
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return  sortedClassCount[0][0]  # 返回 数 最多 的 那个

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]  # 所有 类别 的 列表
    if classList.count(classList[0] ) == len(classList):  # 只有 一类
        return classList[0]
    if len(dataSet[0]) == 1:  # 数据集 没有 特征 了 停止 分割
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]  # 返回 最好 特征 的 名字
    myTree = {bestFeatLabel:{}}  # 初始 化 决策 树
    del(labels[bestFeat])  # 删除 该 特征 名
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:  # 递归 创建 子树
        subLables = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLables)
    return myTree

def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]  # 同样 是 个字典

    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]

    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):  # 递归
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:  # 得到 类别
        classLabel = valueOfFeat
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)









