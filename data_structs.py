from __future__ import annotations

import copy

from typing import List

from settings import Settings


class Vector:
    def __init__(self, *coordinates) -> None:
        self.coordinates = list(coordinates)

    def get_x(self):
        return self.coordinates[0]

    def get_y(self):
        return self.coordinates[1]

    def set_x(self, x):
        self.coordinates[0] = x

    def set_y(self, y):
        self.coordinates[1] = y

    def __eq__(self, other: Vector) -> bool:
        return self.coordinates == other.coordinates

    def __str__(self) -> str:
        return "({})".format(", ".join([str(i) for i in self.coordinates]))

    def offset(self, direction: List[int], reverse: bool = False) -> None:
        if len(self.coordinates) != len(direction):
            raise ValueError("Different length of vector and direction")
        if reverse:
            self.coordinates = [a + b for a, b in zip(self.coordinates, direction)]
        else:
            self.coordinates = [a - b for a, b in zip(self.coordinates, direction)]


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
