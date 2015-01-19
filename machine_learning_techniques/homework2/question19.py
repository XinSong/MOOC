import cvxpy as cp
import numpy as np
import pandas as pd
import math

def K(x1,x2,gamma):
    return math.exp(- gamma * np.dot(x1 - x2, x1 - x2))

def evaluate(x_train, beta, b, gamma, x_test, y_test):
    correct = 0.0
    error = 0.0
    for i in range(0, len(x_test)):
        pred = 0
        for j in range(0, len(x_train)):
            pred += beta[j] * K(x_test[i],x_train[j], gamma)
        if pred >= 0 and y_test[i] == 1 or pred < 0 and y_test[i] == -1:
            #print "correct", pred, y_test[i]
            correct += 1
        else:
            #print "error", pred, y_test[i]
            error += 1
    return error/(error + correct)

def main():
    train = pd.read_table('train.dat', header=None, sep=' ')
    x_train = np.array(train[range(0,10)])
    y_train = np.array(train[[10]])
    test = pd.read_table('test.dat', header=None, sep=' ')
    x_test = np.array(test[range(0,10)])
    y_test = np.array(test[[10]])
    Q = np.empty((400,400))

    for gamma in (32, 2, 0.125):
        Q = np.empty((400,400))
        for i in range(0,400):
            for j in range(0,400):
                Q[i,j] = K(x_train[i], x_train[j], gamma)

        for C in (0.001, 1, 1000):
            beta = np.dot(np.linalg.inv(C * np.eye(400) + Q), np.array(y_train))
            pred = 0
            for j in range(0, len(x_train)):
                pred += beta[j] * K(x_train[1],x_train[j], gamma)
            b = y_train[1] - pred
            evaluation = evaluate(x_train, beta, b, gamma, x_train, y_train)
            test_evaluation = evaluate(x_train, beta, b, gamma, x_test, y_test)
            print "Gamma=",gamma, ", lambda=", C, ", b=",b,", evaluation=",evaluation, test_evaluation
                        
if __name__ == "__main__":
    main()

