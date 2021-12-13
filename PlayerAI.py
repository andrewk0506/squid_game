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
            #make opponent move
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
            #add our throw
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
        own_neighbours = grid.get_neighbors(grid.find(self.player_num), only_available=True)
        bigger_neighbours = set(own_neighbours)
        for i in own_neighbours:
            i_neighbours = grid.get_neighbors(i, only_available=True)
            for j in i_neighbours:
                bigger_neighbours.add(j)

        own = len(own_neighbours)/8
        bigger = len(bigger_neighbours)/24
        score = own + bigger

        return score

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
        new_grid = self.trap_decision(grid)
        new_position = new_grid.find(self.player_num)
        return new_position

    def trap_decision(self, grid: Grid):
        alpha = -1000000
        beta = 1000000
        child, utility = self.trap_max(grid, 0, alpha, beta)
        return child

    def trap_max(self, grid: Grid, depth, alpha, beta):
        if self.is_terminal(grid) or depth > 5:
            return None, self.trap_evaluate(grid)
        max_utility = -1000
        max_child = None
        mypos = grid.find(self.player_num)
        opponent = grid.find(3 - self.player_num)
        children = grid.get_neighbors(opponent, only_available=True)

        if not children:
            return random.choice(grid.getAvailableCells())

        children = grid.get_neighbors(opponent, only_available=True)
        for i in children:
            mandist = abs(mypos[0] - i[0]) + abs(mypos[1] + i[1])
            p = 1 - 0.05 * (mandist - 1)
            child_grid = grid.clone()
            #add our move
            child_grid.trap(i)
            child_utility = p * self.trap_min(child_grid, depth+1, alpha, beta)[1]
            if child_utility > max_utility:
                max_child = child_grid
                max_utility = child_utility
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility
        return max_child, max_utility

    def trap_min(self, grid: Grid, depth, alpha, beta):
        if self.is_terminal(grid) or depth > 5:
            return None, self.trap_evaluate(grid)

        min_utility = 1000
        min_child = None
        opposition = grid.find(3 - self.player_num)
        children = grid.get_neighbors(opposition, only_available=True)
        for i in children:
            child_grid = grid.clone()
            child_grid.move(i, opposition)
            child_utility = self.trap_max(child_grid, depth + 1, alpha, beta)[1]
            if child_utility < min_utility:
                min_child = child_grid
                min_utility = child_utility
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility
        return min_child, min_utility

    def trap_evaluate(self, grid: Grid):
        opponent_number = 3 - self.player_num
        opponent_pos = grid.find(opponent_number)
        opponent_neighbours = grid.get_neighbors(opponent_pos, only_available=True)
        bigger_neighbours = set(opponent_neighbours)
        for i in opponent_neighbours:
            i_neighbours = grid.get_neighbors(i, only_available=True)
            for j in i_neighbours:
                bigger_neighbours.add(j)

        opponent = len(opponent_neighbours) / 8
        bigger = len(bigger_neighbours) / 24
        score = -(opponent + bigger)

        return score