"""
A class that represents graphical interface of 2048 game made with standard tkinter library
"""
import tkinter as tk
from tkinter import simpledialog, messagebox
from Classes.Board import *
from Classes.Game import *


class GUI:
    """
    Initializes an instance of a game with a board of the given size and goal and interface
    By default the size is 4 and the goal is 2048
    Leaderboard size is also set here
    Parameters:
        optional size (int): The size of the board
        optional goal (int): The goal as in the tile that player aims to achieve
    Returns:
        None
    """
    def __init__(self, root, size=4, goal=2048):
        self.leaderboard_size = 10
        self.root = root
        self.root.title("2048 Game")
        self.size = size
        self.game = Game(size, goal)
        self.frame = None
        self.tiles = [[None for _ in range(size)] for _ in range(size)]
        self.create_menu()
        self.create_grid()
        self.update_grid()

        self.root.bind("<Key>", self.handle_keypress)

    def create_menu(self):
        """
        Creates the menu for the game
        Options:
            new game
            save game
            load game
            computer game - let the simple ai complete the game
            quit
            save score
            view leaderboard
        Returns:
            None
        """
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_command(label="Save Game", command=self.save_file)
        file_menu.add_command(label="Load Game", command=self.load_file)
        file_menu.add_command(label="Next computer move", command=self.make_computer_move)
        file_menu.add_command(label="Computer Game", command=self.play_computer_game)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        leaderboard_menu = tk.Menu(menu_bar, tearoff=0)
        leaderboard_menu.add_command(label="Save Score", command=self.save_score)
        leaderboard_menu.add_command(label="View Leaderboard", command=self.print_leaderboard)
        menu_bar.add_cascade(label="Leaderboard", menu=leaderboard_menu)





        self.root.config(menu = menu_bar)
    def new_game(self):
        """
        Creates a new instance of the game for the interface
        Updates the game tiles
        Returns:
             None
        """
        while True:
            size = simpledialog.askinteger("New Game", "Enter size of the board:", minvalue=2, maxvalue=10)
            goal = simpledialog.askinteger("New Game", "Enter goal (e.g., 2048):", minvalue=8)
            if size and goal:
                try:
                    self.game = Game(size, goal)
                    self.tiles = [[None for _ in range(size)] for _ in range(size)]
                    self.size = size
                    self.create_grid()
                    self.update_grid()
                    self.root.title("2048 Game")
                    self.root.bind("<Key>", self.handle_keypress)
                    break
                except WrongBoardSizeError as e:
                    messagebox.showinfo("New game error", str(e))
                except WrongGoalError as e:
                    messagebox.showinfo("New game error", str(e))

    def load_file(self):
        """
        Helper function for loading a saved file
        Returns:
            None
        """
        name = simpledialog.askstring("Load file", "Enter file name: ")
        if name:
            if not self.game.load_file(name):
                messagebox.showinfo("Load error", "error loading file save, perhaps the file doesn't exist?")
            else:
                self.size = len(self.game.board.tiles[0])
                self.tiles = [[None for _ in range(self.size)] for _ in range(self.size)]
                self.create_grid()
                self.update_grid()
                self.root.title("2048 Game")

                #in case a game is over
                self.root.unbind("<Key>")
                self.root.bind("<Key>", self.handle_keypress)


    def save_file(self):
        """
        Helper function for saving the current state of the board
        Returns:
            None
        """
        name = simpledialog.askstring("Save file", "Enter file name: ")
        if name:
            if not self.game.save_file(name):
                messagebox.showinfo("Save file", "error saving, perhaps the name is already in use or save is corrupted?")
            else:
                messagebox.showinfo("Save file", "save successful")

    def save_score(self):
        name = simpledialog.askstring("Save Score", "Enter your name:")
        if name:
            if self.game.save_score(name):
                messagebox.showinfo("Save Score", "Score saved successfully.")
            else:
                messagebox.showinfo("Save Score", "something went wrong, try a different name")


    def create_grid(self):
        """
        Creates the GUI tile grid for the game from the Game object from scratch
        Used when a new game is started
        Returns:
            None
        """
        if self.frame:
            self.next_computer_move_button.destroy()
            self.frame.destroy()

        self.frame = tk.Frame(self.root)
        self.frame.grid(sticky="w")

        for i in range(self.size):
            for j in range(self.size):
                tile = tk.Label(self.frame, text="", width=4, height=2, font=("Helvetica", 24), borderwidth=2, relief="groove")
                tile.grid(row=i, column=j, padx=5, pady=5)
                self.tiles[i][j] = tile
        self.next_computer_move_button = tk.Button(
            text="Next computer move", command=self.make_computer_move)
        self.next_computer_move_button.grid(row=len(self.game.board.tiles), column = len(self.game.board.tiles), padx=5, pady=5)


    def update_grid(self):
        """
        Updates the GUI tile grid based on the current state of the board in Game object
        Returns:
             None
        """
        for i in range(self.size):
            for j in range(self.size):
                value = self.game.board.tiles[i][j]
                self.tiles[i][j].configure(text=str(value) if value != 0 else "", bg=self.get_tile_color(value))

    def print_leaderboard(self):
        """
        Creates and displays a new window with loaded leaderboard from saved score files
        Shows only top x scores, where x is set in the init function as leaderboard_size
        Returns:
            None
        """
        top_scores = self.game.get_leaderboard()[:self.leaderboard_size]
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")

        for i, (name, score) in enumerate(top_scores, start=1):
            tk.Label(leaderboard_window, text=f"{i}. {name}: {score}").pack()

    def get_tile_color(self, value: int) -> str:
        """
        Gets color in hexagonal based on the value of the tile.
        By default it returns #CDC1B4.
        Parameters:
            value (int): The value of the tile of which color is needed.
        Returns:
            str: The hexagonal value of the tile color.
        """
        colors = {
            0: "#CDC1B4", 2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563",
            32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72", 256: "#EDCC61",
            512: "#EDC850", 1024: "#EDC53F", 2048: "#EDC22E",
            4096: "#3D3A32", 8192: "#2E3A32", 16384: "#1F3A32"
        }
        return colors.get(value, "#CDC1B4")

    def make_computer_move(self):
        self.game.make_computer_move()
        self.update_grid()

    def play_computer_game(self):
        """
        Helper function for letting the computer play the game until its over
        Algorith described in Game class
        Returns:
            None
        """
        while self.game.board.is_there_move_possible():
            direction = self.game.board.get_direction_with_highest_empty_tiles()
            if self.game.board.make_move(direction):
                if self.game.board.is_there_empty_tile():
                    self.game.board.generate_new_tile()
                self.update_grid()

    def handle_keypress(self, event: tk.Event):
        """
        Helper function for handling wsad key presses and moves
        Bound when a game is in progress, if the game is over, unbound
        Parameters:
            event (tkinter.Event): The event to which we want to bind the function
        Returns:
            None
        """
        key = event.keysym
        if key in ['w', 's', 'a', 'd']:
            direction = {
                'w': Direction.UP,
                's': Direction.DOWN,
                'a': Direction.LEFT,
                'd': Direction.RIGHT
            }[key]
            if not self.game.board.is_there_move_possible():
                messagebox.showinfo("Game Over", "No more moves possible. Game over!")
                self.root.unbind("<Key>")
            if self.game.board.make_move(direction):
                self.update_grid()
                if self.game.board.is_goal_reached():
                    self.root.title("2048 Game - Goal Reached!")
                else:
                    if self.game.board.is_there_empty_tile():
                        self.game.board.generate_new_tile()
                    self.update_grid()
