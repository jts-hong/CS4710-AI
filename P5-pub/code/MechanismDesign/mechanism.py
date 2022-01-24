# coding=utf-8 
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import sys
import numpy as np
from cvxopt.modeling import *
from cvxopt import matrix, spmatrix, solvers


class PostedPrice:
    def __init__(self, values, dist):
        # Values = [values_0, ..., values_9] where value_i is buyer of type i's valuation for the item
        self.values = values
        # dist = [dist_0, ..., dist_9] is the distribution probability of buyer's different types
        self.dist = dist
    
    def setObjectiveOptimizeRevenue(self):
        """
        TODO
        The buyer‘s valuation of the item is assumed to be a random number which is drawn from [0.0, ..., 0.9]
        Compute the mechanism's optimal price which can maximize the ecpected revenue (i.e. the payment by the buyer) 
        through searching over the whole possible pricing space [0.0, ..., 0.9]
        
        Returns the optimal expected revenue and the corresponding reserved price

        Hint: 
        For a specific price p, the expected revenue = p * Pr(value > p) where Pr(values > p) is the probability for buyer's
        valuation to be greater than p, and you can calculate this through exhaustive search over buyer's value distribution
        """
        price_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        revenues = []
        for i in range(9):
            cP = price_list[i]
            prob=0
            for j in range(len(self.values)):
                if cP<= self.values[j]:
                    prob+=self.dist[j]
            revenues.append((cP*prob,cP))
        maxValue = max(revenues)
        
        return maxValue


class Mechanism:
    def __init__(self, values, dist):
        # Values = [values_0, ..., values_9] where value_i is buyer of type i's valuation for the item
        self.values = values
        # dist = [dist_0, ..., dist_9] is the distribution probability of buyer's different types
        self.dist = dist
        self.getInitProblem()
    
    def getInitProblem(self):

        """
        Payment decision variables: X = [x_0, ...., x_9]
        x_i represents the payment required by the mechanism for the buyer type i
        """
        self.x = {(i): variable(name = 'x_{0}'.format(i)) for i in range(10)}
        
        """
        Allocation probability decision variables: P = [p_0, ...., p_9]
        x_i represents the mechanism's probability of allocating the item to buyer type i
        """
        self.p = {(i): variable(name = 'p_{0}'.format(i)) for i in range(10)}

        """
        The sequence of Individual Rationality constraints C_IR = [c1, ..., c_m]
        which requre that all the types of buyer's utility should be greater than or equal to 0
        """
        self.C_IR = []

        """
        The sequence of Incentive Compatible constraints C_IC = [c1, ..., c_n]
        The constraints requre that all the types of buyer's utility of behaving truthfully
        should be greater than or equal to the utility of behaving untruthfully
        """
        self.C_IC = []

        # Individual rationality constraints for the mechanism
        self.addIRConstraint()
        
        # Incentive compatible constraints for the mechanism
        self.addICConstraint()

        # Set the objective of the mechanism: maximizing the expected revenue of the mechanism
        self.setObjective()
    
    def addIRConstraint(self):
        """
        TODO
        Compute the sequence of constraints C_IR = [c1, ..., c_m]
        The constraints requre that all the types of buyer's utility should be greater than or equal to 0

        Hint:
        Buyer type i's utility = value[i] * p[i] - x[i]
        where p[i] is the probability for buyer type i to get the item
        x[i] is the buyer type i's payment
        """
        for i in range(len(self.x)):
            self.C_IR.append((self.values[i]*self.p[i]-self.x[i] >= 0))
        return self.C_IR
        pass

    def addICConstraint(self):
        """
        TODO
        Compute the sequence of constraints C_IC = [c1, ..., c_n]
        The constraints requre that all the types of buyer's utility of behaving truthfully
        should be greater than or equal to the utility of behaving untruthfully

        Hint:
        Buyer type i's truthful utility  = value[i] * p[i] - x[i] 
        Buyer type i's untruthful utility = value[i] * p[j] - x[j]
        where p[i] is the probability for buyer type i to get the item
        x[i] is the buyer type i's payment
        p[j] is the probability for buyer type j to get the item
        x[j] is the buyer type j's payment
        """
        for i in range(len(self.x)):
            for j in range(len(self.x)):
                if (i!=j):
                    self.C_IC.append((self.values[i]*self.p[i]-self.x[i] >= self.values[i]*self.p[j]-self.x[j]))
        pass
    
    def setObjective(self):
        """
        TODO
        The objective is to maximize the expected revenue from the buyer 
        while satisfying the IC constraints (C_IC) and IR(C_IR) constraint:
        
        Returns (1) the optimal revenue, 
        (2) a list of payment decision variables' values
        (3) a list of allocation probability variables' values

        Hint:
        The expected revenue from the buyer shoule be the weighted sum of payments,
        and the weight of each payment from a specific type is the distribution probability of the corresponding type
        revenue = sum(payment[i] * dist[i] for i in range(10))
        """
        revenue = sum(self.x[i] * self.dist[i] for i in range(10))
        prob_constraint = []
        for i in range(len(self.values)):
            prob_constraint.append((self.p[i]>=0))
            prob_constraint.append((self.p[i]<=1))
        
        problem = op(-revenue, self.C_IC+self.C_IR+prob_constraint)
        problem.solve()
        payment = [[0] for i in range(10)]
        allocation = [[0] for i in range(10)]

        for i in range(10):
            payment[i] = self.x[i].value
            allocation[i] = self.p[i].value
        
        return -problem.objective.value()[0], payment, allocation

        

if __name__ == '__main__':

    values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    dist = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    print('Q1: Reserved Price')
    pp = PostedPrice(values, dist)
    r, p = pp.setObjectiveOptimizeRevenue()
    print('The value types of the buyer are {} and the distribution probability of those value types is {}'.format(values, dist))
    print('The optimal revenue and its corresponsing reserved price are {} and {}\n'.format(r, p))
    
    print('Q2: Mechanism Design')
    m = Mechanism(values, dist)
    revenue, payment, alloc_prob = m.setObjective()
    print('The optimal revenue of the mechanism is {} when the value types of the buyer are {} and the distribution probability of those value types is {}'.format(revenue, values, dist))
    print('The payment rule is {} for the above buyer type distribution'.format(payment))
    print('The probability of the buyer to get the item is {}'.format(alloc_prob))