from k import trees
from k import treePlotter
from strategy import lensesDict
fr = open("F:\data\machine learning\glasses\lenses.data")
lenses = [inst.strip().split("  ") for inst in fr.readlines()]

for inst in lenses:
    inst[0] = lensesDict.ageToString(inst[0])
    inst[1] = lensesDict.spectacleToString(inst[1])
    inst[2] = lensesDict.astigmaticToString(inst[2])
    inst[3] = lensesDict.tearToString(inst[3])
    inst[4] = lensesDict.classToString(inst[4])

lensesLabels = ["age", "prescript", "astigmatic", "tearRate"]

lensesTree = trees.createTree(lenses, lensesLabels)

print(lensesTree)

treePlotter.createPlot(lensesTree)
