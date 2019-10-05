from __future__ import annotations

import copy
import itertools

from typing import List

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
        board_content = Settings.empty_tile
        for dim in Settings.dimensions:
            next_dimension = []
            for i in range(dim):
                next_dimension.append(copy.deepcopy(board_content))
            board_content = next_dimension
        self._board_array = board_content

    def set_value(self, position: Position, value):
        if not position.is_on_board():
            raise ValueError("position is not in board")
        elements = self._board_array
        for i in position.coordinates[:-1]:
            elements = elements[i]
        elements[position.coordinates[-1]] = value

    def reset_board(self):
        """
        Reset the board to the starting position of reversi board.
        """
        self._board_array = Board()._board_array
        coordinates = []
        for dim in Settings.dimensions:
            coordinates.append([dim//2-1, dim//2])  # choose the mid 2 coordinate
        for position in [Position(*coordinate) for coordinate in itertools.product(*coordinates)]:
            if sum(position.coordinates) % 2:  # alternate choosing
                self.set_value(position, Settings.tile_2)
            else:
                self.set_value(position, Settings.tile_1)

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
