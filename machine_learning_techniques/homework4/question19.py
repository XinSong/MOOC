#coding=utf-8
import numpy as np
import random

def distance(x1,x2):
    return sum(np.square(x1-x2))

def knn(data, k):
    recordNum = len(data)
    cluster = np.array([0] *recordNum)
    u = random.sample(data,k)
    converge = False
    while not converge:
        converge = True
        for i in range(0,len(data)):
            leastDistance = float('inf')
            leastCluster = 0
            for j in range(0,len(u)):
                _distance = distance(data[i], u[j])
                if leastDistance > _distance:
                    leastDistance = _distance
                    leastCluster = j
            if cluster[i] != leastCluster:
                cluster[i] = leastCluster
                converge = False
        for i in range(0, len(u)):
            u[i] = np.sum(data[cluster==i],axis=0)/sum(cluster==i)
    e_in = 0.0
    for i in range(0, len(data)):
        e_in += sum(np.square(data[i] - u[cluster[i]]))
    e_in /= recordNum
    return e_in

def main():
    data = np.loadtxt('hw4_kmeans_train.dat')
    k = 10 
    sum = 0.0
    for i in range(0,100):
        sum +=  knn(data,k)

    sum /=100
    print sum
    
if __name__=='__main__':
    main()
