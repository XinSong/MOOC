#coding=utf-8
import numpy as np
import random

def logit(s):
    return 1.0/(1.0 + np.exp(-s))

def derivative_tanh(s):
    return 4 * logit(2*s)*(1-logit(2*s)) 

class NeuralNet:
    def __init__(self, d=2, eta=0.1, r=0.1, T = 50000):
        self.d = d
        self.eta = eta
        self.r = r
        self.T = T
    
    def train(self, trainData):
        #Network Structure: d-8-3-1
        recordNum = len(trainData)
        trainData = np.hstack(([[1]]*recordNum, trainData))
        self.w1 = np.random.uniform(-self.r, self.r, (self.d + 1, 8))
        self.w2 = np.random.uniform(-self.r, self.r, (8 + 1,3))
        self.w3 = np.random.uniform(-self.r, self.r, (3 + 1,1))
        for t in xrange(0, self.T):
            n = random.randint(0,recordNum-1)
            x0 = trainData[n,0:3]
            y = trainData[n, 3]
            s1 = np.dot(self.w1.T, x0)
            s1.shape = (8,1)
            x =  np.tanh(s1)
            x1 = np.vstack(([1], x))
            x1.shape = (8+1,1)
            s2 = np.dot(self.w2.T, x1)
            s2.shape = (3,1)
            x = np.tanh(s2)
            x2 = np.vstack(([1], x))
            s3 = np.dot(self.w3.T, x2)
            yPredict = np.tanh(s3)
            e = y - yPredict
            delta3 = -2 * (y - yPredict) * derivative_tanh(s3)
            self.w3 = self.w3 - self.eta * np.dot(x2,delta3.T)
            delta2 = delta3 * self.w3[1:] * derivative_tanh(s2)
            self.w2 = self.w2 - self.eta * np.dot(x1, delta2.T)
            delta1 = np.dot(self.w2[1:], delta2) * derivative_tanh(s1)
            x0.shape = (self.d+1,1) 
            self.w1 = self.w1 - self.eta * np.dot(x0, delta1.T)

    def test(self, testData):
        recordNum = len(testData)
        testData = np.hstack(([[1]]*recordNum, testData))
        X = np.matrix(testData[:,0:3])
        Y = np.matrix(testData[:, 3]).T
        S =  np.tanh(X * self.w1) 
        S = np.hstack(([[1]]*len(S),S))
        S = np.tanh(S * self.w2)
        S = np.hstack(([[1]]*len(S),S))
        YPredict = np.tanh(S* self.w3)
        print 'sum=',sum(np.square(Y - YPredict))
        return 1.0/recordNum * sum(np.square(Y - YPredict))

def main():
   trainData = np.loadtxt('hw4_nnet_train.dat')
   testData = np.loadtxt('hw4_nnet_test.dat')
   d = 2
   r = 0.1
   eta = 0.01
   T = 50000
   neuralNet = NeuralNet(d, eta, r, T)
   for i in range(0,10):
       neuralNet.train(trainData)
       print neuralNet.test(testData)

if __name__=='__main__':
    main()
