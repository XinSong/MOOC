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

    w = cp.Variable(2)
    b = cp.Variable()
    Q = np.identity(2)
    xi = cp.Variable(len(x))
    C = 0.01
    objective = cp.Minimize(0.5 * cp.quad_form(w,Q) + C * cp.sum_entries(xi))
    constraints = []
    for i in range(0,len(x)):
        constraints.append(y[i]*(cp.conv(x[i],w) + b) >= 1 - xi[i])
        constraints.append(xi[i]>=0)
    
    prob = cp.Problem(objective, constraints)
    prob.solve()
    print "w=",sum([ item**2 for item in w.value])
    #choose any support vector (z,y) to calculate the b
    print "b=",y[1] - np.dot(w.value, x[1])
    print "status:", prob.status
    print "optimal value", prob.value

if __name__ == "__main__":
    main()

    
