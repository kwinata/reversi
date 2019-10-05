from __future__ import annotations

import copy

from typing import Tuple

from settings import Settings


class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Vector) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return "({}, {})".format(self.x + 1, self.y + 1)

    def offset(self, direction: Tuple[int, int], reverse: bool = False) -> None:
        if reverse:
            self.x -= direction[0]
            self.y -= direction[1]
        else:
            self.x += direction[0]
            self.y += direction[1]


class Location(Vector):
    """
    A pointer to a cell on board

    Args:
        x : x axis value (valid from 0 to 7)
        y : y axis value (valid from 0 to 7)
    """
    def is_on_board(self) -> bool:
        return 0 <= self.x <= 7 and 0 <= self.y <= 7

    def copy(self) -> Location:
        return Location(self.x, self.y)


class Board:
    """
    A data structure representing the reversi board.
    """
    _board_array = None

    def __init__(self):
        board_content = []
        for i in range(8):
            board_content.append([' '] * 8)
        self._board_array = board_content

    def reset_board(self):
        """
        Reset the board to the starting position of reversi board.
        """
        for x in range(8):
            for y in range(8):
                self._board_array[x][y] = ' '

        # Starting pieces
        self._board_array[3][3] = Settings.tile_1
        self._board_array[3][4] = Settings.tile_2
        self._board_array[4][3] = Settings.tile_2
        self._board_array[4][4] = Settings.tile_1

    def is_empty_and_on_board(self, location: Location) -> bool:
        """
        Checks whether the board is empty at the ``location`` and
        still inside the board

        Args:
            location : the ``Location`` object to be checked
        """
        return location.is_on_board() and self._board_array[location.x][location.y] == Settings.empty_tile

    def duplicate_board(self) -> Board:
        """
        Make a duplicate of the board and return the duplicate.
        """
        board = Board()
        board._board_array = copy.deepcopy(self._board_array)
        return board
