import cvxpy as cp
import numpy as np
import math
def K(x1,x2):
    return (1 + np.dot(x1,x2))**2
def main():
    TARGET = 0
    y = []
    x = []
    for line in open("features.train"):
        vec = line.strip().split()
        x.append([float(vec[1]),float(vec[2])])
        if int(float(vec[0])) == TARGET:
            y.append(1)
        else:
            y.append(-1)
    Q = np.empty((len(x),len(x)))
    p = [-1] * len(x)
    for i in range(0,len(x)):
        for j in range(0,len(x)):
            Q[i,j] = y[i]*y[j] * K(x[i],x[j])

    alpha = cp.Variable(len(x))
    C = 0.01
    objective = cp.Minimize(0.5 * cp.quad_form(alpha,Q) + cp.sum_entries(cp.mul_elemwise(p,alpha)))
    constraints = [cp.sum_entries(cp.mul_elemwise(y,alpha)) == 0]
    for i in range(0,len(x)):
        constraints.append(alpha[i]>=0)
    
    prob = cp.Problem(objective, constraints)
    prob.solve()
    print "sum(alpha)=",sum(alpha.value)
    #choose any support vector (z,y) to calculate the b
    print "status:", prob.status
    print "optimal value", prob.value

if __name__ == "__main__":
    main()

    
