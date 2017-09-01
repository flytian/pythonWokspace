# coding = utf-8

import trees
reload(trees)
dataSet, labels = trees.createDataSet()

myTree = trees.createTree(dataSet, labels)
print myTree
featLabels = ['no surfacing', 'flippers']
testVec = [1, 1]
print trees.classify(myTree,  featLabels, testVec)
