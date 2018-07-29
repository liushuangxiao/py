from myBayes import bayes

listOPosts, listClass = bayes.loadDataSet()
myVocabList = bayes.createVocabList(listOPosts)
print(myVocabList)

trainMat = []

for postinDoc in listOPosts :
    trainMat.append(bayes.setOfWordd2Vec(myVocabList, postinDoc))

p0V, p1V, pAb = bayes.trainNB0(trainMat, listClass)

# print(pAb)
# print(p0V)
# print(p1V)

bayes.testingNB()

