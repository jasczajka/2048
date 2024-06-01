"""
A class that represents a game of 2048 with custom size and goal.
"""
from Classes.Board import *
import os.path
import time
import tkinter as tk


class Game:
    def __init__(self, size=4, goal=2048):
        """
        Initializes an instance of a game with a board of the given size and goal
        By default the size is 4 and the goal is 2048
        Parameters:
            optional size (int): The size of the board
            optional goal (int): The goal as in the tile that player aims to achieve
        Returns:
            None
        """
        self.board = Board(size, goal)

    def save_file(self, file_name=None) -> bool:
        file_saved = False
        """
        Saves the current state of the board into a file with a given name
        Only saves the game if the save file name is not already in use
        Parameters:
            file_name (str): the name of the file to save
        Returns:
            bool: True if the file was saved, False otherwise
        """
        if file_name is None:
            file_name = input('Enter save file name: ')
        file_path = f'Saves/{file_name}.txt'
        if os.path.isfile(file_path):
            print('such file save already exists, choose a different name')
        else:
            try:
                with open(file_path, 'w') as fSave:
                    fSave.write(f'{self.board.size} {self.board.goal}\n')
                    string_tiles = [' '.join([str(tile) for tile in row]) for row in self.board.tiles]
                    fSave.write('\n'.join(string_tiles))
                print('file saved')
                file_saved = True
            except (FileNotFoundError, PermissionError, OSError):
                print('error saving the file')
                try:
                    os.remove(file_path)
                except OSError:
                    pass
                return False
        return file_saved

    def load_file(self, file_name=None) -> bool:
        """
        Loads the state of the board from a file with a given name
        If no name is given, name is read from the CLI user input
        Parameters:
            file_name (str): the of the file to load
        Returns:
            bool: True is the file was loaded, False otherwise
        """
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
                except (ValueError, FileNotFoundError, PermissionError, OSError):
                    print('error loading save file')
                    return False

    def save_score(self, file_name=None) -> bool:
        """
        Saves the current score to the file with the given name
        If no name is given, name is read from the CLI user input
        Parameters:
            file_name (str): the name of the score file
        Returns:
            bool: True if the score was saved, False otherwise
        """
        if file_name is None:
            file_name = input('Enter score file name: ')
        file_path = f'Scores/{file_name}.txt'
        if os.path.isfile(file_path):
            print('such score name already exists, choose a different name')
            return False
        else:
            try:
                with open(file_path, 'w') as fSave:
                    fSave.write(f'{file_name} {self.board.get_score_on_board()}')
                    print('score saved')
                    return True
            except (FileNotFoundError, PermissionError, OSError):
                try:
                    os.remove(file_path)
                except OSError:
                    pass
                print('error saving the score')
                return False

    def get_leaderboard(self) -> list[tuple[str, int]]:
        """
        Gets the leaderboard from the saved score files and returns them in a list sorted from high score to low
        In case of an error returns an empty list
        Returns:
            list[tuple[str, int]]: sorted list of tuples in which first element is the name of the score and the second is the score
        """
        score_dict = {}
        for file in os.listdir('Scores'):
            try:
                if file.endswith('.txt'):
                    file_path = f'Scores/{file}'
                    with open(file_path, 'r') as fScore:
                        score_line = fScore.readline().split(' ')
                        score_dict[score_line[0]] = int(score_line[1])
            except (IndexError, FileNotFoundError, PermissionError, OSError):
                print(f"error reading the score from file {file}")
        return sorted(score_dict.items(), key=lambda item: item[1], reverse=True)

    def print_leaderboard(self):
        """
        Prints the leaderboard on the console in the format 'name - scored 0'
        Returns:
            None
        """
        print(f'top scores:')
        leaderboard = self.get_leaderboard()
        for score in leaderboard:
            print(f'{score[0]} - scored {score[1]}')

    def make_computer_move(self):
        """
        Make a single computer move if possible
        Computer moves are based on a simple greedy algorithm that makes the possible move with the highest amount of empty tiles
        Returns:
            None
        """
        if self.board.is_there_move_possible():
            direction = self.board.get_direction_with_highest_empty_tiles()
            if self.board.make_move(direction):
                if self.board.is_there_empty_tile():
                    self.board.generate_new_tile()
                self.board.print_board()
    def play_game_computer(self):
        """
        Lets the computer play the game until its over
        Computer moves are based on a simple greedy algorithm that makes the possible move with the highest amount of empty tiles
        Returns:
            None
        """
        while self.board.is_there_move_possible():
            time.sleep(0.2)
            self.make_computer_move()

    def display_main_menu(self):
        """
        Function used to display the main menu and handle its control by inputs
        Commands:
            game - new game
            load - load file
            comp - play computer
            q - quit the application
            leaderboard - display the leaderboard
        Returns:
            None
        """
        while True:
            move = input(
                "Enter game to play a new game or leaderboard to display the leaderboard or load to load a file or comp for computer game or q to quit: ").strip().lower()
            if move == 'game':
                self.handle_console_game()
            elif move == 'leaderboard':
                self.print_leaderboard()
            elif move == 'save':
                self.save_file()
            elif move == 'load':
                self.load_file()
            elif move == 'q':
                break
            else:
                print("invalid input")


    def handle_console_game(self):
        """
        Function used to play the game on the console
        Commands:
            wsad is used for moving the tiles
            q for quitting the game
            save for saving current state of the board
            score for saving current score
            comp for initializing ai completing the game
            leaderboard for showing the leaderboard
        Returns:
            None
        """
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
                print("Quit chosen")
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
