# -*- coding: utf-8 -*-
"""
Created on Mon May 29 12:08:18 2017

@author: csto935
"""

from BaseAI_3 import BaseAI
from random   import randint

class PlayerAI(BaseAI):
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        print("moves: " + str(moves))
        return 1
    
    def decision(self, state):
        A = -100
        B = 100
        child = self.maximize(state, A, B)
        return child
        
    def maximize(self, state, A, B):
        moves = state.getAvailableMoves()
        
        if len(moves) < 0: #Terminal state
            return self.evall(state)
        
        maxChild = None
        maxUtility = -100
        
        childs = []
        
        #get MAX childs
        for m in moves:
            stateCopy = state.clone()
            stateCopy.move(m)
            childs.append(stateCopy)
        
         
            
        
    def minimize(self, state, A, B):
        return 0
        
    def evall(self, state):
        return 0
    
    def getRandomTileValue(self):
        if randint(0,99) < 100 * self.probability:
            return 2
        else:
            return 4
    
    
    
    
    