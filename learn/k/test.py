from k import trees
from k import treePlotter


myDat, labels = trees.createDataSet()

# rtn = trees.chooseBestFeatureToSplite(myDat)
# print(rtn)

myTree = trees.createTree(myDat, labels)
# print(myTree)

# treePlotter.createPlot()
numLeafs = treePlotter.getNumLeafs(myTree)
treeDepth = treePlotter.getTreeDepth(myTree)
print(numLeafs)
print(treeDepth)
