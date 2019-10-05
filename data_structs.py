from __future__ import annotations

import copy

from typing import Tuple

from settings import Settings


class Vector:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def __eq__(self, other: Vector) -> bool:
        return self.get_x() == other.get_x() and self.get_y() == other.get_y()

    def __str__(self) -> str:
        return "({}, {})".format(self.get_x() + 1, self.get_y() + 1)

    def offset(self, direction: Tuple[int, int], reverse: bool = False) -> None:
        if reverse:
            self.set_x(self.get_x() - direction[0])
            self.set_y(self.get_y() - direction[1])
        else:
            self.set_x(self.get_x() + direction[0])
            self.set_y(self.get_y() + direction[1])


class Position(Vector):
    """
    A pointer to a cell on board

    Args:
        x : x axis value (valid from 0 to 7)
        y : y axis value (valid from 0 to 7)
    """
    def is_on_board(self) -> bool:
        return 0 <= self.get_x() <= 7 and 0 <= self.get_y() <= 7

    def copy(self) -> Position:
        return Position(self.get_x(), self.get_y())


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

    def is_empty_and_on_board(self, location: Position) -> bool:
        """
        Checks whether the board is empty at the ``location`` and
        still inside the board

        Args:
            location : the ``Position`` object to be checked
        """
        return location.is_on_board() and self._board_array[location.get_x()][location.get_y()] == Settings.empty_tile

    def duplicate_board(self) -> Board:
        """
        Make a duplicate of the board and return the duplicate.
        """
        board = Board()
        board._board_array = copy.deepcopy(self._board_array)
        return board
