# -*- coding: utf-8 -*-
"""
Created on Mon May 29 12:08:18 2017

@author: csto935
"""

from BaseAI_3 import BaseAI
from random   import randint
from heapq import heappush, heappop
import time



class PlayerAI(BaseAI):
    def getMove(self, grid):
        
        start = time.clock()
        initialState = State(None, grid, 0, -1)
        initialState.childs = []
#        print(initialState.childs)
        
        bestChild = self.decision(initialState, start)
        
        return bestChild.move
    
    def decision(self, state, start):
        A = -1000000
        B = 1000000
        decisionT = self.maximize(state, A, B, start)
        return decisionT[0]
        
    def maximize(self, state, A, B, start):
      
        moves = []
        moves = state.grid.getAvailableMoves()
        
        
        diff = time.clock() - start
       

        if diff >= 0.17 or len(moves) <= 0: #Terminal state
            print(diff)

            return self.evall(state)
        
        maxChild = None
        maxUtility = -1000000
        
#        print(time.clock())
#        print(start)
#        print("diff time: " + str(time.clock() - start))
        
        state.calculateChilds("MAX")
       
        for c in state.childs:

            currentState = c
            
            t = self.minimize(currentState, A, B, start)
            
            if t[1] > maxUtility:
                maxChild = currentState
                maxUtility = t[1]
            if maxUtility >= B:
                break
            if maxUtility > A:
                A = maxUtility
        
        finalT = (maxChild, maxUtility)
        return finalT
        
    def minimize(self, state, A, B, start):
       
        emptyCells = []
        emptyCells = state.grid.getAvailableCells()
        
      

        diff = time.clock() - start
        
        
        if diff >= 0.17 or len(emptyCells) <= 0: #Terminal State
#            print("Terminal")
            print(diff)
            return self.evall(state)
        
        minChild = None
        minUtility = 1000000
        
        state.calculateChilds("MIN")
        for c in state.childs:
           
            t = self.maximize(c, A, B,start)
            
            if t[1] < minUtility:
                minChild = c
                minUtility = t[1]
            if minUtility <= A:
                break
            if minUtility < B:
                B = minUtility
        
        finalT = (minChild, minUtility)
        return finalT
            

    def evall(self, state):
        maxT = state.grid.getMaxTile()
        return (None, maxT)
    
  
class State(object):
    
    parent = None
    move = -1
    childs = []
    mark = -1
    
    def __init__(self, parent, grid, depth, move):
        self.parent = parent
        self.grid = grid
        self.depth = depth
        self.move = move
        
        
        
    def __eq__(self, othr):
        return self.grid == othr.grid

    def __hash__(self):
        return hash((self.grid))
    
    def __lt__(self, other):
        
        if self.mark < other.mark:
            return self.mark < other.mark
        
    def calculateChilds(self, turn):
        
        if turn == "MAX":   #MAX Turn
            moves = self.grid.getAvailableMoves()

            for m in moves:
                newGrid = self.grid.clone()          
                newGrid.move(m)
                mark = len(newGrid.getAvailableCells()) 
                newState = State(self, newGrid, self.depth + 1, m)
                newState.mark = mark
                newState.childs = []
                self.childs.append(newState)
               

            self.childs.sort(key = lambda x: x.mark)
            
            
        else:  #MIN Turn
            
            emptyCells = self.grid.getAvailableCells()
            
            for i in range(len(emptyCells)):
                newGrid = self.grid.clone()
                
                move = emptyCells[randint(0, len(emptyCells) - 1)]
                newGrid.setCellValue(move, self.getRandomTileValue())
                newState = State(self, newGrid, self.depth + 1, -1)
                newState.childs = []
                self.childs.append(newState)
            
            
    def getRandomTileValue(self):
        if randint(0,99) < 100 * 0.9:
            return 2
        else:
            return 4            
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    