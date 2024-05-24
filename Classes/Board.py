from enum import Enum
import random
from Classes.exceptions import WrongBoardSizeError
class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Board:
    def __init__(self, size :int):
        try:
            self.size = int(size)
        except ValueError:
            raise WrongBoardSizeError
        if size < 2:
            raise WrongBoardSizeError
        self.size = size
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
    def print_board(self):
        for row in self.board:
            print(row)
        print('='*self.size)
    def get_2_or_4(self) -> int:
        prob = random.uniform(0,1)
        if prob < 0.7:
            return 2
        else:
            return 4
    def is_there_empty_tile(self) -> bool:
        for row in self.board:
            if 0 in row:
                return True
        return False
    def is_there_move_possible(self) -> bool:
        if self.is_there_empty_tile():
            return True
        for i in range(self.size):
            for j in range(self.size):
                if i < self.size - 1 and self.board[i][j] == self.board[i+1][j]:
                    return True
                if j < self.size - 1 and self.board[i][j] == self.board[i][j+1]:
                    return True
        return False

    def get_random_empty_tile(self)->(int,int):
        empty_tiles = [(x,y) for x in range(0, self.size) for y in range(0, self.size) if self.board[x][y] == 0]
        return random.choice(empty_tiles)
    def generate_new_tile(self):
        (x,y) = self.get_random_empty_tile()
        self.board[x][y] = self.get_2_or_4()
        print(f"new {self.board[x][y]} tile at {x+1}, {y+1}")
    @staticmethod
    def get_score_on_board(board):
        return sum([sum(row) for row in board])
    def make_move(self, direction: Direction):
        if direction == Direction.UP:
            #shift up first
            for i in range(0,self.size):
                put_index = 0
                j = 0
                while j < self.size :
                    #if its a number, put it in put_index
                    if self.board[j][i] != 0:
                        tmp = self.board[j][i]
                        self.board[j][i] = self.board[put_index][i]
                        self.board[put_index][i] = tmp
                        put_index += 1
                        j+=1
                    #if its a zero just go up
                    elif self.board[j][i] == 0:
                        j+=1
            #merge then
            #for each column
            for i in range(0,self.size):
                 # start at 1, no point in comparing from 0
                j = 1
                while j < self.size:
                    if self.board[j][i] == self.board[j-1][i] and self.board[j][i] != 0:
                        self.board[j-1][i] *= 2
                        # here shift the rest up
                        k = j
                        while k < self.size:
                            if k == self.size-1:
                                #if its the last one, take zero
                                self.board[k][i] = 0
                            else:
                                self.board[k][i] = self.board[k+1][i]
                            k += 1
                        #if a jump was made, jump over
                    j += 1


        elif direction == Direction.DOWN:
            for i in range(0,self.size):
                put_index = self.size - 1
                j = self.size - 1
                while j >= 0 :
                    #if its a number, put it in put_index
                    if self.board[j][i] != 0:
                        tmp = self.board[j][i]
                        self.board[j][i] = self.board[put_index][i]
                        self.board[put_index][i] = tmp
                        put_index -= 1
                        j -= 1
                    #if its a zero just go down
                    elif self.board[j][i] == 0:
                        j -= 1
            #merge then
            #for each column
            for i in range(0,self.size):
                 # start at last - 1, no point in comparing from last
                j = self.size - 2
                while j >= 0:
                    if self.board[j][i] == self.board[j+1][i] and self.board[j][i] != 0:
                        self.board[j+1][i] *= 2
                        # here shift the rest down
                        k = j
                        while k >= 0:
                            if k == 0:
                                #if its the last one, take zero
                                self.board[k][i] = 0
                            else:
                                self.board[k][i] = self.board[k-1][i]
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
                    if self.board[i][j] != 0:
                        tmp = self.board[i][j]
                        self.board[i][j] = self.board[i][put_index]
                        self.board[i][put_index] = tmp
                        put_index += 1
                        j += 1
                    # if its a zero just go up
                    elif self.board[i][j] == 0:
                        j += 1
                #merge then
                #for each row
            for i in range(0, self.size):
                # start at 1, no point in comparing from 0
                j = 1
                while j < self.size:
                    if self.board[i][j] == self.board[i][j-1] and self.board[i][j] != 0:
                        self.board[i][j - 1] *= 2
                        # here shift the rest up
                        k = j
                        while k < self.size:
                            if k == self.size - 1:
                                # if its the last one, take zero
                                self.board[i][k] = 0
                            else:
                                self.board[i][k] = self.board[i][k + 1]
                            k += 1
                        # if a jump was made, jump over
                    j += 1

        elif direction == Direction.RIGHT:
            for i in range(0,self.size):
                put_index = self.size - 1
                j = self.size - 1
                while j >= 0 :
                    #if its a number, put it in put_index
                    if self.board[i][j] != 0:
                        tmp = self.board[i][j]
                        self.board[i][j] = self.board[i][put_index]
                        self.board[i][put_index] = tmp
                        put_index -= 1
                        j -= 1
                    #if its a zero just go down
                    elif self.board[i][j] == 0:
                        j -= 1
            #merge then
            #for each row
            for i in range(0,self.size):
                 # start at last - 1, no point in comparing from last
                j = self.size - 2
                while j >= 0:
                    if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0:
                        self.board[i][j + 1] *= 2
                        # here shift the rest down
                        k = j
                        while k >= 0:
                            if k == 0:
                                #if its the last one, take zero
                                self.board[i][k] = 0
                            else:
                                self.board[i][k] = self.board[i][k - 1]
                            k -= 1
                        #if a merge was made, jump over
                    j -= 1