# Setup
import copy
import sys
import io
import os
import math
import numpy as np
from svm import SVM

def hyperplane_str(sol):
    y = sol[1]
    if y == 0.0:
        if x == 0.0:
            return "x = {:.3f}".format(sol[2]/sol[0])
        else:
            return "x = {:.3f}".format(sol[2])
    else:
        x = -1*sol[0]/y
        b = -1*sol[2]/y
        return "y = {:.3f}x + {:.3f}".format(x, b)

def min_margin(plane, points):
    theta = math.sqrt(plane[0]**2 + plane[1]**2)
    return min([abs((plane[0]*p[0]+plane[1]*p[1]+plane[2])/theta) for p in points])

def hard_debug_info(plane, sol_plane, points, labels):
    print("Points and labels: ")
    print(points)
    print(labels)
    print("\tYour solution: " + hyperplane_str(plane))
    print("\tYour Margin: {:.5f}".format(min_margin(plane, points)))
    print("\tReference solution: " + hyperplane_str(sol_plane))
    print("\tReference Margin: {:.5f}".format(min_margin(sol_plane, points)))

def soft_debug_info(plane, sol_plane, points, labels):
    print("Points and labels: ")
    print(points)
    print(labels)
    print("\tYour solution: " + hyperplane_str(plane))
    print("\tReference solution: " + hyperplane_str(sol_plane))

class Grader:
    def __init__(self, path=os.getcwd(), gs_flag=0):
        self._save_stdout = sys.stdout
        sys.stdout = io.BytesIO()
        sys.stdout = self._save_stdout

        self._score = 0.0
        self._score_max = 10.0
        self.gs = gs_flag

    # output prining code
    def gsOutput(self):
        totalScore = self._score
        maxScore = self._score_max
        json = '{"output": "Total score (' + str(totalScore) + ' / ' + str(maxScore) + ')"," tests": []'
        json += ', "score": ' + str(totalScore) + ', "max_score": ' + str(maxScore) + '}'
        f = open('grade.json', 'w')
        f.write(json)

    def grade(self):
        easy_points = [[1.0,0.0],[0.0,0.0],[0.0,1.0],[1.0,1.0]]
        easy_labels = [1.0,-1.0,1.0,1.0]
        easy_hard_sol = [1.0,1.0,-0.5]

        hard_points = [[-1.0,1.0],[1.0,0.0],[0.0,2.0],[2.0,2.0],[6.0,4.0],
                       [3.0,5.0],[4.0,4.0],[4.0,5.0],[5.0,6.0],[6.0,5.0]]
        hard_labels = [1.0,1.0,1.0,1.0,1.0,-1.0,-1.0,-1.0,-1.0,-1.0]
        hard_hard_sol = [-0.33333,1.0,-2.33333]
        hard_soft_sol = [0.5,1.0,-4.347]

        nonsep_points = [[0.0,0.0],[0.0,1.0],[1.0,0.0],[3.0,2.0],
                         [3.0,1.0],[2.0,2.0],[1.0,3.0]]
        nonsep_labels = [1.0,1.0,1.0,1.0,-1.0,-1.0,-1.0]
        nonsep_soft_sol = [1.0,1.0,-2.5]

        easy = SVM(easy_points, easy_labels)
        hard = SVM(hard_points, hard_labels)
        nonsep = SVM(nonsep_points, nonsep_labels)
        
        correct = True

        print("Testing the hard margin classifier...")
        easy.hard_margin()
        plane = easy.get_hyperplane()
        if(plane is None):
            print("NOT IMPLEMENTED: hard_margin (-2)")
        elif(abs(min_margin(plane, easy_points) - min_margin(easy_hard_sol, easy_points)) > 0.001):
            print("FAILED: easy points (-2)")
            hard_debug_info(plane, easy_hard_sol, easy_points, easy_labels)
        else:
            self._score += 2.0

        hard.hard_margin()
        plane = hard.get_hyperplane()
        if(plane is None):
            print("NOT IMPLEMENTED: hard_margin (-2)")
        elif(abs(min_margin(plane, hard_points) - min_margin(hard_hard_sol, hard_points)) > 0.001):
            print("FAILED: hard points (-2)")
            hard_debug_info(plane, hard_hard_sol, hard_points, hard_labels)
        else:
            self._score += 2.0

        print("Testing the soft margin classifier...")
        nonsep.soft_margin(1.0)
        plane = nonsep.get_hyperplane()
        if(plane is None):
            print("NOT IMPLEMENTED: soft_margin (-2)")
        else:
            x = plane[0]/plane[1]
            b = plane[2]/plane[1]
            if(abs(x-nonsep_soft_sol[0])+abs(b-nonsep_soft_sol[2]) > 0.001):
                print("FAILED: non-separable points with reg = 1.0 (-2)")
                soft_debug_info(plane, nonsep_soft_sol, nonsep_points, nonsep_labels)
            else:
                self._score += 2.0

        hard.soft_margin(10.0)
        plane = hard.get_hyperplane()
        if(plane is None):
            print("NOT IMPLEMENTED: soft_margin (-2)")
        else:
            x = plane[0]/plane[1]
            b = plane[2]/plane[1]
            if(abs(x-hard_soft_sol[0])+abs(b-hard_soft_sol[2]) > 0.001):
                print("FAILED: hard points with reg = 1.0 (-2)")
                soft_debug_info(plane, hard_soft_sol, hard_points, hard_labels)
            else:
                self._score += 2.0

        print("Testing classify...")
        l1 = hard.classify([0.0,0.0])
        l2 = hard.classify([7.4,4.0])
        l3 = hard.classify([0.0,3.0])
        if(l1 == 1.0 and  l2 == -1.0 and l3 == 1.0):
            self._score += 1.0
        else:
            print("FAILED: soft margin classify (-1)")
            print("[0, 0] (+1) classified as {}".format(l1))
            print("[7, 4] (-1) classified as {}".format(l2))
            print("[0, 3] (+1) classified as {}".format(l3))

        hard.hard_margin()
        l1 = hard.classify([0.0,0.0])
        l2 = hard.classify([7.4,4.0])
        l3 = hard.classify([0.0,3.0])
        if(l1 == 1.0 and l2 == 1.0 and l3 == -1.0):
            self._score += 1.0
        else:
            print("FAILED: hard margin classify (-1)")
            print("[0, 0] (+1) classified as {}".format(l1))
            print("[7, 4] (+1) classified as {}".format(l2))
            print("[0, 3] (-1) classified as {}".format(l3))

        print('SCORE: {}/{}'.format(self._score, self._score_max))
        self.gsOutput()

