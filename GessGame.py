# Author: Kento Woolery
# Date 5/23/2020
# Description: Class that represents a board game with a rule set similar to combining Chess and Go.


class SuicideError(Exception):
    """Exception case to be raised when a player's move would otherwise cause them to be without a ring."""
    pass


class GessGame:
    """Creates an object representing the chess/go alternative board game, Gess. See the ReadMe for detailed rules, but
    the basic idea is to remove all of the opponent's rings. Rings are any 3x3 "piece" with an empty center and the
    player's stones in all 8 surrounding spaces. Pieces move based on the layout of stones within their piece.
    Doesn't communicate with any other classes. All functionality is built within this class's methods."""

    def __init__(self):
        """Initializes the GessGame with a game board in the starting layout, the turn number at 1,
        and the game state as 'UNFINISHED'. 'X's represent Black stones and 'O's represent white stones."""
        self._game_board = [
            ['  ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'],
            [' 1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            [' 2', '_', '_', 'X', '_', 'X', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '_', 'X', '_', 'X', '_', '_'],
            [' 3', '_', 'X', 'X', 'X', '_', 'X', '_', 'X', 'X', 'X', 'X', '_', 'X', '_', 'X', '_', 'X', 'X', 'X', '_'],
            [' 4', '_', '_', 'X', '_', 'X', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '_', 'X', '_', 'X', '_', '_'],
            [' 5', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            [' 6', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            [' 7', '_', '_', 'X', '_', '_', 'X', '_', '_', 'X', '_', '_', 'X', '_', '_', 'X', '_', '_', 'X', '_', '_'],
            [' 8', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            [' 9', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['10', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['11', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['12', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['13', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['14', '_', '_', 'O', '_', '_', 'O', '_', '_', 'O', '_', '_', 'O', '_', '_', 'O', '_', '_', 'O', '_', '_'],
            ['15', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['16', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['17', '_', '_', 'O', '_', 'O', '_', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '_', 'O', '_', 'O', '_', '_'],
            ['18', '_', 'O', 'O', 'O', '_', 'O', '_', 'O', 'O', 'O', 'O', '_', 'O', '_', 'O', '_', 'O', 'O', 'O', '_'],
            ['19', '_', '_', 'O', '_', 'O', '_', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '_', 'O', '_', 'O', '_', '_'],
            ['20', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']]
        self._turnNumber = 1
        self._game_state = 'UNFINISHED'

    def print_board(self):
        """Prints out the current layout of the game board. Primarily for debugging purposes."""
        print(self._game_board)
        return

    def get_game_state(self):
        """Simply returns the status of the game. Either 'UNFINISHED', 'BLACK_WON', or 'WHITE_WON'."""
        return self._game_state

    def resign_game(self):
        """Sets the game state as the other player having won. Determines winner based on turn count when called.
        Since Black always starts, they will always play on odd turns; White on even turns."""
        if self._turnNumber % 2 == 0:
            self._game_state = "BLACK_WON"
        else:
            self._game_state = "WHITE_WON"
        # print(self.get_game_state())
        return

    def ring_check(self, player):
        """Takes the string that represents the player ('X' for black, 'O' for white), and searches the actual playable
        game board for a ring of that player's stones. Returns a bool based on if one was found or not. Is called
        at the end of every turn to check for suicide and victory."""
        for row in self._game_board[3:19]:
            for i in range(3, 19):
                if row[i] == "_":
                    footprint = self.create_footprint(self._game_board[0][i] + str(self._game_board.index(row)))
                    if footprint["NW"] == player and footprint["N"] == player and footprint["NE"] == player and \
                            footprint["W"] == player and footprint["E"] == player and \
                            footprint["SW"] == player and footprint["S"] == player and footprint["SE"] == player:
                        return True

        if self._turnNumber % 2 == 0 and player == '0':
            """if it's white's turn and their move causes them to no longer have a ring"""
            raise SuicideError
        elif self._turnNumber % 2 == 1 and player == 'X':
            """if it's black's turn and their move causes them to no longer have a ring"""
            raise SuicideError
        return False

    def create_footprint(self, center):
        """Takes a string representing the center space of the designated "piece" as a parameter (for example "b7").
        Determines the row and column indexes for that center space, and then creates a dictionary with cardinal and
        intermediate directions as keys and contents of corresponding spaces as related values for the 3x3 footprint
        surrounding the center. Returns the created dictionary."""
        column = self._game_board[0].index(center[0].upper())
        row = int(center[1:])
        footprint = {
            "NW": self._game_board[row - 1][column - 1],
            "N": self._game_board[row - 1][column],
            "NE": self._game_board[row - 1][column + 1],
            "W": self._game_board[row][column - 1],
            "C": self._game_board[row][column],
            "E": self._game_board[row][column + 1],
            "SW": self._game_board[row + 1][column - 1],
            "S": self._game_board[row + 1][column],
            "SE": self._game_board[row + 1][column + 1]
        }
        return footprint

    def calculate_direction(self, current_center, new_center):
        """Takes strings that represent the center square of the piece being moved and the desired new location
        of the center square as parameters. Determines what direction the piece is attempting to move and returns it
        as a string (i.e. "N" for north).
         If it is an invalid direction (not directly orthogonal or diagonal), or doesn't move, returns False."""
        current_column = self._game_board[0].index(current_center[0].upper())
        current_row = int(current_center[1:])

        new_column = self._game_board[0].index(new_center[0].upper())
        new_row = int(new_center[1:])

        row_change = abs(current_row - new_row)
        column_change = abs(current_column - new_column)

        if new_column == current_column:
            """It is a North or South move"""
            if new_row > current_row:
                return "S"
            elif new_row < current_row:
                return "N"
            else:
                return False

        elif new_row == current_row:
            """It is an East or West move"""
            if new_column > current_column:
                return "E"
            elif new_column < current_column:
                return "W"
            else:
                return False

        elif (new_row < current_row) and (new_column < current_column):
            """it is a NorthWest move"""
            if row_change == column_change:
                """if it is a true diagonal"""
                return "NW"

        elif (new_row < current_row) and (new_column > current_column):
            """it is a NorthEast move"""
            if row_change == column_change:
                """if it is a true diagonal"""
                return "NE"

        elif (new_row > current_row) and (new_column < current_column):
            """it is a SouthWest move"""
            if row_change == column_change:
                """if it is a true diagonal"""
                return "SW"

        elif (new_row > current_row) and (new_column > current_column):
            """it is a SouthEast move"""
            if row_change == column_change:
                """it is a true diagonal"""
                return "SE"

        return False

    def spaces_moved_is_valid(self, current_center, new_center):
        """Takes strings that represent the center square of the piece being moved and the desired new location
        of the center square as parameters. Calculates the number of spaces in the proposed move.
        Determines if it is a valid proposal based on the contents of the center space. Returns a relevant bool."""
        current_column = self._game_board[0].index(current_center[0].upper())
        current_row = int(current_center[1:])

        new_column = self._game_board[0].index(new_center[0].upper())
        new_row = int(new_center[1:])

        row_change = abs(current_row - new_row)
        column_change = abs(current_column - new_column)

        current_footprint = self.create_footprint(current_center)

        if current_footprint["C"] == "_":  # if the center is empty
            max_moves = 3
        else:
            max_moves = 18  # theoretical limit since it is an 18x18 playable board space

        if row_change <= max_moves and column_change <= max_moves:
            return True
        # print("Spaces moved is invalid.")
        return False

    def obstruction_check(self, current_center, new_center):
        """Takes strings that represent the center square of the piece being moved and the desired new location
        of the center square as parameters. Simulates the proposed move incrementally up to but _not_ including the
        last move and checks for obstruction at each step. Returns a relevant bool based on if it finds obstruction."""

        current_column = self._game_board[0].index(current_center[0].upper())
        current_row = int(current_center[1:])

        new_column = self._game_board[0].index(new_center[0].upper())
        new_row = int(new_center[1:])

        row_change = abs(current_row - new_row)
        column_change = abs(current_column - new_column)

        if self.calculate_direction(current_center, new_center) == "NW":
            for i in range(1, row_change):
                current_column -= 1
                current_row -= 1
                center_string = self._game_board[0][current_column] + str(current_row)
                footprint = self.create_footprint(center_string)
                for item in footprint:
                    if footprint[item] != "_":
                        return False

        elif self.calculate_direction(current_center, new_center) == "N":
            for i in range(1, row_change):
                current_row -= 1
                center_string = self._game_board[0][current_column] + str(current_row)
                footprint = self.create_footprint(center_string)
                for item in footprint:
                    if footprint[item] != "_":
                        return False

        elif self.calculate_direction(current_center, new_center) == "NE":
            for i in range(1, row_change):
                current_column += 1
                current_row -= 1
                center_string = self._game_board[0][current_column] + str(current_row)
                footprint = self.create_footprint(center_string)
                for item in footprint:
                    if footprint[item] != "_":
                        return False

        elif self.calculate_direction(current_center, new_center) == "W":
            for i in range(1, column_change):
                current_column -= 1
                center_string = self._game_board[0][current_column] + str(current_row)
                footprint = self.create_footprint(center_string)
                for item in footprint:
                    if footprint[item] != "_":
                        return False

        elif self.calculate_direction(current_center, new_center) == "E":
            for i in range(1, column_change):
                current_column += 1
                center_string = self._game_board[0][current_column] + str(current_row)
                footprint = self.create_footprint(center_string)
                for item in footprint:
                    if footprint[item] != "_":
                        return False

        elif self.calculate_direction(current_center, new_center) == "SW":
            for i in range(1, row_change):
                current_column -= 1
                current_row += 1
                center_string = self._game_board[0][current_column] + str(current_row)
                footprint = self.create_footprint(center_string)
                for item in footprint:
                    if footprint[item] != "_":
                        return False

        elif self.calculate_direction(current_center, new_center) == "S":
            for i in range(1, row_change):
                current_row += 1
                center_string = self._game_board[0][current_column] + str(current_row)
                footprint = self.create_footprint(center_string)
                for item in footprint:
                    if footprint[item] != "_":
                        return False

        elif self.calculate_direction(current_center, new_center) == "SE":
            for i in range(1, row_change):
                current_column += 1
                current_row += 1
                center_string = self._game_board[0][current_column] + str(current_row)
                footprint = self.create_footprint(center_string)
                for item in footprint:
                    if footprint[item] != "_":
                        return False

        return True

    def edge_removal(self, new_center):
        """Takes the center square of the desired new location as a parameter. Checks to see if it is on an edge,
        and if so, removes stones that are over the edge."""
        new_column = self._game_board[0].index(new_center[0].upper())
        new_row = int(new_center[1:])
        if new_row == 2:
            self._game_board[new_row - 1][new_column - 1] = "_"
            self._game_board[new_row - 1][new_column] = "_"
            self._game_board[new_row - 1][new_column + 1] = "_"

        if new_row == 19:
            self._game_board[new_row + 1][new_column - 1] = "_"
            self._game_board[new_row + 1][new_column] = "_"
            self._game_board[new_row + 1][new_column + 1] = "_"

        if new_column == 2:
            self._game_board[new_row - 1][new_column - 1] = "_"
            self._game_board[new_row][new_column - 1] = "_"
            self._game_board[new_row + 1][new_column - 1] = "_"

        if new_column == 19:
            self._game_board[new_row - 1][new_column + 1] = "_"
            self._game_board[new_row][new_column + 1] = "_"
            self._game_board[new_row + 1][new_column + 1] = "_"

        return

    def is_valid_move(self, current_center, new_center):
        """Takes strings that represent the center square of the piece being moved and the desired new location
         of the center square as parameters. Checks if proposed move is valid. Calls other methods for assistance in
         some validation checks. Returns a relevant bool."""

        # Makes sure the game is still in play
        if self.get_game_state() != "UNFINISHED":
            # print("Game is over.")
            return False

        # Checks to make sure the center square of the piece and desired new location are on the game board
        if current_center[0].upper() not in self._game_board[0]:
            # print("That is not a column on the game board.")
            return False
        if new_center[0].upper() not in self._game_board[0]:
            # print("You are trying to move to a column not on the game board.")
            return False
        if current_center[0].upper() == 'A' or current_center[0].upper() == 'T':
            # print("That center is on the edge of the board and invalid.")
            return False
        if new_center[0].upper() == 'A' or new_center[0].upper() == 'T':
            # print("You are trying to move to a center on the edge of the board and is invalid.")
            return False
        if (int(current_center[1:]) < 2) or (int(current_center[1:]) > 19):
            # print("That row is not on the playable portion of the game board.")
            return False
        if (int(new_center[1:]) < 2) or (int(new_center[1:]) > 19):
            # print("You are trying to move to a row not on the playable portion of the game board.")
            return False

        if self._turnNumber % 2 == 0:
            player = 'O'
            other_player = 'X'
        else:
            player = 'X'
            other_player = 'O'

        # Makes sure the suggested piece is legal (contains at least 1 player stone and no opponent stones)
        current_footprint = self.create_footprint(current_center)
        player_found = False
        for item in current_footprint:
            if other_player in current_footprint[item]:
                # print("The wrong player's stones are in that piece.")
                return False
            if player in current_footprint[item] and not player_found:
                player_found = True
        if not player_found:
            # print("That piece doesn't contain any of your stones.")
            return False

        # Makes sure the suggested movement is valid (the proposed piece has a corresponding direction stone,
        #       and a valid travel distance.)
        if not self.calculate_direction(current_center, new_center):
            # print("Could not calculate a valid direction.")
            return False
        if current_footprint[self.calculate_direction(current_center, new_center)] != player or \
                not self.spaces_moved_is_valid(current_center, new_center):
            return False

        return True

    def make_move(self, current_center, new_center):
        """Takes strings that represent the center square of the piece being moved and the desired new location
        of the center square as parameters. Calls the validation check method to make sure the proposed move is valid.
        If not, simply returns False.
        If it passes the validation checks, it will save the state of the game board then attempt to make the move. If
        carrying out the move removes the current player's last remaining ring, it returns False and restores the
        save state prior to the move. Otherwise finishes the move, checks for breaking the opponents last ring for
        victory and updates game state accordingly, increments the turn, and returns True."""

        if self._turnNumber % 2 == 0:
            player = 'O'
            other_player = 'X'
        else:
            player = 'X'
            other_player = 'O'

        if self.is_valid_move(current_center, new_center):

            current_footprint = self.create_footprint(current_center)
            saved_board = [row[:] for row in self._game_board]
            try:
                old_column = self._game_board[0].index(current_center[0].upper())
                old_row = int(current_center[1:])
                self._game_board[old_row - 1][old_column - 1] = "_"
                self._game_board[old_row - 1][old_column] = "_"
                self._game_board[old_row - 1][old_column + 1] = "_"
                self._game_board[old_row][old_column - 1] = "_"
                self._game_board[old_row][old_column] = "_"
                self._game_board[old_row][old_column + 1] = "_"
                self._game_board[old_row + 1][old_column - 1] = "_"
                self._game_board[old_row + 1][old_column] = "_"
                self._game_board[old_row + 1][old_column + 1] = "_"

                if not self.obstruction_check(current_center, new_center):
                    # print("Cannot complete the move. Something is in the way.")
                    self._game_board = saved_board
                    return False

                new_column = self._game_board[0].index(new_center[0].upper())
                new_row = int(new_center[1:])
                self._game_board[new_row - 1][new_column - 1] = current_footprint["NW"]
                self._game_board[new_row - 1][new_column] = current_footprint["N"]
                self._game_board[new_row - 1][new_column + 1] = current_footprint["NE"]
                self._game_board[new_row][new_column - 1] = current_footprint["W"]
                self._game_board[new_row][new_column] = current_footprint["C"]
                self._game_board[new_row][new_column + 1] = current_footprint["E"]
                self._game_board[new_row + 1][new_column - 1] = current_footprint["SW"]
                self._game_board[new_row + 1][new_column] = current_footprint["S"]
                self._game_board[new_row + 1][new_column + 1] = current_footprint["SE"]

                self.edge_removal(new_center)

                self.ring_check(player)
            except SuicideError:
                self._game_board = saved_board
                # print("That move would leave you without a ring.")
                return False
        else:
            return False

        if not self.ring_check(other_player):
            if player == 'O':
                self._game_state = "WHITE_WINS"
            else:
                self._game_state = "BLACK_WINS"

        self._turnNumber += 1
        return True
