from Classes.Board import *
class Game:
    def __init__(self, size:int, goal:int):
        self.board = Board(size,goal)

    def play(self):
        self.board.print_board()
        while True:
            self.board.print_board()
            move = input("Enter move (w/a/s/d for up/left/down/right or q to quit): ").strip().lower()
            if move == 'q':
                print("Game over!")
                break
            elif move in ['w', 'a', 's', 'd']:
                direction = {'w': Direction.UP, 'a': Direction.LEFT, 's': Direction.DOWN, 'd': Direction.RIGHT}[
                    move]
                self.board.make_move(direction)
                if self.board.is_there_empty_tile():
                    self.board.generate_new_tile()
                if self.board.is_there_empty_tile():
                    self.board.generate_new_tile()
                if not self.board.is_there_move_possible():
                    print("No more moves possible. Game over!")
                    self.board.print_board()
                    break
            else:
                print("Invalid input. Use w/a/s/d for direction or q to quit.")