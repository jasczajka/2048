import copy
from enum import Enum
import random
from Classes.exceptions import *


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Board:
    def __init__(self, size: int, goal: int):
        if not isinstance(goal, int):
            raise WrongBoardSizeError('board size must be an integer')
        self.size = size
        if self.size < 2:
            raise WrongBoardSizeError('board size must be greater than 2')
        if not isinstance(goal, int):
            raise WrongGoalError('goal must an integer')
        self.goal = goal
        if self.goal.bit_count() != 1 or self.goal <= 8:
            raise WrongGoalError('goal must be power of 2 greater than 8')
        self.goal = goal
        self.size = size
        self.tiles = [[0 for _ in range(self.size)] for _ in range(self.size)]
        #2 tiles at beginning
        self.generate_new_tile()
        self.generate_new_tile()

    def print_board(self):
        print('score: ', self.get_score_on_board(self))
        print('goal: ', self.goal)
        for row in self.tiles:
            print(row)
        print('max tile: ', self.find_max_tile())
        if self.is_goal_reached():
            print('goal reached!!')
        print('=='*self.size)
    def is_goal_reached(self) -> bool:
        if self.find_max_tile() >= self.goal:
            return True
        return False
    def get_2_or_4(self) -> int:
        prob = random.uniform(0, 1)
        if prob < 0.7:
            return 2
        else:
            return 4
    def find_max_tile(self):
        return max(max(row) for row in self.tiles)

    def is_there_empty_tile(self) -> bool:
        for row in self.tiles:
            if 0 in row:
                return True
        return False

    def is_there_move_possible(self) -> bool:
        if self.is_there_empty_tile():
            return True
        for i in range(self.size):
            for j in range(self.size):
                if i < self.size - 1 and self.tiles[i][j] == self.tiles[i+1][j]:
                    return True
                if j < self.size - 1 and self.tiles[i][j] == self.tiles[i][j+1]:
                    return True
        return False

    def get_random_empty_tile(self)->(int, int):
        empty_tiles = [(x, y) for x in range(0, self.size) for y in range(0, self.size) if self.tiles[x][y] == 0]
        if len(empty_tiles) != 0:
            return random.choice(empty_tiles)
    def generate_new_tile(self):
        (x, y) = self.get_random_empty_tile()
        self.tiles[x][y] = self.get_2_or_4()
        print(f"new {self.tiles[x][y]} tile at {x+1}, {y+1}")

    def get_score_on_board(self):
        return sum([sum(row) for row in self.tiles])

    def get_empty_tile_count(self) -> int:
        return len([(x, y) for x in range(0, self.size) for y in range(0, self.size) if self.tiles[x][y] == 0])
    def get_direction_with_highest_empty_tiles(self) -> Direction:
        potential_directions_empties = {Direction.UP: -1, Direction.DOWN: -1, Direction.LEFT: -1, Direction.RIGHT: -1}
        for direction in potential_directions_empties:
            board_copy = copy.deepcopy(self)
            board_copy.make_move(direction)
            potential_directions_empties[direction] = board_copy.get_empty_tile_count()
        return max(potential_directions_empties, key=potential_directions_empties.get)

    def make_move(self, direction: Direction):
        if direction == Direction.UP:
            #shift up first
            for i in range(0, self.size):
                put_index = 0
                j = 0
                while j < self.size:
                    #if its a number, put it in put_index
                    if self.tiles[j][i] != 0:
                        tmp = self.tiles[j][i]
                        self.tiles[j][i] = self.tiles[put_index][i]
                        self.tiles[put_index][i] = tmp
                        put_index += 1
                        j+=1
                    #if its a zero just go up
                    elif self.tiles[j][i] == 0:
                        j+=1
            #merge then
            #for each column
            for i in range(0, self.size):
                 # start at 1, no point in comparing from 0
                j = 1
                while j < self.size:
                    if self.tiles[j][i] == self.tiles[j-1][i] and self.tiles[j][i] != 0:
                        self.tiles[j-1][i] *= 2
                        # here shift the rest up
                        k = j
                        while k < self.size:
                            if k == self.size-1:
                                #if its the last one, take zero
                                self.tiles[k][i] = 0
                            else:
                                self.tiles[k][i] = self.tiles[k+1][i]
                            k += 1
                        #if a jump was made, jump over
                    j += 1
        elif direction == Direction.DOWN:
            for i in range(0, self.size):
                put_index = self.size - 1
                j = self.size - 1
                while j >= 0:
                    #if its a number, put it in put_index
                    if self.tiles[j][i] != 0:
                        tmp = self.tiles[j][i]
                        self.tiles[j][i] = self.tiles[put_index][i]
                        self.tiles[put_index][i] = tmp
                        put_index -= 1
                        j -= 1
                    #if its a zero just go down
                    elif self.tiles[j][i] == 0:
                        j -= 1
            #merge then
            #for each column
            for i in range(0, self.size):
                 # start at last - 1, no point in comparing from last
                j = self.size - 2
                while j >= 0:
                    if self.tiles[j][i] == self.tiles[j+1][i] and self.tiles[j][i] != 0:
                        self.tiles[j+1][i] *= 2
                        # here shift the rest down
                        k = j
                        while k >= 0:
                            if k == 0:
                                #if its the last one, take zero
                                self.tiles[k][i] = 0
                            else:
                                self.tiles[k][i] = self.tiles[k-1][i]
                            k -= 1
                        #if a merge was made, jump over
                    j -= 1

        elif direction == Direction.LEFT:
            # shift left first
            for i in range(0, self.size):
                put_index = 0
                j = 0
                while j < self.size:
                    # if its a number, put it in put_index
                    if self.tiles[i][j] != 0:
                        tmp = self.tiles[i][j]
                        self.tiles[i][j] = self.tiles[i][put_index]
                        self.tiles[i][put_index] = tmp
                        put_index += 1
                        j += 1
                    # if its a zero just go up
                    elif self.tiles[i][j] == 0:
                        j += 1
                #merge then
                #for each row
            for i in range(0, self.size):
                # start at 1, no point in comparing from 0
                j = 1
                while j < self.size:
                    if self.tiles[i][j] == self.tiles[i][j-1] and self.tiles[i][j] != 0:
                        self.tiles[i][j - 1] *= 2
                        # here shift the rest up
                        k = j
                        while k < self.size:
                            if k == self.size - 1:
                                # if its the last one, take zero
                                self.tiles[i][k] = 0
                            else:
                                self.tiles[i][k] = self.tiles[i][k + 1]
                            k += 1
                        # if a jump was made, jump over
                    j += 1

        elif direction == Direction.RIGHT:
            for i in range(0, self.size):
                put_index = self.size - 1
                j = self.size - 1
                while j >= 0:
                    #if its a number, put it in put_index
                    if self.tiles[i][j] != 0:
                        tmp = self.tiles[i][j]
                        self.tiles[i][j] = self.tiles[i][put_index]
                        self.tiles[i][put_index] = tmp
                        put_index -= 1
                        j -= 1
                    #if its a zero just go down
                    elif self.tiles[i][j] == 0:
                        j -= 1
            #merge then
            #for each row
            for i in range(0, self.size):
                 # start at last - 1, no point in comparing from last
                j = self.size - 2
                while j >= 0:
                    if self.tiles[i][j] == self.tiles[i][j + 1] and self.tiles[i][j] != 0:
                        self.tiles[i][j + 1] *= 2
                        # here shift the rest down
                        k = j
                        while k >= 0:
                            if k == 0:
                                #if its the last one, take zero
                                self.tiles[i][k] = 0
                            else:
                                self.tiles[i][k] = self.tiles[i][k - 1]
                            k -= 1
                        #if a merge was made, jump over
                    j -= 1
