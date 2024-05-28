import tkinter as tk
from tkinter import simpledialog
from Classes.Board import *
from Classes.Game import *


class GUI:
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
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_command(label="Save Game", command=self.save_file)
        file_menu.add_command(label="Load Game", command=self.load_file)
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
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(self.root)
        self.frame.grid()

        for i in range(self.size):
            for j in range(self.size):
                tile = tk.Label(self.frame, text="", width=4, height=2, font=("Helvetica", 24), borderwidth=2, relief="groove")
                tile.grid(row=i, column=j, padx=5, pady=5)
                self.tiles[i][j] = tile

    def update_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.game.board.tiles[i][j]
                self.tiles[i][j].configure(text=str(value) if value != 0 else "", bg=self.get_tile_color(value))

    def print_leaderboard(self):
        top_scores = self.game.get_leaderboard()[:self.leaderboard_size]
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")

        for i, (name, score) in enumerate(top_scores, start=1):
            tk.Label(leaderboard_window, text=f"{i}. {name}: {score}").pack()
    def get_tile_color(self, value):
        colors = {
            0: "#CDC1B4", 2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563",
            32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72", 256: "#EDCC61",
            512: "#EDC850", 1024: "#EDC53F", 2048: "#EDC22E"
        }
        return colors.get(value, "#CDC1B4")

    def play_computer_game(self):
        while self.game.board.is_there_move_possible():
            time.sleep(0.4)
            direction = self.game.board.get_direction_with_highest_empty_tiles()
            if self.game.board.make_move(direction):
                if self.game.board.is_there_empty_tile():
                    self.game.board.generate_new_tile()
            self.update_grid()

    def handle_keypress(self, event):
        key = event.keysym
        if key in ['w', 's', 'a', 'd']:
            direction = {
                'w': Direction.UP,
                's': Direction.DOWN,
                'a': Direction.LEFT,
                'd': Direction.RIGHT
            }[key]
            if self.game.board.make_move(direction):
                self.update_grid()
                if self.game.board.is_goal_reached():
                    self.root.title("2048 Game - Goal Reached!")
                if not self.game.board.is_there_move_possible():
                    messagebox.showinfo("Game Over", "No more moves possible. Game over!")
                    self.root.unbind("<Key>")
                else:
                    if self.game.board.is_there_empty_tile():
                        self.game.board.generate_new_tile()
                    self.update_grid()
