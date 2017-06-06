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
        
        explored.clear()
        initialState = State(None, grid, 0, -1)
        start = time.clock()
        best = self.decision(initialState, start)
#        initialState.calculateChildren("MIN")
        
        
        return best.move
    
    def decision(self, state, start):
        A = -math.inf
        B = math.inf
        

        best = self.maximize(state, A, B, start)
        
        return best[0]
            
            
        
    def maximize(self, state, A, B, start):
        
        diff = time.clock() - start
        
        if diff > 0.17 or len(state.grid.getAvailableMoves()) <= 0:
            
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
            originalAvailableCells = len(self.grid.getAvailableCells())
            for m in moves:
                newGrid = self.grid.clone()
                newGrid.move(m)
                if str(newGrid.map) not in explored:
                    newAvailableCells = len(newGrid.getAvailableCells()) 
                    mark = self.monotonic(newGrid) * 0.6 + self.smoothnessMax(originalAvailableCells, newAvailableCells) * 0.4  
                    newState = State(self, newGrid, self.depth + 1, m)
                    newState.mark = mark
                    listt.append(newState)
                    explored.add(str(newGrid.map))
            for l in listt:
                heappush(self.childs,(l.mark, l))
                
                
        else:  #MIN Turn
            listt = []
            cells = self.grid.getAvailableCells()
            
            for i in range(len(cells)):
                move = cells[randint(0, len(cells) - 1)] 
                newGrid = self.grid.clone()
                newGrid.setCellValue(move, self.getNewTileValue())
                if str(newGrid.map) not in explored:
                    newState = State(self, newGrid, self.depth + 1, -1)
                    mark = self.monotonic(newGrid) * 0.6 + self.smoothnessMin(newGrid) * 0.4
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
        
    def monotonic(self, grid):
        
        countRow = [0,0,0,0]
      
        for i in range(grid.size):
            crescente = -1
            for j in range(grid.size):
                if grid.map [i][j] >= crescente:
                    crescente = grid.map [i][j]
                    countRow[i] += 1
                else:
                    break
        
        countColumn = [0,0,0,0]
        for j in range(grid.size):
            crescente = math.inf
            for i in range(grid.size):
                if grid.map [i][j] <= crescente:
                    crescente = grid.map [i][j]
                    countColumn[j] += 1
                else:
                    break
        monotonicMark = 0
        for i in range(len(countRow)):
            if countRow[i] == 4:
                monotonicMark += 1
            if countColumn[i] == 4:
                monotonicMark += 1
        
        return monotonicMark
    
    def smoothnessMax(self, originalAvailableCells, newAvailableCells):
        
        diff = 0
        diff = abs(originalAvailableCells - newAvailableCells)
        return diff
    
    def smoothnessMin(self, grid):
        
        smooth = 0
        
        for i in range(grid.size):
            saved = -1
            for j in range(grid.size):
                if grid.map[i][j] != 0:
                    if grid.map[i][j] != saved:
                        saved = grid.map[i][j]
                    else:
                        smooth += 1
                        saved = -1
        
                     
        for j in range(grid.size):
            saved = -1
            for i in range(grid.size):
                if grid.map [i][j] != 0:
                    if grid.map[i][j] != saved:
                        saved = grid.map[i][j]
                    else:
                        smooth += 1
                        saved = -1
        
        return smooth
             
                
                
                
                
                
                
                
                
                
                
                