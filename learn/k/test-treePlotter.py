from k import treePlotter
from k import trees

myDat, labels = trees.createDataSet()

myTree = treePlotter.retrieveTree(0)
# treePlotter.createPlot(myTree)

trees.storeTree(myTree, "classifierStorage.txt")

print(trees.grabTree("classifierStorage.txt"))

# print(trees.classify(myTree, labels, [1,0]))

# print(trees.classify(myTree, labels, [1,1]))