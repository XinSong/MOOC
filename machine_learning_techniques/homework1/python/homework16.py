from svmutil import *
import random
import sys
def main(train_file):
    (y,x) = svm_read_problem(train_file)
    m = svm_train(y, x,"-s 0 -t 1 -d 2 -c 0.01")
    (y_pred, p_acc, p_val) = svm_predict(y,x,m)
    print p_acc

if __name__ == '__main__':
    main(sys.argv[1])
