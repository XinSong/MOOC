#coding=utf-8
import numpy as np
import random

def logit(s):
    return 1.0/(1.0 + np.exp(-s))

def derivative_tanh(s):
    return 4 * logit(2*s)*(1-logit(2*s)) 

class NeuralNet:
    def __init__(self, structure, eta=0.1, r=0.1, T = 50000):
        self.d, self.M, self.o = structure
        self.eta = eta
        self.r = r
        self.T = T
    
    def train(self, trainData):
        recordNum = len(trainData)
        trainData = np.hstack(([[1]]*recordNum, trainData))
        self.w1 = np.random.uniform(-self.r, self.r, (self.d + 1, self.M))
        self.w2 = np.random.uniform(-self.r, self.r, (self.M + 1,1))
        for t in xrange(0, self.T):
      #      if t % 10000 == 0:
      #          print t
            n = random.randint(0,recordNum-1)
            x0 = trainData[n,0:3]
            y = trainData[n, 3]
            s1 = np.dot(self.w1.T, x0)
            s1.shape = (self.M,1)
            x =  np.tanh(s1)
            x1 = np.vstack(([1], x))
            x1.shape = (self.M+1,1)
#            print 'w2.shape=',self.w2.shape,self.w2
#            print 'x1.shape=',x1.shape,x1
            s2 = np.dot(self.w2.T, x1)
            yPredict = np.tanh(s2)
            e = y - yPredict
            delta2 = -2 * (y - yPredict) * derivative_tanh(s2)
            x = x1 * delta2
            self.w2 = self.w2 - self.eta * x1 * delta2
#            if t==0:
#                print "delta2.shape=",delta2.shape
#                print "w2.shape=",self.w2.shape
#                print derivative_tanh(s1).shape
#            print 'w2.shape=',self.w2.shape
#            print 's1.shape=',s1.shape
            delta1 = delta2 * self.w2[1:] * derivative_tanh(s1)
            x0.shape = (3,1) 
#            print 'delta1.shape=',delta1.shape
            self.w1 = self.w1 - self.eta * np.dot(x0, delta1.T)

    def test(self, testData):
        recordNum = len(testData)
        testData = np.hstack(([[1]]*recordNum, testData))
        X = np.matrix(testData[:,0:3])
        Y = np.matrix(testData[:, 3]).T
        S =  np.tanh(X * self.w1) 
        S = np.hstack(([[1]]*len(S),S))
        YPredict = np.tanh(S* self.w2)
#        print YPredict
        return 1.0/recordNum * sum(np.square(Y - YPredict))

def main():
   trainData = np.loadtxt('hw4_nnet_train.dat')
   testData = np.loadtxt('hw4_nnet_test.dat')
   M = 3
   r = 0.1
   T = 50000
   for eta in (0.001,0.01,0.1,1,10): 
       for i in range(0,10):
           neuralNet = NeuralNet((2,M,1), eta, r, T)
           neuralNet.train(trainData)
           print eta,neuralNet.test(testData)[0,0]

if __name__=='__main__':
    main()
