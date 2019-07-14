# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections
class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
      
      
       
        i = 0
        while i<iterations:
            states = self.mdp.getStates()
            temp_counter = util.Counter()
            l=0
            while l<len(states):
                maxv = float("-inf")
                k = 0
                all_actions = self.mdp.getPossibleActions(states[l])
                while k<len(all_actions):
                    qv = self.computeQValueFromValues(states[l], all_actions[k])
                    if qv > maxv:
                        maxv = qv
                    temp_counter[states[l]] = maxv
                    k+=1
                l+=1
            self.values = temp_counter
            
            i+=1
   
   
   
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"



        action_prob_pairs = self.mdp.getTransitionStatesAndProbs(state, action)
        arr = []
        for val in action_prob_pairs:
            arr.append(((self.mdp.getReward(state, action, val[0])) + self.discount * self.values[val[0]])*val[1])
        return sum(arr)
    
    
        
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
      
      
      
        all_actions = self.mdp.getPossibleActions(state)
        action_to_take = None
        maxv = float("-inf")
        all_vals = [self.computeQValueFromValues(state, all_actions[i]) for i in range(len(all_actions))]
        j = 0
        while j<len(all_actions):
            if all_vals[j] > maxv:
                action_to_take = all_actions[j]
                maxv = all_vals[j]
            j+=1
        
        return action_to_take
   
   
   
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
