import cvxpy as cp
import numpy as np
import math
def K(x1,x2):
    return (1 + np.dot(x1,x2))**2
def main():
    x = [[1,0],[0,1],[0,-1],[-1,0],[0,2],[0,-2],[-2,0]]
    y = [-1, -1, -1, 1, 1, 1, 1]
    Q = np.empty((7,7))
    for i in range(0,7):
        for j in range(0,7):
            Q[i,j] = y[i]*y[j]*K(x[i],x[j])

    p = np.array([-1] * 7)
    alpha = cp.Variable(7)
    objective = cp.Minimize(0.5 * cp.quad_form(alpha, Q) + cp.sum_entries(cp.mul_elemwise(p, alpha)))
    constraints = [cp.sum_entries(cp.mul_elemwise(y,alpha)) == 0]
    for i in range(0,7):
        constraints.append(alpha[i]>=0)
    prob = cp.Problem(objective, constraints)
    prob.solve()
    z = [[1,math.sqrt(2)*x1, math.sqrt(2)*x2, x1 ** 2, x2 ** 2] for (x1,x2) in x]
    w = [0] * 5
    for i in range(0,7):
        w += np.dot(float(alpha.value[i]) * y[i], z[i])
    print "w=",sum(w)
    #choose any support vector (z,y) to calculate the b
    print "b=",y[1] - np.dot(w, z[1])
    print "status:", prob.status
    print "optimal value", prob.value
    print alpha.value
    print sum(alpha.value)

if __name__ == "__main__":
    main()

    
