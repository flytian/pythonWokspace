# coding=utf-8
import matplotlib.pyplot as plt

# dict用来直接定义字典
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
# 定义 箭头 样式
arrow_args = dict(arrowstyle="<-")
# 从 第一 层 子树 递归计算 叶子 节点 位置
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]  #最初 只有 一个键 ，'no surfacing'
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':  # 判断 元素 类型
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

# 从 第一 层 子树 递归 计算树的深度
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

# 绘制 箭头， 并 绘制 节点 样式
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',  # 不是 赋值 语句 ， 是 map 里面的 成员
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

# 绘制 箭头 上的 特征 的 取值
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)
# 定义终点位置, 绘制箭头线和 节点 , 绘制 箭头文字, 改变纵轴坐标， 绘制下一层 子树
#                        键值为字典，则递归绘制子树
#                        键值为类别，则   改变横轴坐标， 绘制箭头线和 节点 , 绘制 箭头文字
# 还原 纵轴 坐标
def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
   # depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)  # 先抵消 1.0 /2.0/plotTree.totalW 再 平移  float(numLeafs)/2.0/plotTree.totalW 【其实分成了 2* 份 】

    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    plotMidText(cntrPt, parentPt, nodeTxt)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)  # cntrPt 成了 父 节点， 连到 (plotTree.xOff, plotTree.yOff) 画 一个 箭头 叶子 节点
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
#  定义 绘图对象 ，生成图对象， 定义 根节点 位置 信息，开始 绘制 树形图
def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=True, **axprops)  # 字典 合并
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    # 想把多个语句写在同一行，分号就是必需的
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0  # xOff 需要 所有 节点 位置  左偏 一点，实现 图 的 向 左 偏 移
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()

def retrieveTree(i):
    listOfTrees = [  # 树 的 列表
        {'no surfacing': {0: {'flippers': {1: 'no', 0: 'yes'}},  1: 'no'}},
        {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}} }
    ]

    return listOfTrees[i]

