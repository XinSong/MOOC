#coding=utf-8
import numpy as np
import heapq
import math

class Neighbor:
    def __init__(self, distance, y):
        self.distance = distance
        self.y = y
    def __gt__(self, other):
        return self.distance > other.distance
    def __eq__(self, other):
        return self.distance == other.distance
    def __lt__(self, other):
        return self.distance < other.distance
    def __ge__(self, other):
        return self.distance >= other.distance
    def __le__(self, other):
        return self.distance <= other.distance

class RBFNetwork:
    def __init__(self, k):
        self.k = k

    def train(self, trainData):
        self.data = trainData

    def test(self, testData):
        correct = 0.0
        error = 0.0
        for testRecord in testData:
            test_x = testRecord[0:9]
            test_y = testRecord[9]
            neighbors = []
            for trainRecord in self.data:
                train_x = trainRecord[0:9]
                distance = sum(np.square(test_x - train_x))
                y = trainRecord[9]
                if len(neighbors) < self.k:
                    heapq.heappush(neighbors, Neighbor(-distance,y))
                elif neighbors[0].distance < -distance:
                    heapq.heapreplace(neighbors, Neighbor(-distance, y))
            if test_y * sum([neighbor.y * math.exp(10*neighbor.distance) for neighbor in neighbors]) > 0:
                correct += 1.0
            else:
                error += 1.0
        return  correct/(correct+error)
                
def main():
    trainData = np.loadtxt('hw4_knn_train.dat')
    testData = np.loadtxt('hw4_knn_test.dat')
    knn = RBFNetwork(5)
    knn.train(trainData)
    print knn.test(testData)

if __name__=='__main__':
    main()
