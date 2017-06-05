# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 14:12:08 2017

@author: csto935
"""

from BaseAI_3 import BaseAI
from heapq import heappush, heappop
from random import randint
import time
import math

explored = set()

class PlayerAI(BaseAI):
    
    def getMove(self, grid):
        
        
        initialState = State(None, grid, 0, -1)
        start = time.clock()
        best = self.decision(initialState, start)
        print(best)
        return best.move
    
    def decision(self, state, start):
        A = -math.inf
        B = math.inf
        

        best = self.maximize(state, A, B, start)
        
        return best[0]
            
            
        
    def maximize(self, state, A, B, start):
        
        diff = time.clock() - start
        
        if diff > 0.17 or len(state.grid.getAvailableMoves()) <= 0:
            print(len(state.grid.getAvailableMoves()))
            return self.evall(state)
        
        else:
           
            state.calculateChildren("MAX")
            
            maxChild = None
            maxUtility = -math.inf
             
            for c in reversed(state.childs):
                currentState = c[1]
                minTuple = self.minimize(currentState, A, B, start)
                 
                if minTuple[1] > maxUtility:
                    maxChild = currentState
                    maxUtility = minTuple[1]
                if maxUtility >= B:
                    break
                if maxUtility > A:
                     
                    A = maxUtility
            
            
            return (maxChild, maxUtility)
        
    def minimize(self, state, A, B, start):
        
        diff = time.clock() - start
        
        if diff > 0.17 or len(state.grid.getAvailableCells()) <= 0:
            print(len(state.grid.getAvailableCells()))
            return self.evall(state)
        
        else:
            state.calculateChildren("MIN")
            
            minChild = None
            minUtility = math.inf
             
            for c in state.childs:
                currentState = c[1]
                maxTuple = self.maximize(currentState, A, B, start)
                 
                if maxTuple[1] < minUtility:
                    minChild = currentState
                    minUtility = maxTuple[1]
                if minUtility <= A:
                     
#                    print("prouning")
                    break
                if minUtility < B:
                     
                    B = minUtility
                
            
            return (minChild, minUtility)
        
    def evall(self, state):
     
        return (state, state.mark)

class State(object):
    
    mark = -1
    
    def __init__(self, parentNode, grid, depth, move):
        self.parentNode = parentNode
        self.grid = grid
        self.depth = depth
        self.move = move
        self.childs = []
        
    def __lt__(self, other):
        
        if self.mark < other.mark:
            return self.mark < other.mark
        else:
            if self.move == 0:  
                return self
            elif other.move == 0:
                return other
            elif self.move == 1 and (other.move == 2 or other.move == 3):
                return self
            elif self.move == 2 and other.move == 3:
                return self
        
    def calculateChildren(self, turn):
        
        if turn == "MAX":
            listt = []
            moves = self.grid.getAvailableMoves()
            for m in moves:
                newGrid = self.grid.clone()
                newGrid.move(m)
                
                if str(newGrid.map) not in explored:
                    mark = len(newGrid.getAvailableCells())
                    newState = State(self, newGrid, self.depth + 1, m)
                    newState.mark = mark
                    listt.append(newState)
                    explored.add(str(newGrid.map))
            for l in listt:
                heappush(self.childs,(l.mark, l))
                
                
        else:
            listt = []
            cells = self.grid.getAvailableCells()
            
            for i in range(len(cells)):
                move = cells[randint(0, len(cells) - 1)] 
                newGrid = self.grid.clone()
                newGrid.setCellValue(move, self.getNewTileValue())
                if str(newGrid.map) not in explored:
                    newState = State(self, newGrid, self.depth + 1, -1)
                    mark = len(newGrid.getAvailableCells())
                    newState.mark = mark
                    listt.append(newState)
                    explored.add(str(newGrid.map))
            for l in listt:
                heappush(self.childs,(l.mark, l))
             
    def getNewTileValue(self):
        if randint(0,99) < 100 * 0.9:
            return 2
        else:
            return 4
                
                
                
                
                
                
                
                
                
                
                
                