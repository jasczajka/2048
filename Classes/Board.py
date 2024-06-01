"""
A class that represents a board in a game of 2048 with custom size and goal.
"""
import copy
from enum import Enum
import random
from Classes.exceptions import *


class Direction(Enum):
    """
    Enum class that represents move directions
    """
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Board:
    def __init__(self, size: int, goal: int):
        """
        Initializes an instance of a board with the given size and goal

        Parameters:
            size (int): The size of the board
            goal (int): The goal as in the tile that player aims to achieve
        Returns:
            None
        Raises:
            WrongBoardSizeError: if the size is not an integer or is lower than 2
            WrongGoalError: if the goal is not an integer or is less than 8 or more than 16384 or is not a power of 2
        """
        if not isinstance(goal, int):
            raise WrongBoardSizeError('board size must be an integer')
        self.size = size
        if self.size < 2:
            raise WrongBoardSizeError('board size must be greater than 2')
        if not isinstance(goal, int):
            raise WrongGoalError('goal must an integer')
        self.goal = goal
        if self.goal.bit_count() != 1 or self.goal <= 8 or self.goal > 16384:
            raise WrongGoalError('goal must be power of 2 greater than 8 and smaller or equal to 16384')
        self.goal = goal
        self.size = size
        self.tiles = [[0 for _ in range(self.size)] for _ in range(self.size)]
        #2 tiles at beginning
        self.generate_new_tile()
        self.generate_new_tile()

    def print_board(self):
        """
        Prints the current state of the board on the console
        Returns:
            None
        """
        print('score: ', self.get_score_on_board())
        print('goal: ', self.goal)
        for row in self.tiles:
            print('[',end="")
            for tile in row:
                print(f'{tile:{5}} ', end="")
            print(']')
        print('max tile: ', self.find_max_tile())
        if self.is_goal_reached():
            print('goal reached!!')
        print('=='*self.size)

    def is_goal_reached(self) -> bool:
        """
        Checks if the goal set by the player is rached
        Returns:
            bool: True if the goal is reached, False otherwise
        """

        if self.find_max_tile() >= self.goal:
            return True
        return False

    def get_2_or_4(self) -> int:
        """
        Returns either 2 with probability of 70% or 4 with probability of 30%
        Returns:
            int: 2 or 4
        """
        prob = random.uniform(0, 1)
        if prob < 0.7:
            return 2
        else:
            return 4

    def find_max_tile(self) -> int:
        """
        Finds the maximum tile currently on the board
        Returns:
            int: the maximum tile
        """
        return max(max(row) for row in self.tiles)

    def is_there_empty_tile(self) -> bool:
        """
        Checks if there is an empty tile in the board
        Returns:
            bool: True if there is a tile, False otherwise
        """
        for row in self.tiles:
            if 0 in row:
                return True
        return False

    def is_there_move_possible(self) -> bool:
        """
        Checks if there is a possible move on the board, first checking if there is an empty tile, then if there are 2 neigbhors with possibility to merge
        Returns:
            bool: True if there is a possible move, False otherwise
        """
        if self.is_there_empty_tile():
            return True
        for i in range(self.size):
            for j in range(self.size):
                if i < self.size - 1 and self.tiles[i][j] == self.tiles[i+1][j]:
                    return True
                if j < self.size - 1 and self.tiles[i][j] == self.tiles[i][j+1]:
                    return True
        return False

    def get_random_empty_tile(self) -> (int, int):
        """
        Gets coordinates of a random empty tile on the board
        Returns:
            (int, int): coordinates of the empty tile
        """
        empty_tiles = [(x, y) for x in range(0, self.size) for y in range(0, self.size) if self.tiles[x][y] == 0]
        if len(empty_tiles) != 0:
            return random.choice(empty_tiles)

    def generate_new_tile(self):
        """
        Generates a new 2/4 tile on the board in an empty spot
        Returns:
            None
        """
        (x, y) = self.get_random_empty_tile()
        self.tiles[x][y] = self.get_2_or_4()
        #print(f"new {self.tiles[x][y]} tile at {x+1}, {y+1}")

    def get_score_on_board(self) -> int:
        """
        Gets the sum of the tiles on the board as the score
        Returns:
            int: sum of the tiles on the board
        """
        return sum([sum(row) for row in self.tiles])

    def get_empty_tile_count(self) -> int:
        """
        Gets the number of empty tiles on the board
        Returns:
            int: number of empty tiles on the board
        """
        return len([(x, y) for x in range(0, self.size) for y in range(0, self.size) if self.tiles[x][y] == 0])

    def get_direction_with_highest_empty_tiles(self) -> Direction:
        """
        Gets the direction of the move with the highest empty tiles on the board after the move would be made
        Only considers valid moves
        Returns:
            Direction: Direction of the move with the highest empty tile count
        """
        directions = {Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT}
        potential_directions_empties = {}
        for direction in directions:
            board_copy = copy.deepcopy(self)
            if board_copy.make_move(direction):
                potential_directions_empties[direction] = board_copy.get_empty_tile_count()
        return max(potential_directions_empties, key=potential_directions_empties.get)

    def make_move(self, direction: Direction) -> bool:
        """
        Makes a move is the given direction
        If the move is invalid, no tiles were merged, or shifted in any direction, it means the move was not made and False is returned
        Parameters:
            Direction: Direction of the move to be made
        Returns:
            bool: True if the move was valid and made, False otherwise
        """
        move_made = False
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
                        #if something changed, then a move was made
                        if self.tiles[j][i] != tmp:
                            move_made = True
                        put_index += 1
                        j += 1
                    #if its a zero just go up
                    elif self.tiles[j][i] == 0:
                        j += 1
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
                        move_made = True
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
                        if self.tiles[j][i] != tmp:
                            move_made = True
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
                        move_made = True
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
                        if self.tiles[i][j] != tmp:
                            move_made = True
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
                        move_made = True
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
                        if self.tiles[i][j] != tmp:
                            move_made = True
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
                        move_made = True
                    j -= 1
        return move_made
