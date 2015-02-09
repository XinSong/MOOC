#coding=utf-8
import sys
import pandas as pd
import numpy as np

class DecisionTreeNode:
    def __init__(self, threshold=None, index=None, left=None, right=None):
        self.threshold = threshold
        self.index = index
        self.left = left
        self.right = right
    def predict(self, x):
        if x[self.index] <= self.threshold:
            return self.left
        else:
            return self.right

def impurity(threshold, index, trainData):
    posPre = 0.0
    negPre = 0.0
    posPost = 0.0
    negPost = 0.0
    recordNum = len(trainData)
    for i in range(0, recordNum):
        if trainData.irow(i)[index] <= threshold:
            if trainData.irow(i)['y'] == 1:
                posPre += 1
            else:
                negPre += 1
        else:
            if trainData.irow(i)['y'] == 1:
                posPost += 1
            else:
                negPost += 1
    preNum = posPre + negPre
    postNum = posPost + negPost

    return preNum/recordNum * gini(posPre, negPre) + postNum/recordNum * gini(posPost, negPost)

def gini(posNum, negNum):
    if posNum==0 or negNum==0:
        return 0
    else:
        return 1 - (posNum/(posNum + negNum))**2 - (negNum/(posNum + negNum))**2

def test(rootDTree, testData):
    correct = 0.0
    error = 0.0
    recordNum = len(testData)
    for i in range(0, recordNum):
        if rootDTree.predict(testData.ix[i]) == testData.ix[i, 'y']:
            correct += 1.0
        else:
            error += 1.0
    return (correct, error)

def get_label(trainData):
    value_count = trainData['y'].value_counts()
    if -1 not in value_count:
        return 1
    elif 1 not in value_count:
        return -1

    if value_count[-1] > value_count[1]:
        return -1
    else:
        return 1

def train(trainData):
    recordNum = len(trainData)
    minGini = float('inf')
    for index in ('x1','x2'):
        trainData.sort(index, inplace = True)
        for i in range(0, recordNum):
            j = i + 1
            while j < recordNum and trainData.irow(i)['y'] == trainData.irow(j)['y']:
                j += 1
            if j == recordNum:
                threshold = float('inf')
            else:    
                threshold = (trainData.irow(j)[index] + trainData.irow(j-1)[index])/2.0
            gini = impurity(threshold, index, trainData)
            if minGini > gini:
                minGini = gini
                minIndex = index
                leftData = trainData[0:j]
                rightData = trainData[j:]
                minThreshold = threshold 
    
    left = get_label(leftData)
    right = get_label(rightData)
    root = DecisionTreeNode(minThreshold, minIndex, left, right)
    return root

def BFS(root):
    nodeList = []
    nodeList.append(root)
    count = 0
    while nodeList:
        node = nodeList[0]
        nodeList = nodeList[1:]
        if node.left:
            nodeList.append(node.left)
            count += 1
        if node.right:
            nodeList.append(node.right)
    return count

def randomForestTest(forest, testData):
    correctTotal = 0.0
    errorTotal = 0.0
    for i in range(0,len(testData)):
        correct = 0.0
        error = 0.0 
        for tree in forest:
            if tree.predict(testData.irow(i)) == testData.ix[i, 'y']:
                correct += 1.0
            else:
                error += 1.0
        if correct >= error:
            correctTotal += 1.0 
        else:
            errorTotal += 1.0
    return (correctTotal, errorTotal)
        
def main():
    trainData = pd.read_table('hw3_train.dat', names=['x1','x2','y'], sep=' ')
    testData = pd.read_table('hw3_test.dat', names=['x1','x2','y'], sep=' ')
    
    recordNum = len(trainData)
    randomForest = []
    for T in range(0,300):
        index = np.random.randint(0,recordNum,recordNum)
        trainBagData = trainData.reindex(index)
        dTree = train(trainBagData)     
        randomForest.append(dTree)
#        correct, error = test(dTree,trainData)
#        E_in = error/(correct + error)
        print T  #,E_in
    print randomForestTest(randomForest, trainData)
    print randomForestTest(randomForest, testData)

if __name__=='__main__':
    main()
