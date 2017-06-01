# -*- coding: utf-8 -*-
"""
Created on Mon May 29 12:08:18 2017

@author: csto935
"""

from BaseAI_3 import BaseAI
from random   import randint
import time
import math
from heapq import heappush, heappop



#create explored Set
explored = set()

class PlayerAI(BaseAI):
    def getMove(self, grid):
        
        start = time.clock()
       
        initialState = State(None, grid, 0, -1)
        

        initialState.calculateChilds("MIN")
#        initialState.childs[0].calculateChilds("MIN")
#        print("time: " + str(time.clock() - start))
#       
#        print()
#        bestChild = self.decision(initialState, start)

        return 0
    
    def decision(self, state, start):
        A = -math.inf
        B = math.inf
        decisionT = self.maximize(state, A, B, start)
        print("time: " + str(time.clock() - start))
        print()
        return decisionT[0]
        
    def maximize(self, state, A, B, start):
        
        
        moves = []
        moves = state.grid.getAvailableMoves()

        diff = time.clock() - start

        if diff >= 0.1 or len(moves) <= 0: #Terminal state
            return self.evall(state)
        
        maxChild = None
        maxUtility = -math.inf

        state.calculateChilds("MAX")
       
        for c in state.childs:
            
            currentState = c
            
            t = self.minimize(currentState, A, B, start)
            
            if t[1] > maxUtility:
                maxChild = currentState
                maxUtility = t[1]
                if maxUtility >= B:
                    print("prouning")
                    break
                if maxUtility > A:
                    A = maxUtility
#            if str(c.grid.map) not in explored:
#                explored.add(str(c.grid.map))
#                currentState = c
#            
#                t = self.minimize(currentState, A, B, start)
#            
#                if t[1] > maxUtility:
#                    maxChild = currentState
#                    maxUtility = t[1]
#                    if maxUtility >= B:
#                        print("prouning")
#                        break
#                    if maxUtility > A:
#                        A = maxUtility
        
        finalT = (maxChild, maxUtility)
        return finalT
        
    def minimize(self, state, A, B, start):
       
        emptyCells = []
        emptyCells = state.grid.getAvailableCells()

        diff = time.clock() - start

        if diff >= 0.1 or len(emptyCells) <= 0: #Terminal State
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
                   print("prouning")
                   break
               if minUtility < B:
                   B = minUtility
#            if str(c.grid.map) not in explored:
#                explored.add(str(c.grid.map))
#                t = self.maximize(c, A, B,start)
#            
#                if t[1] < minUtility:
#                    minChild = c
#                    minUtility = t[1]
#                    if minUtility <= A:
#                        print("prouning")
#                        break
#                    if minUtility < B:
#                        B = minUtility
        
        finalT = (minChild, minUtility)
        return finalT
            

    def evall(self, state):
        mark = len(state.grid.getAvailableCells()) 
        return (None, mark)
    
  
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
    
#    def __eq__(self, othr):
#        return self.grid == othr.grid
#
#    def __hash__(self):
#        return hash((self.grid))
#    
#    def __lt__(self, other):
#        
#        if self.mark < other.mark:
#            return self.mark < other.mark
        
    def calculateChilds(self, turn):
        
        if turn == "MAX":   #MAX Turn
            moves = self.grid.getAvailableMoves()
            
            listt = []
            for m in moves:

                newGrid = self.grid.clone()    
                newGrid.move(m)
                mark = len(newGrid.getAvailableCells()) 
                newState = State(self, newGrid, self.depth + 1, m)
                newState.mark = mark
#                print("max depth: " + str(newState.depth))
                listt.append(newState)

            listt.sort(key = lambda x: x.mark, reverse = True)
            self.childs = tuple(listt)
#             for s in listt:
#                 heappush(self.childs, (s.mark, s))
            
        else:  #MIN Turn
            
            emptyCells = self.grid.getAvailableCells()
            listt = []
            for i in range(len(emptyCells)):
                
                move = emptyCells[randint(0, len(emptyCells) - 1)]
                
                newGrid = self.grid.clone()
                newGrid.setCellValue(move, self.getRandomTileValue())
                if str(newGrid.map) not in explored:
                    mark = len(newGrid.getAvailableCells()) 
                    newState_2 = State(self, newGrid, self.depth + 1, -1)
                    newState_2.mark = mark
#                print("min depth: " + str(newState_2.depth))
                    listt.append(newState_2)
                    explored.add(str(newGrid.map))
                else:
                    print("present")



#                newGrid_2 = self.grid.clone()
#                newGrid_2.setCellValue(move, 2)
#                mark = len(newGrid_2.getAvailableCells()) 
#                newState_2 = State(self, newGrid_2, self.depth + 1, -1)
#                newState_2.mark = mark
##                print("min depth: " + str(newState_2.depth))
#                listt.append(newState_2)
# 
#                newGrid_4 = self.grid.clone()
#                newGrid_4.setCellValue(move, 4)
#                mark = len(newGrid_2.getAvailableCells()) 
#                newState_4 = State(self, newGrid_4, self.depth + 1, -1)
#                newState_4.mark = mark
##                print("min depth: " + str(newState_4.depth))
#                listt.append(newState_4)
    
            listt.sort(key = lambda x: x.mark)
            self.childs = tuple(listt)
            print("explored size: " + str(len(explored)))

            
            
    def getRandomTileValue(self):
        if randint(0,99) < 100 * 0.9:
            return 2
        else:
            return 4            
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    