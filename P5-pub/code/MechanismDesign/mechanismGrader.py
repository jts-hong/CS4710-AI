# Setup
import copy
import sys
import io
import os
import numpy as np
import mechanism
import copy


class Grader:
    def __init__(self, path=os.getcwd(), gs_flag=0):
        self._save_stdout = sys.stdout
        sys.stdout = io.BytesIO()
        sys.stdout = self._save_stdout

        self._score = 0.0
        self._score_max = 10.0
        self._values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        self._dist = [[1.0/len(self._values)] * len(self._values)]
        self._scores = [0.25, 0.20, 0.16, 0.12, 0.12, 0.12, 0.3, 0.36, 0.42, 0.48, 0.5, 0.18, 0.13, 0.33, 0.42, 0.16, 0.165, 0.39, 0.54, 0.25]
        self.gs = gs_flag

    # output prining code
    def gsOutput(self):
        totalScore = self._score
        maxScore = self._score_max
        json = '{"output": "Total score (' + str(totalScore) + ' / ' + str(maxScore) + ')"," tests": []'
        json += ', "score": ' + str(totalScore) + ', "max_score": ' + str(maxScore) + '}'
        f = open('grade.json', 'w')
        f.write(json.encode('UTF-8'))

    def gen(self):
        temp = copy.deepcopy(self._dist[0])
        for trial in range(5):
            temp2 = copy.deepcopy(temp)
            temp2[trial] += 0.1
            temp2[10 -1 - trial] -= 0.1
            self._dist.append(temp2)
            temp = temp2
        for trial in range(5):
            new_temp = self._dist[trial+1][::-1]
            self._dist.append(new_temp)
        temp = copy.deepcopy(self._dist[0])
        for trial in [0, 2]:
            temp2 = copy.deepcopy(temp)
            temp2[trial] += 0.15
            temp2[10 - 1 - trial] -= 0.1
            temp2[10 - 2 - trial] -= 0.05
            self._dist.append(temp2)
            temp = temp2
        for trial in [11, 12]:
            new_temp = self._dist[trial][::-1]
            self._dist.append(new_temp)
        temp = copy.deepcopy(self._dist[0])
        for trial in [0, 3]:
            temp2 = copy.deepcopy(temp)
            temp2[trial] += 0.25
            temp2[10 - 1 - trial] -= 0.1
            temp2[10 - 2 - trial] -= 0.05
            temp2[10 - 3 - trial] -= 0.05
            self._dist.append(temp2)
            temp = temp2
        for trial in [15, 16]:
            new_temp = self._dist[trial][::-1]
            self._dist.append(new_temp)
        temp = copy.deepcopy(self._dist[0])
        self._dist.append(temp)

    def grade(self):
        self.gen()
        print('Grading Q1: Reserved Price')
        count = 0.0
        for trial in range(len(self._dist)):
            print('Test case {}'.format(trial+1))
            test_distribution = self._dist[trial]
            pp = mechanism.PostedPrice(self._values, test_distribution)
            test_rev, _ = pp.setObjectiveOptimizeRevenue()
            if abs(test_rev - self._scores[trial]) <= 0.00001:
                count += 1.0
                print('Passed!')
            else:
                print('Failed with the following testing case - valuation types: {}, distributions: {}'.format(self._values, test_distribution))
        if count / len(self._dist) >= 0.6: self._score += 4.0
        print('Your score for Q1 is {}\n'.format(self._score))
        print('===================================================================================\n')
        count = 0.0
        print('Grading Q2: Mechanism Design')
        for trial in range(len(self._dist)):
            print('Test case {}'.format(trial+1))
            test_distribution = self._dist[trial]
            m = mechanism.Mechanism(self._values, test_distribution)
            test_rev, _, _ = m.setObjective()
            if abs(test_rev - self._scores[trial]) <= 0.00001:
                count += 1.0
                print('Passed!')
            else:
                print('Failed with the following testing case - valuation types: {}, distributions: {}'.format(self._values, test_distribution))
        if count / len(self._dist) >= 0.6: self._score += 6.0
        print('TOTAL SCORE: {}/{}'.format(self._score, self._score_max))
        