# Author: Kento Woolery
# Date: 3/11/2020
# Description: Simulates a boardgame-like game

class FBoard:
    """Creates an FBoard game object"""

    def __init__(self):
        """Initializes the game board to an 8 X 8 list of lists with player x in space (0, 0) and
        o players in spaces (5, 7), (6, 6), (7, 5), and (7, 7)"""
        self._game_board = [["x", "_", "_", "_", "_", "_", "_", "_"],
                            ["_", "_", "_", "_", "_", "_", "_", "_"],
                            ["_", "_", "_", "_", "_", "_", "_", "_"],
                            ["_", "_", "_", "_", "_", "_", "_", "_"],
                            ["_", "_", "_", "_", "_", "_", "_", "_"],
                            ["_", "_", "_", "_", "_", "_", "_", "o"],
                            ["_", "_", "_", "_", "_", "_", "o", "_"],
                            ["_", "_", "_", "_", "_", "o", "_", "o"]]
        self._game_state = "UNFINISHED"
        self._x_row = 0
        self._x_column = 0

    def get_game_state(self):
        """Returns the game state"""
        return self._game_state

    def get_x_row(self):
        """Returns the row of the 'x' piece"""
        return self._x_row

    def get_x_column(self):
        """Returns the column of the 'x' piece"""
        return self._x_column

    def available_move_x(self, new_x_row, new_x_column):
        """Checks if attempted move of 'x' piece is valid"""
        if self._game_board[new_x_row][new_x_column] == "_":
            if new_x_row == (self._x_row + 1):
                if new_x_column == (self._x_column + 1):
                    return True
                elif new_x_column == (self._x_column - 1):
                    return True
                else:
                    return False
            elif new_x_row == (self._x_row - 1):
                if new_x_column == (self._x_column + 1):
                    return True
                elif new_x_column == (self._x_column - 1):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def available_move_o(self, initial_o_row, initial_o_column, new_o_row, new_o_column):
        """Checks if attempted move of 'o' piece is valid"""
        if self._game_board[initial_o_row][initial_o_column] == "o":
            if self._game_board[new_o_row][new_o_column] == "_":
                if new_o_row == (initial_o_row + 1):
                    if new_o_column == (initial_o_column - 1):
                        return True
                    else:
                        return False
                if new_o_row == (initial_o_row - 1):
                    if new_o_column == (initial_o_column + 1):
                        return True
                    elif new_o_column == (initial_o_column - 1):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


    def move_x(self, new_x_row, new_x_column):
        """Moves the x player along the game board"""
        if self._game_state != "UNFINISHED":
            """Makes sure the game is still in progress"""
            return False
        elif self.available_move_x(new_x_row, new_x_column):
            """If the move is valid..."""
            self._game_board[self._x_row][self._x_column] = "_"
            self._x_row = new_x_row
            self._x_column = new_x_column
            self._game_board[self._x_row][self._x_column] = "x"
            if self._game_board[7][7] == "x":
                self._game_state = "X_WON"
            return True

    def move_o(self, initial_o_row, initial_o_column, new_o_row, new_o_column):
        """Selects an 'o' piece and moves it along the game board"""
        if self._game_state != "UNFINISHED":
            """Makes sure the game is still in progress"""
            return False
        elif self.available_move_o(initial_o_row, initial_o_column, new_o_row, new_o_column):
            """If the move is valid..."""
            self._game_board[initial_o_row][initial_o_column] = "_"
            self._game_board[new_o_row][new_o_column] = "o"
            if self._game_board[self._x_row + 1][self._x_column + 1] == "o":
                if self._game_board[self._x_row + 1][self._x_column - 1] == "o":
                    if self._game_board[self._x_row - 1][self._x_column + 1] == "o":
                        if self._game_board[self._x_row - 1][self._x_column - 1] == "o":
                            """Checks if all possible moves for 'x' are now blocked and if so, awards an 'o' victory"""
                            self._game_state = "O_WON"
            return True


    def print_game_board(self):
        print(self._game_board)

    def print_game_state(self):
        print(self._game_state)

    def print_x_location(self):
        print(self._x_row, self._x_column)
