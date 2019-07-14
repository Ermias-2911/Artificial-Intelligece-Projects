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
#
# Ermias Haile
# CSC 665
# Professor Pooyan Fazli
# October, 10 2018

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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"
     
        i = 0
        min_dist = []
        
    
        while (i<len(newGhostStates)):
    
    
            ghost_distance = abs( newPos[0] - newGhostStates[i].getPosition()[0] ) + abs( newPos[1] - newGhostStates[i].getPosition()[1] )
            min_dist.append(ghost_distance)
            i += 1
        min_ghost_dist = min(min_dist)
        t_score = sum(min_dist)
        if min_ghost_dist < 2:
            return min_ghost_dist


        foodList = currentGameState.getFood().asList()
        j = 0
        food_distances = []
        while j<len(foodList):
            f_dist = abs( newPos[0] - foodList[j][0] ) + abs( newPos[1] - foodList[j][1] ) 
            food_distances.append(f_dist)
            j+=1

        try:
            return 80.0 - min(food_distances)
        except:
            return t_score

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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        self.game_agents = gameState.getNumAgents()

        next_move = self.max_min_value(gameState, 0, 0,'max')

    
        return next_move[0][1]

    def max_min_value(self, state, agent, depth,max_min='max'):

        max_score = float('-inf')
        max_action = "South"

        min_score = float('inf')
        min_action = "South"

        i = 0
        depth = depth + 1
        all_actions = state.getLegalActions(agent)


        if(max_min=='max'):
            while i<(len(all_actions)):
               
                
                scucessor_states = state.generateSuccessor(agent, all_actions[i])
                score = self.compute_score(scucessor_states, depth % self.game_agents, depth)

                new_max_score = max([score,max_score])
                if new_max_score>max_score:
                    max_action = all_actions[i]
                max_score = new_max_score
                i+=1
            return [max_score, max_action],[0,'']    
        
 
        i = 0
        while i<len(all_actions):
            scucessor_states = state.generateSuccessor(agent, all_actions[i])

            score = self.compute_score(scucessor_states, depth % self.game_agents, depth)

            new_min_score = min([score,min_score])
            if new_min_score<min_score:
                min_action = all_actions[i]
            min_score = new_min_score
            i+=1
        return [0,''],[min_score, min_action]
    

    def compute_score(self, state, agent, depth):
        
        dga = self.depth*self.game_agents
        if depth>= dga:
            mp_result = True
        else:
            mp_result = False

        if (mp_result==True or state.isWin()==True or state.isLose()==True):
            return self.evaluationFunction(state)
        
        elif agent == 0:
            mx = self.max_min_value(state, agent, depth,'max')
            return mx[0][0]
        else:
            mn = self.max_min_value(state, agent, depth,'min')
            
            return mn[1][0]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        self.game_agents = gameState.getNumAgents()

        path = self.max_min_value(gameState, 0, 0, float('-inf'), float('inf'),max_min='max')
        return path[1]

    def max_min_value(self, state, agent, depth, alpha, beta,max_min='max'):
        
        
        all_actions = state.getLegalActions(agent)

        if max_min=='max':
            m_value = float('-inf')
            v_action = 'Stop'
            i = 0
            depth += 1
        
            while i<len(all_actions):

                
                succes_states = state.generateSuccessor(agent, all_actions[i])
                score = self.compute_score(succes_states, depth % self.game_agents, depth, alpha, beta)

                new_m = max([score,m_value])
                if new_m>m_value:
                    v_action = all_actions[i]
                m_value = new_m
                
                if m_value > beta:
                    return m_value, v_action
                alpha = max(alpha, m_value)
                i += 1
            return m_value, v_action


        m_value = float('inf')
        v_action = 'Stop'
        depth += 1

        i = 0        
        while i<len(all_actions):

            
            succes_states = state.generateSuccessor(agent, all_actions[i])
            score = self.compute_score(succes_states, depth % self.game_agents, depth, alpha, beta)

            new_m = min([score,m_value])
            if new_m<m_value:
                v_action = all_actions[i]
            m_value = new_m
            
            if m_value < alpha:
                return m_value, v_action
            beta = min(beta, m_value)
            i += 1
        return m_value, v_action

    
    def compute_score(self, state, agent, depth, alpha, beta):
       
        dga = self.depth * self.game_agents
         
        if depth >= dga: 
            mp_result = True
        else:
            mp_result = False
      
        if mp_result==True or state.isWin()==True or state.isLose()==True :
            return self.evaluationFunction(state)
        elif agent == 0:
            n_state = self.max_min_value(state, agent, depth, alpha, beta,'max')
            return n_state[0]
        else:
            n_state = self.max_min_value(state, agent, depth, alpha, beta,'min')
            return n_state[0]



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
        self.game_agents = gameState.getNumAgents()


        path = self.max_rand_value(gameState, 0, 0,'max')
        return path[1]

    def max_rand_value(self, state, agent, depth,max_rand='max'):
    
        if max_rand=='max':
            max_score = float('-inf')
            max_action = "Stop"

            depth = depth + 1
            all_actions = state.getLegalActions(agent)
            i = 0
            while i<(len(all_actions)):
             
                
                scucessor_states = state.generateSuccessor(agent, all_actions[i])
                score = self.compute_score(scucessor_states, depth % self.game_agents, depth)

                new_max_score = max([score,max_score])
                if new_max_score>max_score:
                    max_action = all_actions[i]
                max_score = new_max_score
                i+=1
            return max_score, max_action 

        all_actions = state.getLegalActions(agent)
        score_list = {}
        cur_score = 0
        i = 0
        depth = depth + 1
        while i<len(all_actions):
            ss = state.generateSuccessor(agent, all_actions[i])
            score_list[all_actions[i]] = self.compute_score(ss, depth % self.game_agents, depth)
            i += 1
        return sum(score_list.values()) / float(len(score_list.values())), ''

    def compute_score(self, state, agent, depth):
      
        dga = self.depth * self.game_agents
         
        if depth >= dga: 
            mp_result = True
        else:
            mp_result = False
      
        if mp_result==True or state.isWin()==True or state.isLose()==True :
            return self.evaluationFunction(state)
        elif agent == 0:
            n_state = self.max_rand_value(state, agent, depth,'max')
            return n_state[0]
        else:
            n_state = self.max_rand_value(state, agent, depth,'rand')
            return n_state[0]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    ghostStates = currentGameState.getGhostStates()

    total_score = 0.0
    c_ghosts = []
    j = 0
    while j<len(ghostStates):
        ghost_distance = abs( currentGameState.getPacmanPosition()[0] - ghostStates[j].getPosition()[0] ) + abs( currentGameState.getPacmanPosition()[1] - ghostStates[j].getPosition()[1] )
        if ghost_distance>0:
            c_ghosts.append(-1/ghost_distance)
        elif ghost_distance==0:
            c_ghosts.append(0)
        else:
            c_ghosts.append(-1/ghost_distance)
        j += 1
   
    ghost_score = min(c_ghosts)
    
    food_distances = []
    for food_pos in currentGameState.getFood().asList():
        f_dist = abs( currentGameState.getPacmanPosition()[0] - food_pos[0] ) + abs( currentGameState.getPacmanPosition()[1] - food_pos[1] )
        food_distances.append(-1*f_dist)
    
    
    try:
        fscore = max(food_distances)
    except:
        fscore = 1000
    total_score = fscore + ghost_score + currentGameState.getScore()

    return total_score

# Abbreviation
better = betterEvaluationFunction

