import copy

from exceptions import InvalidLocationException
from settings import Settings


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "({}, {})".format(self.x + 1, self.y + 1)

    def offset(self, direction, reverse=False):
        if reverse:
            self.x -= direction[0]
            self.y -= direction[1]
        else:
            self.x += direction[0]
            self.y += direction[1]

    def copy(self):
        return Location(self.x, self.y)

    def is_on_board(self):
        return 0 <= self.x <= 7 and 0 <= self.y <= 7

class Board:
    _board_array = None

    def __init__(self):
        board_content = []
        for i in range(8):
            board_content.append([' '] * 8)
        self._board_array = board_content

    def reset_board(self):
        for x in range(8):
            for y in range(8):
                self._board_array[x][y] = ' '

        # Starting pieces
        self._board_array[3][3] = Settings.tile_1
        self._board_array[3][4] = Settings.tile_2
        self._board_array[4][3] = Settings.tile_2
        self._board_array[4][4] = Settings.tile_1

    def check_valid_location(self, x, y):
        if self._board_array[x][y] != ' ' or not Location(x, y).is_on_board():
            raise InvalidLocationException()

    def getBoardCopy(self):
        # Make a duplicate of the board list and return the duplicate.
        board = Board()
        board._board_array = copy.deepcopy(self._board_array)
        return board
