# Setup
import copy
import sys
import io
import os
import multiprocessing
import time
import sudoku as sudoku

# some helper boards to work with
boardDone = [[7,6,9,3,4,2,1,5,8],
             [3,5,4,7,8,1,6,9,2],
             [1,8,2,6,9,5,4,7,3],
             [5,9,3,1,7,8,2,6,4],
             [4,1,7,2,6,3,5,8,9],
             [6,2,8,9,5,4,3,1,7],
             [8,3,5,4,1,9,7,2,6],
             [2,7,1,8,3,6,9,4,5],
             [9,4,6,5,2,7,8,3,1]]
boardM00 =  [[0,6,9,3,4,2,1,5,8],
             [3,5,4,7,8,1,6,9,2],
             [1,8,2,6,9,5,4,7,3],
             [5,9,3,1,7,8,2,6,4],
             [4,1,7,2,6,3,5,8,9],
             [6,2,8,9,5,4,3,1,7],
             [8,3,5,4,1,9,7,2,6],
             [2,7,1,8,3,6,9,4,5],
             [9,4,6,5,2,7,8,3,1]]
boardM00c = [[0,6,6,3,4,2,1,5,8],
             [3,5,4,7,8,1,6,9,2],
             [1,8,2,6,9,5,4,7,3],
             [5,9,3,1,7,8,2,6,4],
             [4,1,7,2,6,3,5,8,9],
             [6,2,8,9,5,4,3,1,7],
             [8,3,5,4,1,9,7,2,6],
             [2,7,1,8,3,6,9,4,5],
             [9,4,6,5,2,7,8,3,1]]
boardM36 =  [[7,6,9,3,4,2,1,5,8],
             [3,5,4,7,8,1,6,9,2],
             [1,8,2,6,9,5,4,7,3],
             [5,9,3,1,7,8,0,6,4],
             [4,1,7,2,6,3,5,8,9],
             [6,2,8,9,5,4,3,1,7],
             [8,3,5,4,1,9,7,2,6],
             [2,7,1,8,3,6,9,4,5],
             [9,4,6,5,2,7,8,3,1]]
boardM36D =  [[7,6,9,3,4,2,1,5,8],
             [3,5,4,7,8,1,6,9,2],
             [1,8,2,6,9,5,4,7,3],
             [5,9,3,1,7,8,2,6,4],
             [4,1,7,2,6,3,5,8,9],
             [6,2,8,9,5,4,3,1,7],
             [8,3,5,4,1,9,7,2,6],
             [2,7,1,8,3,6,9,4,5],
             [9,4,6,5,2,7,8,3,1]]
boardM36P = [[7,6,9,3,4,2,1,5,8],
             [3,5,4,7,8,1,0,9,2],
             [1,8,2,6,9,5,4,7,3],
             [5,9,3,1,7,8,0,0,4],
             [4,1,7,2,0,3,0,0,9],
             [6,2,8,9,5,4,3,1,7],
             [8,3,0,4,1,9,7,2,6],
             [2,0,1,8,3,6,9,4,5],
             [9,4,6,5,2,7,8,3,1]]
boardM36Pc =[[7,6,9,3,4,2,1,5,8],
             [3,5,4,7,8,1,0,9,2],
             [1,8,2,6,9,5,4,7,3],
             [5,9,3,1,7,8,0,0,4],
             [4,1,7,2,0,3,0,0,4],
             [6,2,8,9,5,4,4,4,4],
             [8,3,0,4,1,9,7,2,6],
             [2,0,1,8,3,6,9,4,5],
             [9,4,6,5,2,7,8,3,1]]
boardHard = [[0,0,0,0,0,8,9,0,2],
             [6,0,4,3,0,0,0,0,0],
             [0,0,0,5,9,0,0,0,0],
             [0,0,5,7,0,3,0,0,9],
             [7,0,0,0,4,0,0,0,0],
             [0,0,9,0,0,0,3,0,5],
             [0,8,0,0,0,4,0,0,0],
             [0,4,1,0,0,0,0,3,0],
             [2,0,0,1,5,0,0,0,0]]
boardEasy =  [[0,2,0,1,7,8,0,3,0],
              [0,4,0,3,0,2,0,9,0],
              [1,0,0,0,0,0,0,0,6],
              [0,0,8,6,0,3,5,0,0],
              [3,0,0,0,0,0,0,0,4],
              [0,0,6,7,0,9,2,0,0],
              [9,0,0,0,0,0,0,0,2],
              [0,8,0,9,0,1,0,6,0],
              [0,1,0,4,3,6,0,5,0]]
boardImpossible = [[0,2,0,1,7,8,0,3,0],
                   [0,4,0,3,0,2,0,9,0],
                   [1,0,0,0,0,0,0,0,6],
                   [0,0,8,6,0,3,5,0,0],
                   [3,0,0,0,0,0,0,0,4],
                   [0,0,6,7,0,9,2,0,0],
                   [9,3,5,0,0,0,0,0,2],
                   [0,8,4,9,0,1,0,6,0],
                   [2,1,7,4,3,6,8,5,9]]


class Grader:
    def __init__(self, path=os.getcwd(), gs_flag = 0):
        self._save_stdout = sys.stdout
        sys.stdout = io.BytesIO()
        sudoku.set_args(None)
        sys.stdout = self._save_stdout

        self._p1_score = 2.0
        self._p2_score = 3.0
        self._p3_score = 2.5
        self._p4_score = 2.5
        self._p5_score = 1.0
        self._p6_score = 1.0
        self._p7_score = 3.0
        self._p1_score_max = 2.0
        self._p2_score_max = 3.0
        self._p3_score_max = 2.5
        self._p4_score_max = 2.5
        self._p5_score_max = 1.0
        self._p6_score_max = 1.0
        self._p7_score_max = 3.0
        self.gs = gs_flag

    # output prining code
    def gsOutput(self):
        totalScore = sum([self._p1_score, self._p2_score, self._p3_score, self._p4_score, self._p5_score, self._p6_score, self._p7_score])
        maxScore = sum([self._p1_score_max, self._p2_score_max, self._p3_score_max, self._p4_score_max, self._p5_score_max, self._p6_score_max, self._p7_score_max])
        json = '{"output": "Total score (' + str(totalScore) + ' / ' + str(maxScore) + ')"," tests": ['
        question_text = str(self._p1_score) + '/' + str(self._p1_score_max)
        json += '{"output": "' + question_text + '", "score": ' + str(self._p1_score) + ', "max_score": ' + str(self._p1_score_max) + ', "name": "P1", "tags": []},'
        question_text = str(self._p2_score) + '/' + str(self._p2_score_max)
        json += '{"output": "' + question_text + '", "score": ' + str(self._p2_score) + ', "max_score": ' + str(self._p2_score_max) + ', "name": "P2", "tags": []},'
        question_text = str(self._p3_score) + '/' + str(self._p3_score_max)
        json += '{"output": "' + question_text + '", "score": ' + str(self._p3_score) + ', "max_score": ' + str(self._p3_score_max) + ', "name": "P3", "tags": []},'
        question_text = str(self._p4_score) + '/' + str(self._p4_score_max)
        json += '{"output": "' + question_text + '", "score": ' + str(self._p4_score) + ', "max_score": ' + str(self._p4_score_max) + ', "name": "P4", "tags": []},'
        question_text = str(self._p5_score) + '/' + str(self._p5_score_max)
        json += '{"output": "' + question_text + '", "score": ' + str(self._p5_score) + ', "max_score": ' + str(self._p5_score_max) + ', "name": "P5", "tags": []},'
        question_text = str(self._p6_score) + '/' + str(self._p6_score_max)
        json += '{"output": "' + question_text + '", "score": ' + str(self._p6_score) + ', "max_score": ' + str(self._p6_score_max) + ', "name": "P6", "tags": []},'
        question_text = str(self._p7_score) + '/' + str(self._p7_score_max)
        json += '{"output": "' + question_text + '", "score": ' + str(self._p7_score) + ', "max_score": ' + str(self._p7_score_max) + ', "name": "P7", "tags": []},'
        temp = list(json) # need to remove trailin comma and replace with close bracket
        temp[-1] = ']'
        json = ('').join(temp)        
        json += ', "score": ' + str(totalScore) + ', "max_score": ' + str(maxScore) + ', "visibility": "visible"' + ', "stdout_visibility": "visible"' + '}'
        f = open('grade.json', 'w')
        f.write(json.encode('UTF-8'))

    # Helper Functions
    def quiet(self, func, *args):
        """
        Suppresses the stdout of a function
        """
        self._save_stdout = sys.stdout
        sys.stdout = io.BytesIO()
        try:
            tmp = func(*args)
            sys.stdout = self._save_stdout
            return tmp
        except:
            pass
        sys.stdout = self._save_stdout
        return None

    def variable_domain_checker(self, domain, expected_domain):
        domain = set(domain)
        expected_domain = set(expected_domain)
        for elt in domain:
            if elt and elt not in expected_domain:
                return False
            if elt:
                expected_domain.remove(elt)
        return len(expected_domain) == 0

    def csp_solve(self, problem):
        statesExplored = 0
        frontier = [problem]
        while frontier:
            state = frontier.pop()
            statesExplored += 1
            if state.complete():
                return (state, statesExplored)
            else:
                successors = state.getSuccessors()
                frontier.extend(successors)
        return None

    def csp_solve_fwd(self, problem):
        statesExplored = 0
        frontier = [problem]
        while frontier:
            state = frontier.pop()
            statesExplored += 1
            if state.complete():
                return (state, statesExplored)
            else:
                successors = state.getSuccessorsWithForwardChecking()
                frontier.extend(successors)
        return None

    def checkRowConsistency(self, problem):
        for r in range(9):
            values = dict([(i, 0) for i in range(1, 10)])
            for c in range(9):
                if problem.board[r][c] in values:
                    del values[problem.board[r][c]]
                elif not problem.board[r][c]:
                    continue
                else:
                    return False
        return True

    def swap(self, problem, v0, v1):
        elt0 = problem.board[v0[0]][v0[1]]
        elt1 = problem.board[v1[0]][v1[1]]
        problem.board[v0[0]][v0[1]] = elt1
        problem.board[v1[0]][v1[1]] = elt0

    def solveLocal(self, problem):
        for r in range(1):
            problem.randomRestart()
            state = problem
            for i in range(100000):
                originalConflicts = state.numConflicts()
                v1, v2 = self.quiet(state.randomSwap)

                self.quiet(state.gradientDescent, v1, v2)

                if state.numConflicts() == 0:
                    return state
        return state

    # Grade Function
    def grade(self):
        ################################ PART 1 TESTS ################################
        print('TESTING PART 1: firstEpsilonVariable, complete, variableDomain')
        s0 = sudoku.Sudoku(boardDone)
        s1 = sudoku.Sudoku(boardM00)
        s2 = sudoku.Sudoku(boardM36Pc)

        try:
            index0 = self.quiet(s0.firstEpsilonVariable)
            index1 = self.quiet(s1.firstEpsilonVariable)
            index2 = self.quiet(s2.firstEpsilonVariable)
            assert(not index0)
            assert(index1 == (0, 0) or index1 == [0, 0])
            assert(index2 == (1, 6) or index2 == [1, 6])
        except:
            print('-0.5 -- firstEpsilonVariable failed!\n'
                  'Did you make sure to 0 index and follow the commented hints?\n')
            self._p1_score -= 0.5

        try:
            complete0 = self.quiet(s0.complete)
            complete1 = self.quiet(s1.complete)
            complete2 = self.quiet(s2.complete)
            assert(complete0)
            assert(not complete1)
            assert(not complete2)
        except:
            print('-0.5 -- complete failed!\n')
            self._p1_score -= 0.5

        try:
            vd0 = self.quiet(s0.variableDomain, 0, 0)
            vd1 = self.quiet(s1.variableDomain, 0, 0)
            vd2 = self.quiet(s2.variableDomain, 3, 6)
            assert(not vd0)
            assert(self.variable_domain_checker(vd1, [7]))
            assert(self.variable_domain_checker(vd2, [2, 6]))
        except:
            print('-1.0 -- variableDomain failed!\n'
                  'Did you make sure to return a list?  [] if empty?\n')
            self._p1_score -= 1.0

        print('PART 1 SCORE: {}/2.0\n\n'.format(self._p1_score))

        ################################ PART 2 TESTS ################################
        print('TESTING PART 2: updateFactor, updateAllFactors, updateVariableFactors')
        s0 = sudoku.Sudoku(boardDone)
        s1 = sudoku.Sudoku(boardM00)
        s2 = sudoku.Sudoku(boardM00c)
        s3 = sudoku.Sudoku(boardM36Pc)

        try:
            self.quiet(s0.updateFactor, 1, 0)
            assert(len(s0.factorNumConflicts.keys()) == 1 and
                   len(s0.factorRemaining.keys()) == 1)
            assert(s0.factorNumConflicts[(1, 0)] == 0)
            assert(self.variable_domain_checker(s0.factorRemaining[(1, 0)], []))

            self.quiet(s1.updateFactor, 2, 0)
            assert(len(s1.factorNumConflicts.keys()) == 1 and
                   len(s1.factorRemaining.keys()) == 1)
            assert(s1.factorNumConflicts[(2, 0)] == 0)
            assert(self.variable_domain_checker(s1.factorRemaining[(2, 0)], [7]))

            self.quiet(s2.updateFactor, 1, 0)
            self.quiet(s2.updateFactor, 2, 0)
            assert(len(s2.factorNumConflicts.keys()) == 2
                   and len(s2.factorRemaining.keys()) == 2)
            assert(s2.factorNumConflicts[(1, 0)] == 1
                   and s2.factorNumConflicts[(2, 0)] == 1)
            assert(self.variable_domain_checker(s2.factorRemaining[(1, 0)], [7, 9]))
            assert(self.variable_domain_checker(s2.factorRemaining[(2, 0)], [7, 9]))
            self.quiet(s2.updateFactor, 3, 0)
            assert(s2.factorNumConflicts[(1, 0)] == 1
                   and s2.factorNumConflicts[(2, 0)] == 1
                   and s2.factorNumConflicts[(3, 0)] == 0)
            assert(self.variable_domain_checker(s2.factorRemaining[(2, 0)], [7, 9]))
            assert(self.variable_domain_checker(s2.factorRemaining[(3, 0)], [7]))
        except:
            print('-2.0 -- updateFactor failed!\n'
                  'Did you add an entry in the self.factorNumConflicts and '
                  'self.factorRemaining dicts?  Did you account for the different '
                  'factor types?\n')
            self._p2_score -= 2.0

        try:
            self.quiet(s0.updateAllFactors)
            assert(len(s0.factorNumConflicts.keys()) == 27
                   and len(s0.factorRemaining.keys()) == 27)
            assert(s0.factorNumConflicts[(1, 0)] == 0)
            assert(self.variable_domain_checker(s0.factorRemaining[(1, 0)], []))

            self.quiet(s2.updateAllFactors)
            assert(len(s2.factorNumConflicts.keys()) == 27 and
                   len(s2.factorRemaining.keys()) == 27)
            assert(sum(s2.factorNumConflicts.values()) == 3)
        except:
            print('-0.5 -- updateAllFactors failed!\n')
            self._p2_score -= 0.5

        try:
            s2 = sudoku.Sudoku(boardM00c)
            self.quiet(s2.updateVariableFactors, (0, 0))
            assert(s2.factorNumConflicts[(1, 0)] == 1 and
                   s2.factorNumConflicts[(2, 0)] == 1 and
                   s2.factorNumConflicts[(3, 0)] == 0)
            assert(self.variable_domain_checker(s2.factorRemaining[(2, 0)], [7, 9]))
            assert(self.variable_domain_checker(s2.factorRemaining[(3, 0)], [7]))
            assert(sum(s2.factorNumConflicts.values()) == 2)

            self.quiet(s3.updateVariableFactors, (3, 6))
            assert(s3.factorNumConflicts.keys() == [(1, 5), (2, 3), (3, 6)])
            assert(self.variable_domain_checker(s3.factorRemaining[(1, 5)],
                   [1, 2, 3, 5, 6, 7, 8, 9]))
            assert(sum(s3.factorNumConflicts.values()) == 5)
            self.quiet(s3.updateAllFactors)
            assert(len(s3.factorNumConflicts.keys()) == 27 and
                   len(s3.factorRemaining.keys()) == 27)
            assert(sum(s3.factorNumConflicts.values()) == 12)
        except:
            print('-0.5 -- updateVariableFactors failed!\n')
            self._p2_score -= 0.5

        print('PART 2 SCORE: {}/3.0\n\n'.format(self._p2_score))

        ################################ PART 3 TESTS ################################
        print('TESTING PART 3: getSuccessors')

        try:
            s = sudoku.Sudoku(boardDone)
            successors = self.quiet(s.getSuccessors)
            assert(not successors or successors == [])

            s = sudoku.Sudoku(boardM00)
            successors = s.getSuccessors()
            assert(len(successors) == 1)
            assert(successors[0].board == boardDone)

            s = sudoku.Sudoku(boardM36)
            successors = s.getSuccessors()
            assert(len(successors) == 1)
            assert(successors[0].board == boardM36D)
        except:
            print('-1.5 -- getSuccessors: complete board or board missing one entry '
                  'incorrect successors.\n')
            self._p3_score -= 1.5

        try:
            s = sudoku.Sudoku(boardM36)
            solved, states_explored = self.csp_solve(s)
            assert(solved)
            assert(solved.board == boardM36D)
            assert(states_explored < 4)

            s = sudoku.Sudoku(boardEasy)
            solved, states_explored = self.csp_solve(s)
            assert(solved)
            assert(states_explored < 400)
        except:
            print('-1.0 -- getSuccessors: could not solve sudoku boards and/or too '
                  'many states expanded.\n')
            self._p3_score -= 1.0

        print('PART 3 SCORE: {}/2.5\n\n'.format(self._p3_score))

        ################################ PART 4 TESTS ################################
        print('TESTING PART 4: forwardCheck')

        try:
            s = sudoku.Sudoku(boardDone)
            assert(s.forwardCheck())
            s = sudoku.Sudoku(boardM36)
            assert(s.forwardCheck())
            s = sudoku.Sudoku(boardImpossible)
            assert(not s.forwardCheck())
        except:
            print('-1.0 -- forwardCheck: function fails on simple board tests')
            self._p4_score -= 1.0

        try:
            s = sudoku.Sudoku(boardM36)
            successors = s.getSuccessorsWithForwardChecking()
            assert(len(successors) == 1)
            assert(successors[0].board == boardM36D)
        except:
            print('-0.5 -- forwardCheck: getSuccessorsWithForwardChecking fails on '
                  'board missing one entry')
            self._p4_score -= 0.5


        try:
            s = sudoku.Sudoku(boardHard)
            solved, states_explored = self.csp_solve_fwd(s)
            assert(solved)
        except:
            print('-0.5 -- forwardCheck: could not solve full sudoku')
            self._p4_score -= 0.5

        try:
            s = sudoku.Sudoku(boardEasy)
            _, states_explored = self.csp_solve_fwd(s)
            _, states_explored2 = self.csp_solve(s)
            assert(states_explored <= states_explored2)
        except:
            print('-0.5 -- forwardCheck: too many states expanded')
            self._p4_score -= 0.5

        print('PART 4 SCORE: {}/2.5\n\n'.format(self._p4_score))

        ################################ PART 5 TESTS ################################
        print('TESTING PART 5: randomRestart')

        try:
            s = sudoku.Sudoku(copy.deepcopy(boardDone), isFirstLocal=True)
            self.quiet(s.randomRestart)
            isComplete = self.quiet(s.complete)
            isRowConsistent = self.checkRowConsistency(s)
            assert(isComplete)
            assert(isRowConsistent)

            s = sudoku.Sudoku(copy.deepcopy(boardM00), isFirstLocal=True)
            self.quiet(s.randomRestart)
            isComplete = self.quiet(s.complete)
            isRowConsistent = self.checkRowConsistency(s)
            assert(isComplete)
            assert(isRowConsistent)

            s = sudoku.Sudoku(copy.deepcopy(boardEasy), isFirstLocal=True)
            self.quiet(s.randomRestart)
            isComplete = self.quiet(s.complete)
            isRowConsistent = self.checkRowConsistency(s)
            assert(isComplete)
            assert(isRowConsistent)
        except:
            print('-1.0 -- randomRestart failed to complete boards with consistent '
                  'rows.  Did you make sure to ensure row consistency?')
            self._p5_score -= 1.0

        print('PART 5 SCORE: {}/1.0\n\n'.format(self._p5_score))

        ################################ PART 6 TESTS ################################
        print('TESTING PART 6: randomSwap')

        try:
            s = sudoku.Sudoku(copy.deepcopy(boardEasy), isFirstLocal=True)
            s.fixedVariables = {}
            for i in range(10):
                v0, v1 = self.quiet(s.randomSwap)
                self.swap(s, v0, v1)
                isRowConsistent = self.checkRowConsistency(s)
                assert(isRowConsistent)

            s = sudoku.Sudoku(copy.deepcopy(boardHard), isFirstLocal=True)
            s.fixedVariables = {}
            for i in range(10):
                v0, v1 = self.quiet(s.randomSwap)
                self.swap(s, v0, v1)
                isRowConsistent = self.checkRowConsistency(s)
                assert(isRowConsistent)

            s = sudoku.Sudoku(copy.deepcopy(boardM36P), isFirstLocal=True)
            s.fixedVariables = {}
            for i in range(10):
                v0, v1 = self.quiet(s.randomSwap)
                self.swap(s, v0, v1)
                isRowConsistent = self.checkRowConsistency(s)
                assert(isRowConsistent)
        except:
            print('-1.0 -- randomSwap returned two variables that when swapped made '
                  'the board row inconsistent.\n')
            self._p6_score -= 1.0

        print('PART 6 SCORE: {}/1.0\n\n'.format(self._p6_score))

        ################################ PART 7 TESTS ################################
        print('TESTING PART 7: gradientDescent')

        test_part_seven = True
        try:
            s = sudoku.Sudoku(copy.deepcopy(boardEasy), isFirstLocal=True)
            v1, v2 = s.randomSwap()
            s.gradientDescent(v1, v2)
        except NotImplementedError:
            # Have not implemented gradientDescent yet, so don't proceed
            self._p7_score -= 3.0
            test_part_seven = False

        if test_part_seven:
            try:
                s = sudoku.Sudoku(copy.deepcopy(boardEasy), isFirstLocal=True)
                p = multiprocessing.Process(
                    target=self.solveLocal, name="solveLocal", args=(s,))
                p.start()
                p.join(60)
                if p.is_alive():
                    p.terminate()
                    p.join()
                    assert(False)
                state = self.solveLocal(s)

                # print "num of conflicts for boardEasy", state.numConflicts()
                assert(state.numConflicts() <= 10)
            except:
                print '-1.5 -- test of gradient descent boardEasy failed'
                self._p7_score -= 1.5

            # 1 point off if it fails boardHard

            try:
                s = sudoku.Sudoku(copy.deepcopy(boardHard), isFirstLocal=True)
                p = multiprocessing.Process(
                    target=self.solveLocal, name="solveLocal", args=(s,))
                p.start()
                p.join(60)
                if p.is_alive():
                    p.terminate()
                    p.join()
                    assert(False)
                state = self.solveLocal(s)

                # print "num of conflicts for boardHard", state.numConflicts()
                assert(state.numConflicts() <= 20)
            except:
                print '-1.5 -- test of gradient descent boardHard failed'
                self._p7_score -= 1.5

        print('PART 7 SCORE: {}/3.0\n\n'.format(self._p7_score))
        scores = [self._p1_score, self._p2_score, self._p3_score, self._p4_score, self._p5_score, self._p6_score, self._p7_score]
        print('FINAL SCORE: {}/15.0\n\n'.format(sum(scores)))
        self.gsOutput()
