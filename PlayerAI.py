import numpy as np
import random
import time
import sys
import os
from BaseAI import BaseAI
from Grid import Grid
import sys
import os

# setting path to parent directory
sys.path.append(os.getcwd())


# TO BE IMPLEMENTED
# 
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None

    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid: Grid) -> tuple:
        new_grid = self.move_decision(grid)
        new_position = new_grid.find(self.player_num)
        return new_position

    def move_min(self, grid: Grid, depth, alpha, beta):
        if self.is_terminal(grid) or depth > 5:
            return None, self.move_evaluate(grid)
        min_utility = 1000
        min_child = None
        children = grid.get_neighbors(grid.find(self.player_num), only_available=True)
        for i in children:
            child_grid = grid.clone()
            child_grid.trap(i)
            child_utility = self.move_max(child_grid, depth+1, alpha, beta)[1]
            if child_utility < min_utility:
                min_child = child_grid
                min_utility = child_utility
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility
        return min_child, min_utility

    def move_max(self, grid: Grid, depth, alpha, beta):
        if self.is_terminal(grid) or depth > 5:
            return None, self.move_evaluate(grid)
        max_utility = -1000
        max_child = None
        children = grid.get_neighbors(grid.find(self.player_num), only_available=True)
        for i in children:
            child_grid = grid.clone()
            child_grid.move(i, self.player_num)
            child_utility = self.move_min(child_grid, depth+1, alpha, beta)[1]
            if child_utility > max_utility:
                max_child = child_grid
                max_utility = child_utility
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility
        return max_child, max_utility

    def move_decision(self, grid: Grid):
        alpha = -1000000
        beta = 1000000
        child, utility = self.move_max(grid, 0, alpha, beta)
        return child

    def move_evaluate(self, grid: Grid):
        opponent_number = 3 - self.player_num
        opponent_pos = grid.find(opponent_number)
        opponent_neighbours = grid.get_neighbors(opponent_pos, only_available=True)
        own_neighbours = grid.get_neighbors(grid.find(self.player_num), only_available=True)

        bigger_neighbours = set(own_neighbours)
        for i in own_neighbours:
            i_neighbours = grid.get_neighbors(i, only_available=True)
            for j in i_neighbours:
                bigger_neighbours.add(j)

        score = len(bigger_neighbours)

        return score

    def trap_evaluate(self, grid: Grid):

        return 0

    def is_terminal(self, grid: Grid):
        opponent_number = 3 - self.player_num
        opponent_pos = grid.find(opponent_number)
        opponent_neighbours = grid.get_neighbors(opponent_pos, only_available=True)
        own_neighbours = grid.get_neighbors(self.pos, only_available=True)
        if len(opponent_neighbours) == 0 or len(own_neighbours) == 0:
            return True
        else:
            return False

    def getTrap(self, grid: Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions, 
        taking into account the probabilities of it landing in the positions you want. 
        
        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """

        # find opponent
        opponent = grid.find(3 - self.player_num)

        # find all available cells surrounding Opponent
        available_cells = grid.get_neighbors(opponent, only_available=True)

        # throw to one of the available cells randomly
        trap = random.choice(available_cells)

        return trap


