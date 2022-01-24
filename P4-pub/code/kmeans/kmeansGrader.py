# Setup
import copy
import sys
import io
import os
import math
import numpy as np
from kmeans import KMeansClassifier


class Grader:
    def __init__(self, path=os.getcwd(), gs_flag=0):
        self._save_stdout = sys.stdout
        sys.stdout = io.BytesIO()
        sys.stdout = self._save_stdout

        self._score = 0.0
        self._score_max = 6.0
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

        points = np.load('easy.npy')
        centers = [[1., 1.], [8., 1.], [1., 8.]]
        kmeans = KMeansClassifier(3, centers, points)
        kmeans.assign_clusters()

        print('Testing assign_clusters...')

        correct_points = [5, 9, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        cluster_0 = [tuple(item) for item in kmeans.clusters[0]]
        correct = sum([tuple(points[i]) in cluster_0 for i in correct_points])

        if correct == len(correct_points):
            print('PASSED')
            self._score += 1.0
        else:
            print('FAILED: {}/{} points are in the wrong cluster'.format(len(correct_points) - correct, len(correct_points)))

        print('Testing update_centers...')

        correct_centers_floored = [(0., 1.), (7., 1.), (2., 7.)]
        kmeans.update_centers()
        centers = [(math.floor(center[0]), math.floor(center[1])) for center in kmeans.centers]
        correct = (correct_centers_floored == centers)

        if correct:
            print('PASSED')
            self._score += 1.0
        else:
            print('FAILED: Correct centers (rounded down):')
            print(correct_centers_floored)
            print('Your centers are:')
            print(centers)

        print('Testing easy.npy...')

        correct = True

        points = np.load('easy.npy')
        centers = [[1., 1.], [8., 1.], [1., 8.]]
        kmeans = KMeansClassifier(3, centers, points)
        kmeans.fit()
        error = kmeans.error()
        if abs(error - 215.328812189) > 1.0:
            correct = False
            print('FAILED: Required error of {} +/- 1.0 for centers:'.format(215.328812189))
            print(centers)
            print('Your error: {}'.format(error))

        centers = [[1., 1.], [8., 1.], [1., 8.], [8., 8.]]
        kmeans = KMeansClassifier(4, centers, points)
        kmeans.fit()
        error = kmeans.error()
        if abs(error - 80.3323760685) > 1.0:
            correct = False
            print('FAILED: Required error of {} +/- 1.0 for centers:'.format(80.3323760685))
            print(centers)
            print('Your error: {}'.format(error))

        if correct:
            print('PASSED')
            self._score += 2.0
        else:
            print('FAILED')

        print('Testing hard.npy...')

        correct = True

        points = np.load('hard.npy')
        centers = [[1., 1.], [8., 1.], [1., 8.]]
        kmeans = KMeansClassifier(3, centers, points)
        kmeans.fit()
        error = kmeans.error()
        if abs(error - 213.551360628) > 1.0:
            correct = False
            print('FAILED: Required error of {} +/- 1.0 for centers:'.format(213.551360628))
            print(centers)
            print('Your error: {}'.format(error))

        centers = [[1., 1.], [8., 1.], [1., 8.], [8., 8.]]
        kmeans = KMeansClassifier(4, centers, points)
        kmeans.fit()
        error = kmeans.error()
        if abs(error - 142.474546813) > 1.0:
            correct = False
            print('FAILED: Required error of {} +/- 2.0 for centers:'.format(142.474546813))
            print(centers)
            print('Your error: {}'.format(error))

        if correct:
            print('PASSED')
            self._score += 2.0

        print('SCORE: {}/{}'.format(self._score, self._score_max))
        self.gsOutput()
