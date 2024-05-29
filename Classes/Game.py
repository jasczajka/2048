from Classes.Board import *
import os.path
import time
import tkinter as tk


class Game:
    def __init__(self, size=4, goal=2048):
        self.board = Board(size, goal)

    def save_file(self, file_name=None) -> bool:
        if file_name is None:
            file_name = input('Enter save file name: ')
        file_path = f'Saves/{file_name}.txt'
        if os.path.isfile(file_path):
            print('such file save already exists, choose a different name')
            return False
        else:
            with open(file_path, 'w') as fSave:
                fSave.write(f'{self.board.size} {self.board.goal}\n')
                string_tiles = [' '.join([str(tile) for tile in row]) for row in self.board.tiles]
                fSave.write('\n'.join(string_tiles))
            print('file saved')
            return True

    def load_file(self, file_name = None) -> bool:
        if file_name is None:
            file_name = input('Enter save file name: ')
        file_path = f'Saves/{file_name}.txt'
        if not os.path.isfile(file_path):
            print('no such a save file')
            return False
        else:
            with open(file_path, 'r') as fSave:
                try:
                    game_info = fSave.readline().strip().split(' ')
                    self.board.size = int(game_info[0])
                    self.board.goal = int(game_info[1])
                    tiles = [[int(tile) for tile in row.split(' ')] for row in fSave.read().split('\n')]
                    self.board.tiles = tiles
                    return True
                except ValueError:
                    print('error loading save file')
                    return False

    def save_score(self, file_name = None) -> bool:
        if file_name is None:
            file_name = input('Enter score file name: ')
        file_path = f'Scores/{file_name}.txt'
        if os.path.isfile(file_path):
            print('such score name already exists, choose a different name')
            return False
        else:
            with open(file_path, 'w') as fSave:
                fSave.write(f'{file_name} {self.board.get_score_on_board(self.board)}')
                print('score saved')
                return True

    def get_leaderboard(self):
        score_dict = {}
        for file in os.listdir('Scores'):
            if file.endswith('.txt'):
                file_path = f'Scores/{file}'
                with open(file_path, 'r') as fScore:
                    score_line = fScore.readline().split(' ')
                    score_dict[score_line[0]] = int(score_line[1])
        return sorted(score_dict.items(), key=lambda item: item[1], reverse=True)

    def print_leaderboard(self):
        print(f'top scores:')
        leaderboard = self.get_leaderboard()
        for score in leaderboard:
            print(f'{score[0]} - scored {score[1]}')

    def play_game_computer(self):
        while self.board.is_there_move_possible():
            time.sleep(0.4)
            direction = self.board.get_direction_with_highest_empty_tiles()
            if self.board.make_move(direction):
                if self.board.is_there_empty_tile():
                    self.board.generate_new_tile()
                self.board.print_board()

    def play_console(self):
        valid_size_and_goal = False
        while not valid_size_and_goal:
            try:
                size = input("Enter size of the board: ")
                goal = input("Enter goal: ")
                if str.isdigit(size) and str.isdigit(goal):
                    self.board = Board(int(size), int(goal))
                    valid_size_and_goal = True
            except WrongGoalError as e:
                print(e)
            except WrongBoardSizeError as e:
                print(e)
        self.board.print_board()
        while True:
            self.board.print_board()
            move = input("Enter move (w/a/s/d for up/left/down/right or q to quit or save to save or load to load or score to save score or comp for computer game): ").strip().lower()
            if move == 'comp':
                self.play_game_computer()
            if move == 'q':
                print("Game over!")
                break
            elif move == 'leaderboard':
                self.print_leaderboard()
            elif move == 'save':
                self.save_file()
            elif move == 'load':
                self.load_file()
            elif move == 'score':
                self.save_score()
            elif move in ['w', 'a', 's', 'd']:
                direction = {'w': Direction.UP, 'a': Direction.LEFT, 's': Direction.DOWN, 'd': Direction.RIGHT}[
                    move]
                self.board.make_move(direction)
                print(self.board.get_direction_with_highest_empty_tiles())
                if self.board.is_there_empty_tile():
                    self.board.generate_new_tile()
                if not self.board.is_there_move_possible():
                    print("No more moves possible. Game over!")
                    self.board.print_board()
                    while True:
                        should_save_score = input("Do you want to save score? y for yes n for no: ").strip().lower()
                        if should_save_score == 'y':
                            while not self.save_score():
                                self.save_score()
                            break
                        elif should_save_score == 'n':
                            break
                        else:
                            print("invalid input")

                    break
            else:
                print("Invalid input. Use w/a/s/d for direction or q to quit.")
