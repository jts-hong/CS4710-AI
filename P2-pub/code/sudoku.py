from copy import deepcopy
import timeit
import os
import sys
import random
import argparse

BOX = 1
ROW = 2
COL = 3

random.seed(18)  # IMPORTANT: DO NOT REMOVE!


def crossOff(values, nums):
    """
    Removes seen nums from domain values (removes all the elements in values
    that are also in nums).
    Also counts the possible constraint violations.
    """
    violations = 0
    for n in nums:
        if n:
            if not values[n-1]:
                violations += 1
            values[n-1] = None
    return violations


class Sudoku:
    def __init__(self, board, lastMoves=[], isFirstLocal=False):
        self.board = board

        # Used for visualization.
        self.lastMoves = lastMoves

        # The values still remaining for a factor.
        self.factorRemaining = {}

        # The number of conflicts at a factor.
        self.factorNumConflicts = {}

        # For local search. Keep track of the factor state.
        if isFirstLocal:
            self._initLocalSearch()

    # BASE SUDOKU CODE
    def row(self, row):
        "The variable assignments for a row factor."
        return list(self.board[row])

    def col(self, col):
        "The variable assignments for a col factor."
        return [row[col] for row in self.board]

    def box(self, b):
        "The variable assignments for a box factor."
        row = int(b / 3)
        col = b % 3
        nums = []
        for x in xrange(row * 3, row * 3 + 3):
            for y in xrange(col * 3, col * 3 + 3):
                nums.append(self.board[x][y])
        return nums

    def box_id(self, row, col):
        "Map variable coord to a box factor id."
        rowmin = int(row / 3)
        colmin = int(col / 3)
        return rowmin * 3 + colmin

    def setVariable(self, row, col, val):
        """
        Creates a new version of the board with a variable
        set to `val`.
        """
        newBoard = deepcopy(self.board)
        newBoard[row][col] = val
        return Sudoku(newBoard, [(row, col)])

    # PART 1
    def firstEpsilonVariable(self):
        """
        IMPLEMENT FOR PART 1
        Returns the first variable with assignment epsilon, otherwise return
        None (i.e. first square in the board that is unassigned -- 0).

        NOTE: for the sake of the autograder, please search for the first
        unassigned variable column-wise, then row-wise:
        """
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c]== 0:
                    return (r,c)
        return None
        raise NotImplementedError()

    def complete(self):
        """
        IMPLEMENT FOR PART 1
        Returns true if the assignment is complete

        i.e. if there are no more first epsilon variables
        """
        return self.firstEpsilonVariable() == None

        raise NotImplementedError()

    def variableDomain(self, r, c):
        """
        IMPLEMENT FOR PART 1
        Returns current domain for the (row, col) variable, and [] if the
        domain is empty.

        i.e. return a list of the possible number assignments to this variable
        without breaking consistency for its row, column, or box.
        """
        res = [1,2,3,4,5,6,7,8,9]
        a=self.row(r)
        for x in a:
            if x in res:
                res.remove(x)
        b = self.col(c)
        for x in b:
            if x in res:
                res.remove(x)
        id = self.box_id(r,c)
        bo = self.box(id)
        for x in bo:
            if x in res:
                res.remove(x)
        return res

        raise NotImplementedError()

    # PART 2
    def updateFactor(self, factor_type, i):
        """
        IMPLEMENT FOR PART 2
        Update the values remaining for a factor.
        `factor_type` is one of BOX, ROW, COL
        `i` is an index between 0 and 8.

        i.e. update factorNumConflicts to contain the number of conflicts
        present at a factor (how many elements to remove to not be in conflict)
        and factorRemaining to contain the remaining numbers not yet assigned
        in the factor.

        Hint: crossOff may be useful here
        """

    
        values = [1,2,3,4,5,6,7,8,9]
        if factor_type == BOX:
            nums = self.box(i)
            conf = crossOff(values,nums)
        if factor_type == ROW:
            nums = self.row(i)
            conf = crossOff(values,nums)
        if factor_type == COL:
            nums = self.col(i)
            conf = crossOff(values,nums)
        self.factorNumConflicts[factor_type,i]= conf
        self.factorRemaining[factor_type,i]=values
        #raise NotImplementedError()

    def updateAllFactors(self):
        """
        IMPLEMENT FOR PART 2
        Update the values remaining for all factors.
        There is one factor for each row, column, and box.
        """
        for x in range(9):
            self.updateFactor(BOX,x)
        for x in range(9):
            self.updateFactor(ROW,x)
        for x in range(9):
            self.updateFactor(COL,x)
        #raise NotImplementedError()

    def updateVariableFactors(self, variable):
        """
        IMPLEMENT FOR PART 2
        Update all the factors impacting a variable (neighbors in factor graph).
        """
        a,b = variable
        box = self.box_id(a,b)

        self.updateFactor(BOX,box)
        self.updateFactor(ROW,a)
        self.updateFactor(COL,b)
        #raise NotImplementedError()

    # CSP SEARCH CODE
    def nextVariable(self):
        """
        Return the next variable to try assigning.
        """
        if args.mostconstrained:
            return self.mostConstrainedVariable()
        else:
            return self.firstEpsilonVariable()

    # PART 3
    def getSuccessors(self):
        """
        IMPLEMENT IN PART 3
        Returns new assignments with each possible value
        assigned to the variable returned by `nextVariable`.  If no valid
        assignments exist, return [].

        i.e. get the next variable to assign, and return a list of all possible
        boards, with that variable assigned to all possible values in its
        domain.

        Hint: setVariable and variableDomain will be useful
        """
        nextVariable =  self.nextVariable()
        res = self.variableDomain(nextVariable[0],nextVariable[1])
        ls = []
        for i in res:
            ls.append(self.setVariable(nextVariable[0],nextVariable[1],i))
        return ls
        
        #raise NotImplementedError()

    def getAllSuccessors(self):
        if not args.forward:
            return self.getSuccessors()
        else:
            return self.getSuccessorsWithForwardChecking()

    # PART 4
    def getSuccessorsWithForwardChecking(self):
        return [s for s in self.getSuccessors() if s.forwardCheck()]

    def forwardCheck(self):
        """
        IMPLEMENT IN PART 4
        Returns True if all variables have non-empty domains, o.w. False.

        i.e. make sure that for every unassigned element in the board, that
        element has a non-trivial domain (its domain isn't empty)
        """
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j]==0 and len(self.variableDomain(i,j))==0:
                    return False
        return True
        raise NotImplementedError()

    # LOCAL SEARCH CODE
    # Fixed variables cannot be changed by the player.
    def _initLocalSearch(self):
        """
        Variables for keeping track of inconsistent, complete
        assignments. (Complete assignment formulism)
        """

        # For local search. Remember the fixed numbers.
        self.fixedVariables = {}
        for r in xrange(0, 9):
            for c in xrange(0, 9):
                if self.board[r][c]:
                    self.fixedVariables[r, c] = True
        self.updateAllFactors()

    def modifySwap(self, square1, square2):
        """
        Modifies the sudoku board to swap two
        row variable assignments.
        """
        t = self.board[square1[0]][square1[1]]
        self.board[square1[0]][square1[1]] = \
            self.board[square2[0]][square2[1]]
        self.board[square2[0]][square2[1]] = t

        self.lastMoves = [square1, square2]
        self.updateVariableFactors(square1)
        self.updateVariableFactors(square2)

    def numConflicts(self):
        "Returns the total number of conflicts"
        return sum(self.factorNumConflicts.values())

    # PART 5
    def randomRestart(self):
        """
        IMPLEMENT FOR PART 5
        Randomly initialize a complete, potentially inconsistent board, making
        sure that all row factors are being held consistent.  Meaning,
        the board may be inconsistent, but every row must contain each of the
        numbers in the domain.  Also make sure that you check before assigning
        a number to a position that a number isn't ALREADY assigned there!

        NOTE: Please, please, please use random.shuffle() -- will help us out
              on the autograder side!
        """
        for x in range(9):
            val = [1,2,3,4,5,6,7,8,9]
            a = self.row(x)
            for y in a:
                if y in val:
                    val.remove(y)
            random.shuffle(val)
            for z in range(len(self.board[0])):
                if self.board[x][z]==0:
                    self.board[x][z]=val[-1]
                    val.pop()
        self.updateAllFactors() # to call at end of function
        #raise NotImplementedError()
        # self.updateAllFactors() # to call at end of function

    # PART 6
    def randomSwap(self):
        """
        IMPLEMENT FOR PART 6
        Returns two random variables that can be swapped without
        causing a row factor conflict.
        i.e. return (r0, c0), (r1, c1) if v0 and v1 are two non fixed variables
        that can be swapped without causing any row inconsistencies.

        NOTE: DO NOT swap any of the variables already set: fixedVariables
        """

        while(True):
            r = random.randint(0,8)
            c0 = random.randint(0,8)
            c1 = random.randint(0,8)
            c2 = random.randint(0,8)
            if self.fixedVariables.get((r,c0)) or self.fixedVariables.get((r,c2)) or c0 == c1 or c0==c2:
                continue
            return (r,c0),(r,c1)
        raise NotImplementedError()

    # PART 7
    def gradientDescent(self, variable1, variable2):
        """
        IMPLEMENT FOR PART 7
        Decide if we should swap the values of variable1 and variable2.
        """
        tr = deepcopy(self.board)
        v1 = self.board[variable1[0]][variable1[1]]
        v2 = self.board[variable2[0]][variable2[1]]
        tr[variable1[0]][variable1[1]] = v2
        tr[variable2[0]][variable2[1]] = v1
        newS = Sudoku(tr,[])
        newS.updateAllFactors()
        if newS.numConflicts()<= self.numConflicts():
            self.board[variable1[0]][variable1[1]] = v2
            self.board[variable2[0]][variable2[1]] = v1
            self.updateAllFactors()
        '''
        x = self.numConflicts()
        self.modifySwap(variable1,variable2)
        y = self.numConflicts()
        if y<x:
            self.modifySwap(variable2,variable1)
            self.updateAllFactors()
            return True
        self.modifySwap(variable2,variable1)
        self.updateAllFactors()
        return False
        '''
        #raise NotImplementedError()

    ### IGNORE - PRINTING CODE

    def prettyprinthtml(self):
        """
        Pretty print the sudoku board and the factors.
        """
        out = "\n"
        cols = {}
        self.updateAllFactors()

        out = """<style>
         .sudoku .board {
            width: 20pt;
            text-align: center;
            border-color: #AAAAAA;
         }

         .sudoku .out {
            width: 10pt;
            text-align: center;
            border-color: #FFFFFF;
         }

         .sudoku .outtop {
            padding: 0pt;
            text-align: center;
            border-color: #FFFFFF;
         }

        </style>"""
        out += "<center><table class='sudoku' style='border:none;border-collapse:collapse; " + \
               " background-color:#FFFFFF; border: #666699 solid 2px;'>"

        for i in range(9):
            out += "<tr style='border: none;'>"
            for j in range(9):
                cols = self.factorRemaining[COL, j]
                td_style = ""
                if j in [0, 3, 6]:
                    td_style = "border-left: #666699 solid 2px;"
                if j in [8]:
                    td_style = "border-right: #666699 solid 2px;"

                out +=  "<td class='outtop' style='%s'> %s </td>"%(td_style , cols[i] if cols[i] else "   ")
            out += "<td class='outtop'></td>" * 9 +  "</tr>" 

        for i in range(9):
            style = "border: #AAAAAA 1px"
            if i in [0, 3, 6]:
                 style = "border:none; border-collapse:collapse; background-color:#AAAAAA 1px; border-top: #666699 solid 2px"

            out += "<tr style='%s'>"%style
            for j in range(9):
                assign = self.board[i][j]
                td_style = ""
                if j in [0, 3, 6]:
                    td_style = "border-left: #666699 solid 2px;"
                if j in [8]:
                    td_style = "border-right: #666699 solid 2px;"

                if (i, j) in self.lastMoves:
                    td_style += "background-color: #FF0000"
                out += "<td class='board' style='%s'>%s</td>"%(td_style, assign if assign else " ")

            row = self.factorRemaining[ROW, i]

            for j in row:
                out += "<td class='out'>%s</td>"%(str(j) if j else " ")

            out += "</tr>"

        out += "</table></center>"
        return out

    def printhtml(self):
        out = """<style>
         .sudoku td {
            width: 20pt;
            text-align: center;
            border-color: #AAAAAA;
         }

        </style>"""
        out += "<center><table class='sudoku' style='border:none; border-collapse:collapse; background-color:#FFFFFF; border: #666699 solid 2px;'>"

        for i in range(9):
            style = "border: #AAAAAA 1px"
            if i in [3, 6]:
                 style = "border:none; border-collapse:collapse; background-color:#AAAAAA 1px; border-top: #666699 solid 2px"

            out += "<tr style='%s'>"%style
            for j in range(9):
                assign = self.board[i][j]
                td_style = ""
                if j in [3, 6]:
                    td_style = "border-left: #666699 solid 2px;"
                if (i, j) in self.lastMoves:
                    td_style += "background-color: #FF0000"
                out += "<td style='%s'>%s</td>"%(td_style ,  assign if assign else " ")
            out += "</tr>"
        out += "</table></center>"
        return out

    def __str__(self):
        """
        Pretty print the sudoku board and the factors.
        """
        OKGREEN = '\033[92m'
        BOLD = '\033[1m'
        ENDC = '\033[92m'

        out = "\n"
        cols = {}
        self.updateAllFactors()

        out += OKGREEN
        for i in range(10):
            for j in range(9):
                cols = self.factorRemaining[COL, j]
                conf = self.factorNumConflicts[COL, j]
                if j in [3, 6]:
                    out += "| "
                if i < 9:
                    out +=  (" %d "%(cols[i]) if cols[i] else "   ") + " "
                else:
                    out +=  ("(%d)"%(conf)) +  " "
            out += "\n"

        out += ENDC
        out += "........................................\n\n"
        for i in range(9):
            if i in [3, 6]:
                out += "----------------------------------------\n\n"
            row = self.factorRemaining[ROW, i]
            conf = self.factorNumConflicts[ROW, i]
            vals = " " .join((str(j) if j else " " for j in row ))

            out += "%s %s %s | %s %s %s | %s %s %s : %s (%d) \n\n"%(
                tuple([((BOLD + " %d " + ENDC)%(assign) if (i, j) in self.lastMoves
                        else " %d "%(assign) if assign
                        else "X-%d"%(len(self.variableDomain(i, j))))
                       for j, assign in enumerate(self.board[i]) ])
                + (vals,conf))

        return out


def solveCSP(problem):
    statesExplored = 0
    frontier = [problem]
    while frontier:
        state = frontier.pop()

        statesExplored += 1
        if state.complete():
            print 'Number of explored: ' + str(statesExplored)
            return state
        else:
            successors = state.getAllSuccessors()
            if args.debug:
                if not successors:
                    print "DEADEND BACKTRACKING \n"
            frontier.extend(successors)

        if args.debug:
            os.system("clear")
            print state
            raw_input("Press Enter to continue...")

        if args.debug_ipython:
            from time import sleep
            from IPython import display
            display.display(display.HTML(state.prettyprinthtml()))
            display.clear_output(True)
            sleep(0.5)

    return None

def solveLocal(problem):
    for r in range(1):
        problem.randomRestart()
        state = problem
        for i in range(100000):
            originalConflicts = state.numConflicts()

            v1, v2 = state.randomSwap()

            state.gradientDescent(v1, v2)

            if args.debug_ipython:
                from time import sleep
                from IPython import display
                state.lastMoves = [s1, s2]
                display.display(display.HTML(state.prettyprinthtml()))
                display.clear_output(True)
                sleep(0.5)

            if state.numConflicts() == 0:
                return state
                break

            if args.debug:
                os.system("clear")
                print state
                raw_input("Press Enter to continue...")


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

start = None
args = None


def set_args(arguments):
    global start, args
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--easy', default=False, help="Use easy board.")
    parser.add_argument('--debug', default=False, help="Print each state.")
    parser.add_argument('--debug_ipython', default=False,
                        help="Print each state in html.")

    parser.add_argument('--localsearch', default=False,
                        help="Use local search.")
    parser.add_argument('--mostconstrained', default=False,
                        help="Use most constrained heuristic.")
    parser.add_argument('--forward', default=False,
                        help="Use forward checking.")
    parser.add_argument('--time', default=False)

    args = parser.parse_args(arguments)


def main(arguments):
    global start, args
    set_args(arguments)
    start = Sudoku(boardEasy if args.easy else boardHard,
                   isFirstLocal=args.localsearch)

    print args

    setup = '''
from __main__ import start, solveLocal, solveCSP
'''
    solveSudoku = '''
print 'Solution: ' + str(solveCSP(start))
'''
    solveSudokuLocal = '''
print 'Solution: ' + str(solveLocal(start))
'''

    print 'Time elapsed: ' + str(timeit.timeit(
            solveSudokuLocal if args.localsearch else solveSudoku,
            setup=setup, number=1))


def doc(fn):
    import pydoc
    import IPython.display
    return IPython.display.HTML(pydoc.html.docroutine(fn))
    # print pydoc.render_doc(fn, "Help on %s")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
