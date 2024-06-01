from Classes.Game import  *
from Classes.GUI import *


if __name__ == '__main__':
    game_type = input('enter 1 for console game, 2 for GUI version: ')
    while True:
        if game_type == '1':
            game = Game()
            game.display_main_menu()
            break
        if game_type == '2':
            root = tk.Tk()
            app = GUI(root)
            root.mainloop()
            break
        else:
            game_type = input('enter 1 for console game, 2 for GUI version: ')
