# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Get a list of distance from current position to all the ghosts
        Ghosts = []
        for ghost in newGhostStates:
            dist = manhattanDistance(ghost.getPosition(), newPos)
            Ghosts.append(dist)
        # Only consider the nearest ghost
        nearestGhost = min(Ghosts)

        # food heuristic is between 0 ~ 10, next state if get food + 10
        if nearestGhost < 2:
            ghostHeuristic = -20
        else:
            ghostHeuristic = 0

        # find the nearest food
        if len(newFood.asList()) > 0:
            Foods = []
            for food in newFood.asList():
                dist = manhattanDistance(food, newPos)
                Foods.append(dist)
            nearestFood = min(Foods)
            # If eat the food beside, point = 10 - 1
            # eat the food +10, move one step -1
            foodHeuristic = 9 / nearestFood
        else:
            foodHeuristic = 0

        return successorGameState.getScore() + ghostHeuristic + foodHeuristic


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # default value = negative infinity
        maxValue = -float('inf')
        bestAction = None
        for action in gameState.getLegalActions(0):
            value = self.getMin(gameState.generateSuccessor(0, action), 0, 1)
            if value > maxValue:
                maxValue = value
                bestAction = action
        return bestAction

    def getMax(self, gameState, depth=0, agentIndex=0):
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        maxValue = -float('inf')
        for action in gameState.getLegalActions(agentIndex):
            value = self.getMin(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
            if value > maxValue:
                maxValue = value
        return maxValue

    def getMin(self, gameState, depth=0, agentIndex=1):
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        minValue = float('inf')
        for action in gameState.getLegalActions(agentIndex):
            if agentIndex == gameState.getNumAgents() - 1:
                value = self.getMax(gameState.generateSuccessor(agentIndex, action), depth + 1, 0)
            else:
                value = self.getMin(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
            if value < minValue:
                minValue = value
        return minValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        maxVal, bestAction = self.getMax(gameState)
        return bestAction

    def getMax(self, gameState, depth=0, agentIndex=0, alpha=-float('inf'), beta=float('inf')):
        if depth == self.depth:
            return self.evaluationFunction(gameState), None
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState), None
        maxValue = -float('inf')
        bestAction = None
        for action in gameState.getLegalActions(agentIndex):
            value = self.getMin(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)[0]
            if value > maxValue:
                maxValue = value
                bestAction = action
            if value > beta:
                return value, action
            alpha = value if value > alpha else alpha
        return maxValue, bestAction

    def getMin(self, gameState, depth=0, agentIndex=1, alpha=-float('inf'), beta=float('inf')):
        if depth == self.depth:
            return self.evaluationFunction(gameState), None
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState), None
        minValue = float('inf')
        bestAction = None
        for action in gameState.getLegalActions(agentIndex):
            if agentIndex == gameState.getNumAgents() - 1:
                value = self.getMax(gameState.generateSuccessor(agentIndex, action), depth + 1, 0, alpha, beta)[0]
            else:
                value = \
                self.getMin(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)[0]
            if value < minValue:
                minValue = value
                bestAction = action
            if value < alpha:
                return value, action
            beta = value if value < beta else beta
        return minValue, bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        result = self.value(gameState, 0, 0)
        return result[0]

    def value(self, gameState, agentIndex, crrdepth):
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            crrdepth += 1
        if crrdepth == self.depth:
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, crrdepth)
        else:
            return self.expValue(gameState, agentIndex, crrdepth)

    def maxValue(self, gameState, agentIndex, crrdepth):
        v = ("unknown", float("-inf"))

        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

        for action in gameState.getLegalActions(agentIndex):
            if action == "Stop":
                continue

            next = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, crrdepth)

            if type(next) is tuple:
                update = max(v[1], next[1])
            else:
                update = max(v[1], next)

            if update != v[1]:
                v = (action, update)

        return v

    def expValue(self, gameState, agentIndex, crrdepth):
        v = ["unknown", 0]

        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        p = 1 / len(gameState.getLegalActions(agentIndex))

        for action in gameState.getLegalActions(agentIndex):
            if action == "Stop":
                continue

            next = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, crrdepth)

            if type(next) is tuple:
                v[1] += next[1] * p
            else:
                v[1] += next * p

            v[0] = action

        return tuple(v)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

    ghost_distances = []
    for ghost in GhostStates:
        ghost_distances += [manhattanDistance(ghost.getPosition(), curPos)]
    nearestGhost = min(ghost_distances)

    foodList = curFood.asList()
    food_distences = []
    if len(foodList) > 0:
        for food in foodList:
            food_distences += [manhattanDistance(food, curPos)]
        nearestFood = min(food_distences)

    scared = False
    for time in scaredTimes:
        if time != 0:
            scared = True
        else:
            scared = False
            break

    foodHeuristic = 0
    ghostHeuristic = 0

    if len(food_distences) > 0 and nearestFood > 0:
        foodHeuristic = 1 / nearestFood
        if nearestGhost < 2:
            ghostHeuristic = -10

    if scared and nearestGhost != 0:
        nearestGhost = 0.5/nearestGhost

    return currentGameState.getScore() + foodHeuristic + ghostHeuristic



# Abbreviation
better = betterEvaluationFunction
