# -*- coding: utf-8 -*-
"""
Created on Mon May 29 12:08:18 2017

@author: csto935
"""

from BaseAI_3 import BaseAI
from random   import randint
from heapq import heappush, heappop
import time
import math



class PlayerAI(BaseAI):
    def getMove(self, grid):
        
#        start = time.clock()
        print()
        initialState = State(None, grid, 0, -1)

        initialState.calculateChilds("MIN")
#        bestChild = self.decision(initialState, start)
        
        
        return 0
    
    def decision(self, state, start):
        A = -math.inf
        B = math.inf
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
        maxUtility = -math.inf
        
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
        minUtility = math.inf
        
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
    childs = ()
    mark = -1
    
    def __init__(self, parent, grid, depth, move):
       
        self.parent = parent
        self.grid = grid
        self.depth = depth
        self.move = move

        
#    def __str__(self):
#        return "State: " + str(self.depth) + ", " + str(self.childs)
    
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
            
            listt = []
            for m in moves:

                newGrid = self.grid.clone()    
                newGrid.move(m)
                mark = len(newGrid.getAvailableCells()) * 0.3 + newGrid.getMaxTile() * 0.7
                newState = State(self, newGrid, self.depth + 1, m)
                newState.mark = mark
                listt.append(newState)

            listt.sort(key = lambda x: x.mark, reverse = True)
            self.childs = tuple(listt)
            
        else:  #MIN Turn
            
            emptyCells = self.grid.getAvailableCells()
            listt = []
            for i in range(len(emptyCells)):
                
                move = emptyCells[randint(0, len(emptyCells) - 1)]
                
                newGrid_2 = self.grid.clone()
                newGrid_2.setCellValue(move, 2)
                mark = len(newGrid_2.getAvailableCells()) * 0.3 + newGrid_2.getMaxTile() * 0.7
                newState_2 = State(self, newGrid_2, self.depth + 1, -1)
                newState_2.mark = mark
                
                newGrid_4 = self.grid.clone()
                newGrid_4.setCellValue(move, 4)
                mark = len(newGrid_4.getAvailableCells()) * 0.3 + newGrid_4.getMaxTile() * 0.7
                newState_4 = State(self, newGrid_4, self.depth + 1, -1)
                newState_4.mark = mark
                
                listt.append(newState_2)
                listt.append(newState_4)
                
            listt.sort(key = lambda x: x.mark)
            self.childs = tuple(listt)
#            for c in self.childs:  
#                g = c.grid
#                print(g.map)
            
            
    def getRandomTileValue(self):
        if randint(0,99) < 100 * 0.9:
            return 2
        else:
            return 4            
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    