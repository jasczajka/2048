from Classes.Board import *


if __name__ == '__main__':
    board1 = Board(4)

    board1.board = [
    [0, 2, 2, 4],
    [2, 0, 0, 4],
    [2, 0, 2, 4],
    [2, 4, 4, 4]
]
    board1.print_board()
    board1.make_move(Direction.RIGHT)
    board1.print_board()
    board1.generate_new_tile()
    board1.generate_new_tile()
    board1.generate_new_tile()
    board1.generate_new_tile()
    board1.print_board()



