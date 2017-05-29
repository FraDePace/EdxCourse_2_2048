# -*- coding: utf-8 -*-
"""
Created on Mon May 29 12:08:18 2017

@author: csto935
"""

from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        print("moves: " + str(moves))
        return 1
    
    