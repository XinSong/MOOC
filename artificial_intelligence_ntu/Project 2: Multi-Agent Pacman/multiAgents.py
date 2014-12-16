# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"
    "*** YOUR CODE HERE ***"
    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    if successorGameState.isWin():
      return float("inf")
    if successorGameState.isLose():
      return float("-inf")
    
    if action == Directions.STOP:
      return successorGameState.getScore() - 1

    capsules = successorGameState.getCapsules()
    horribleGhostDistance = [ manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates if ghost.scaredTimer <= 0]
    #scaredGhostDistance = [ manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates if ghost.scaredTimer > 0 ]
    score = successorGameState.getScore()

    if horribleGhostDistance:
      if min(horribleGhostDistance) <= 1:
        return float("-inf")
      else:
        score -= 0.5 / min(horribleGhostDistance)

    if currentGameState.getNumFood() > successorGameState.getNumFood():
      return float("inf")

    if len(currentGameState.getCapsules()) > len(successorGameState.getCapsules()):
      return float("inf")

    if capsules:
      score += 1.0 / min( [manhattanDistance(newPos, capsule) for capsule in capsules] ) 

    
    newFood = successorGameState.getFood()
    minFoodDistance = min([ manhattanDistance(newPos, (x,y)) for x in range(0, newFood.width) for y in range(0,newFood.height) if newFood[x][y] ])

    score += 1.0 / minFoodDistance 

    return score

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

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    bestScore = float('-inf')
    bestAction = Directions.STOP
    for action in gameState.getLegalActions():
      if action == Directions.STOP:
        continue
      score = self.MinMax(gameState.generateSuccessor(0, action), 1, 1)
#        score -= 1.0
      if bestScore < score:
        bestScore = score
        bestAction = action
    return bestAction

  def MinMax(self, gameState, depth, agentIndex):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    agentNum = gameState.getNumAgents()
    if agentIndex == 0 or agentIndex >= agentNum: #PACMAN
      return max([self.MinMax(gameState.generateSuccessor(0, action), depth + 1, 1) for action in gameState.getLegalActions(0) if action != Directions.STOP])
    elif agentIndex == agentNum - 1: #The Last GHOST
      if depth == self.depth:
        return min([self.evaluationFunction(gameState.generateSuccessor(agentIndex, action)) for action in gameState.getLegalActions(agentIndex)])
      else:
        return min([self.MinMax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1) for action in gameState.getLegalActions(agentIndex)])
    else:  #Other GHOST
      return min([self.MinMax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1) for action in gameState.getLegalActions(agentIndex)])

#    agentNum = gameState.getNumAgents()
#    if ( depth == 0 and agentIndex == 0 ) or gameState.isWin() or gameState.isLose():
#      return self.evaluationFunction(gameState)
#
#    if agentIndex == 0 or agentIndex >= agentNum: #PACMAN
#      return max([self.MinMax(gameState.generateSuccessor(0, action), depth, 1) for action in gameState.getLegalActions(0) if action != Directions.STOP])
#    elif agentIndex == agentNum - 1: #The Last GHOST
#      return min([self.MinMax(gameState.generateSuccessor(agentIndex, action), depth - 1, agentIndex+1) for action in gameState.getLegalActions(agentIndex)])
#    else:  #Other GHOST
#      return min([self.MinMax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1) for action in gameState.getLegalActions(agentIndex)])
              

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    bestScore = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for action in gameState.getLegalActions():
      if action == Directions.STOP:
        continue
      v = self.AlphaBetaPrune(gameState.generateSuccessor(0, action), 1, 1, alpha, beta)
      if bestScore < v:
        bestScore = alpha = v
        bestAction = action
    return bestAction

  def AlphaBetaPrune(self, gameState, depth, agentIndex, alpha, beta):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    agentNum = gameState.getNumAgents()
    if agentIndex == 0 or agentIndex >= agentNum: #PACMAN
      v = float('-inf')
      for action in gameState.getLegalActions(0):
        if action == Directions.STOP:
          continue
        successor = gameState.generateSuccessor(0, action)
        v = max(v, self.AlphaBetaPrune(successor, depth, 1, alpha, beta))
        if v > beta:
          return v
        alpha = max(alpha, v)
      return v
    else:
      if agentIndex == agentNum - 1:
        if depth == self.depth:
          return min([self.evaluationFunction(gameState.generateSuccessor(agentIndex,action)) for action in gameState.getLegalActions(agentIndex)]) 
        else:
          depth += 1

      v = float('inf')
      for action in gameState.getLegalActions(agentIndex):
        successor = gameState.generateSuccessor(agentIndex, action)
        v = min(v, self.AlphaBetaPrune(successor, depth, agentIndex+1, alpha, beta))
        if v < alpha:
          return v
        beta = min(beta, v)
      return v
      
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
    bestScore = float('-inf')
    bestAction = Directions.STOP
    for action in gameState.getLegalActions():
      if action == Directions.STOP:
        continue
      score = self.expectiMax(gameState.generateSuccessor(0, action), 1, 1)
      if bestScore < score:
        bestScore = score
        bestAction = action
    return bestAction

  def expectiMax(self, gameState, depth, agentIndex):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    agentNum = gameState.getNumAgents()
    if agentIndex == 0 or agentIndex >= agentNum: #PACMAN
      return max([self.expectiMax(gameState.generateSuccessor(0, action), depth + 1, 1) for action in gameState.getLegalActions(0) if action != Directions.STOP])
    else:
      if agentIndex == agentNum - 1 and depth == self.depth: #The Last GHOST
        scoreList = [self.evaluationFunction(gameState.generateSuccessor(agentIndex, action)) for action in gameState.getLegalActions(agentIndex)]
      else:  #Other GHOST
        scoreList = [self.expectiMax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1) for action in gameState.getLegalActions(agentIndex)] 
      return sum(scoreList)/len(scoreList)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  # Score = currentGameste.getScore() + foodScore + ghostScore

  if currentGameState.isWin() or currentGameState.isLose():
    return currentGameState.getScore()

  pacmanPos = currentGameState.getPacmanPosition()
  food = currentGameState.getFood()
  ghostStates = currentGameState.getGhostStates()
  ghostDistance = [ manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in ghostStates if ghost.scaredTimer == 0]
  minFoodDistance = min([ manhattanDistance(pacmanPos, (x,y)) for x in range(0, food.width) for y in range(0,food.height) if food[x][y] ])

  if ghostDistance and min(ghostDistance) == 0:
    return currentGameState.getScore()
    
  foodScore = 1.0 / minFoodDistance + 3.0 / food.count() 

  horribleGhosts = [ ghost for ghost in ghostStates if ghost.scaredTimer == 0 ]
  scaredGhosts = [ ghost for ghost in ghostStates if ghost.scaredTimer > 0 ] 

  #ghostScore = horribleGhostScore + scaredGhostScore
  ghostScore = 0.0
  if horribleGhosts:
    minHorribleGhostDist = float("inf")
    for ghost in horribleGhosts:
      if minHorribleGhostDist > manhattanDistance(pacmanPos, ghost.getPosition()):
        minHorribleGhostDist = manhattanDistance(pacmanPos, ghost.getPosition())
        nearestHorribleGhost = ghost
    if minHorribleGhostDist <= 6:  #Only the near ghost can hurt pacman!
        ghostScore -= 0.5 / minHorribleGhostDist
    
  if scaredGhosts:
    minScaredGhostDist = float("inf")
    for ghost in scaredGhosts:
      if minScaredGhostDist > manhattanDistance(pacmanPos, ghost.getPosition()):
        minScaredGhostDist = manhattanDistance(pacmanPos, ghost.getPosition())
        nearestScaredGhost = ghost
    if minScaredGhostDist < nearestScaredGhost.scaredTimer * 0.4:
      ghostScore += 3.0 / minScaredGhostDist
    elif minScaredGhostDist < nearestScaredGhost.scaredTimer * 0.6:
      ghostScore += 3.0 / minScaredGhostDist
    elif minScaredGhostDist < nearestScaredGhost.scaredTimer * 0.8:
      ghostScore += 3.0 / minScaredGhostDist
  score = currentGameState.getScore() + foodScore + ghostScore 
  return score
  
  # Abbreviation
better = betterEvaluationFunction
  

