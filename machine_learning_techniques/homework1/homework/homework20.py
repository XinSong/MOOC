from svmutil import *
import random
import sys
def main(train_file):
    (y,x) = svm_read_problem(train_file)
    count = {1:0,10:0,100:0,1000:0,10000:0}
    for iter in range(0,100):
        max_acc = 0
        max_gamma = -1 
        train_set = set(random.sample(range(0,len(x)),1000))
        x_train = [x[i] for i in train_set]
        y_train = [ y[i] for i in train_set ]
        y_train = [ 1 if int(_y)==0 else -1 for _y in y_train ]
        x_test = [x[i] for i in range(0,len(x)) if i not in train_set ]
        y_test = [y[i] for i in range(0,len(x)) if i not in train_set ]
        y_test = [ 1 if int(_y) == 0 else -1 for _y in y_test ]
        for gamma in (1,10,100,1000,10000):
            m = svm_train(y_train, x_train,"-s 0 -t 2 -c 0.1 -g " + str(gamma))
            (y_pred, p_acc, p_val) = svm_predict(y_test,x_test,m)
            if p_acc[0] > max_acc:
                max_acc = p_acc[0]
                max_gamma = gamma
        count[max_gamma] += 1
    for i in count:
        print i,count[i]

if __name__ == '__main__':
    main(sys.argv[1])
