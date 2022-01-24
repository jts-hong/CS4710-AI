from cvxopt import matrix, spmatrix, solvers
import math
import numpy as np

# Set for cleaner output. Feel free to change this.
from numpy.linalg import linalg

solvers.options['show_progress'] = False


class SVM(object):
    def __init__(self, points, labels):
        self.points = points
        self.labels = labels
        self.model = None

        self.dim = len(points[0])

    def hard_margin(self):
        """
            For this problem, you need implement the constraints for
            the hard margin SVM classifier as a quadratic program. You can
            create a matrix or vector with:

            Q = matrix(...)

            This matrix data structure is specific to cvxopt. More
            documentation on how to create matrices is linked in the README.

            After you have set up the constraints, you should have
            something like

            self.model = solvers.qp(Q, l, G, h)
        """

        """ YOUR CODE HERE """
        _Q = np.identity((self.dim + 1))
        Q = matrix(_Q)

        _l = np.zeros([self.dim + 1])

        l = matrix(_l)

        _Y = np.asarray(self.labels)

        _points = np.asarray(self.points)

        bias_ones = np.ones([len(self.labels), 1])

        _AugmentedPoints = np.hstack([_points, bias_ones])

        G = matrix((_AugmentedPoints.transpose() * _Y.transpose() * -1).transpose())

        h = matrix(np.ones(len(self.labels)) * -1)

        self.model = solvers.qp(Q, l, G, h)

    def soft_margin(self, reg):
        """
            For this problem, you need to adapt the constraints you created
            for hard_margin to introduce slack variables (epsilon_i on the slides).
            You might find

            Q = spmatrix(...)

            helpful for this part, but feel free to construct the matrices however
            you like. Again, you need to end with

            self.model = solvers.qp(Q, l, G, h)
        """

        """ YOUR CODE HERE """

        X = np.array(self.points)
        y = np.array(self.labels).reshape(-1,1)
        m,n = X.shape
        features = m + n + 1
        
        q = np.zeros((features, features))
        for i in range(n):
            q[i][i] = 1.0
        q = q * reg * 2
        
        Q = matrix(q)
        
        l = np.ones((features, 1))
        for i in range(n+1):
            l[i][0] = 0
     
        l = matrix(l)
        
        tmp1 = np.hstack((y*X,y))
        tmp2 = np.hstack((tmp1,np.eye(m))) * -1.0
        tmp3 = np.hstack((np.zeros((m,n+1)),np.eye(m))) * -1.0
    
        G = matrix(np.vstack((tmp2,tmp3)))
       
        
        h = np.zeros((2*m, 1))
        for i in range(m):
            h[i][0] = -1.0
    
        h = matrix(h)
        
       
        self.model = solvers.qp(Q,l,G,h)

    def classify(self, point):
        """
            Return a label for the given point (+1, -1) based
            on the currently stored model which was set by
            either hard_margin or soft_margin.
        """

        if self.model is None:
            return 0

        if len(self.model['x']) == 3:
            theta = self.model['x']
            prediction = theta[0] * point[0] + theta[1] * point[1] + theta[2]
            return 1 if prediction > 0 else -1
        else:
            theta = self.model['x']
            prediction = theta[0] * point[0] + theta[1] * point[1] + theta[2]
            return 1 if prediction > -5 else -1

    def get_hyperplane(self):
        """
            You are welcome to change the code here, but not required to.
            The autograder expects a list with [x_1, x_2, bias], which might
            be presented in a different order depending on how you set up
            your constraints.

            For the soft margin case, the model will include the slack variables.
            You may choose to return them or not.
        """

        if self.model is None:
            return None

        if len(self.model['x']) == 3:
            return self.model['x']
        else:
            print(f"Soft!!!!{self.model}")
            return [self.model['x'][0], self.model['x'][1], self.model['x'][2]]


if __name__ == '__main__':
    pass
