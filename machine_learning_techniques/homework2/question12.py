#coding=utf-8

import pandas as pd
import math

def performance(x_threshold, test, sign = 1):
    correct = 0.0
    error = 0.0
    new_weight = []
    for (idx, row) in test.iterrows():
        x, y, weight = row
        if x >= x_threshold and y == sign:
            correct += weight
        elif x < x_threshold and y == -1 * sign:
            correct += weight
        else:
            error += weight
    return error/(correct+error)

def decision_stump(train):
    best_performance = float("inf")
    best_threshold = 0
    best_sign = 1
    best_column =""
    for i in range(1, 3):
        column = "x" + str(i)
        train.sort(column, inplace=True)
        train_data = train[[column, "y", "weight"]]
        x = train_data[column]
        low = float("-inf")
        for x_item in x:
            threshold = 0.5 * (low + x_item)
            positive_stump = performance(threshold, train_data, 1) 
            if positive_stump < best_performance:
                best_performance = positive_stump
                best_threshold = threshold
                best_sign = 1
                best_column = column
            
            negative_stump = performance(threshold, train_data, -1) 
            if negative_stump < best_performance:
                best_performance = negative_stump
                best_threshold = threshold
                best_sign = -1
                best_column = column
            low = x_item
    
    return (best_column, best_threshold, best_sign, best_performance)

def adjust_weight(train, model, t):
    (column, threshold, sign) = model
    new_weight = [] 
    test = train[[column, "y", "weight"]]
    for (idx, row) in test.iterrows():
        x, y, weight = row
        if x >= threshold and y == sign:
            new_weight.append(weight/t)
        elif x < threshold and y == -1 * sign:
            new_weight.append(weight/t)
        else:
            new_weight.append(weight * t)
    train["weight"] = new_weight
    return train

def predict(test, boosting_model):
    x1, x2 = test
    sum = 0
    for model in boosting_model:
        column, threshold, sign, alpha = model
        if column == "x1":
            if x1 >= threshold:
                sum += sign * alpha
            else:
                sum += -1 * sign * alpha
        if column == "x2":
            if x2 >= threshold:
                sum +=  sign * alpha
            else:
                sum += -1 * sign * alpha
    if sum >= 0:
        return 1
    else:
        return -1
        
def performance_G(test, boosting_model):
    correct = 0.0
    error = 0.0
    for (idx, row) in test.iterrows():
        x1, x2, y = row
        pred = predict((x1,x2), boosting_model)
        if y == pred:
            correct += 1
        else:
            error += 1
    return error/(error + correct)

def main():
    train = pd.read_table("hw2_adaboost_train.dat",names=["x1","x2","y"],sep=" ")
    train["weight"] = [0.01] * 100
    boosting_model = []
    for i in range(0,1):
        (best_column, best_threshold, best_sign, best_performance) = decision_stump(train)        
        print i, best_performance
        t = math.sqrt((1-best_performance)/best_performance)
        alpha = math.log(t)
        train = adjust_weight(train,(best_column, best_threshold, best_sign), t)
        if i==1 or i==299:
            print i,sum(train['weight'])
        
        boosting_model.append((best_column, best_threshold, best_sign, alpha))
    train = train[["x1","x2","y"]]
    test = pd.read_table("hw2_adaboost_test.dat",names=["x1","x2","y"],sep=" ")
    print performance_G(train, boosting_model)
    print performance_G(test, boosting_model)

if __name__=='__main__':
    main()

