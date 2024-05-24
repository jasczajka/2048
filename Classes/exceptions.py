class WrongBoardSizeError(Exception):
    """Raise when board size is not an integer or below 2"""
class WrongGoalError(Exception):
    """Raise when goal is not an integer over 4 or not a power of 2"""