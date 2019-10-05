from __future__ import annotations

import copy

from settings import Settings


class Vector:
    def __init__(self, *coordinates) -> None:
        if len(coordinates) != len(Settings.dimensions):
            raise ValueError("Wrong coordinates dimension length")
        self.coordinates = list(coordinates)

    def get_coordinate(self, axis_no: int) -> int:
        return self.coordinates[axis_no]

    def __eq__(self, other: Vector) -> bool:
        return self.coordinates == other.coordinates

    def __str__(self) -> str:
        return "({})".format(", ".join([str(i) for i in self.coordinates]))

    def offset(self, other: Vector, reverse: bool = False) -> None:
        if reverse:
            self.coordinates = [a + b for a, b in zip(self.coordinates, other.coordinates)]
        else:
            self.coordinates = [a - b for a, b in zip(self.coordinates, other.coordinates)]


class Position(Vector):
    def is_on_board(self) -> bool:
        for i, dim in enumerate(Settings.dimensions):
            if not(0 <= self.get_coordinate(i) <= dim - 1):
                return False
        return True

    def copy(self) -> Position:
        return Position(*self.coordinates)


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
        return location.is_on_board() and self._board_array[location.get_coordinate(0)][location.get_coordinate(1)] == Settings.empty_tile

    def duplicate_board(self) -> Board:
        """
        Make a duplicate of the board and return the duplicate.
        """
        board = Board()
        board._board_array = copy.deepcopy(self._board_array)
        return board
