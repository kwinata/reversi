import itertools
from typing import Any, List, Dict

from data_structs import Position, Vector, Board
from settings import Settings


class Rule:
    @staticmethod
    def get_tiles_to_flip_for_move(board: Board, start_loc: Position, tile: Any) -> List[Position]:
        if tile == Settings.tile_1:
            other_tile = Settings.tile_2
        else:
            other_tile = Settings.tile_1

        tiles_to_flip = []

        itertools_input = []
        for i in range(len(Settings.dimensions)):
            itertools_input.append([-1, 0, 1])

        directions = [Vector(*coordinate) for coordinate in itertools.product(*itertools_input)]

        all_zero = Vector(*[0 for i in Settings.dimensions])
        directions.remove(all_zero)

        for direction in directions:
            current_loc = start_loc.copy()
            current_loc.offset(direction)

            while current_loc.is_on_board() and board.get_value(current_loc) == other_tile:
                current_loc.offset(direction)

            if not current_loc.is_on_board():
                continue
            if board.get_value(current_loc) == tile:
                current_loc.offset(direction, reverse=True)
                while current_loc != start_loc:
                    tiles_to_flip.append(current_loc.copy())
                    current_loc.offset(direction, reverse=True)
        return tiles_to_flip

    @staticmethod
    def get_move_result(board: Board, tile: Any, position: Position) -> List[Position]:
        if not board.is_empty_and_on_board(position):
            return []

        return Rule.get_tiles_to_flip_for_move(board, position, tile)

    @staticmethod
    def is_valid_move(self, tile: Any, position: Position)-> bool:
        return bool(Rule.get_move_result(self, tile, position))

    @staticmethod
    def get_valid_moves(board: Board, tile: Any) -> List[int]:
        valid_moves = []
        cells_to_try = itertools.product(*[range(i) for i in Settings.dimensions])
        for cell in cells_to_try:
            if Rule.is_valid_move(board, tile, Position(*cell)):
                valid_moves.append(cell)
        return valid_moves

    @staticmethod
    def get_board_with_hints(board: Board, tile: Any) -> Board:
        new_board_for_printing_only = board.duplicate_board()

        for cell in Rule.get_valid_moves(board, tile):
            new_board_for_printing_only.set_value(Position(*cell), Settings.tile_hint)

        return new_board_for_printing_only

    @staticmethod
    def get_score_of_board(board: Board) -> Dict[Any, int]:
        # To be used by alpha beta, may differ then the one used for final counting
        # Determine the score by counting the tiles. Returns a dictionary with keys Settings.tile_1 and Settings.tile_2.
        tile_1_score = 0
        tile_2_score = 0
        all_cells = [Position(*coor) for coor in itertools.product(*[range(i) for i in Settings.dimensions])]
        for cell in all_cells:
            if board.get_value(cell) == Settings.tile_1:
                tile_1_score += 3
            if board.get_value(cell) == Settings.tile_2:
                tile_2_score += 3
        return {Settings.tile_1:tile_1_score, Settings.tile_2:tile_2_score}

    @staticmethod
    def get_point_board(board: Board) -> Dict[Any, int]:
        # Determine the score by counting the tiles. Returns a dictionary with keys Settings.tile_1 and Settings.tile_2.
        tile_1_score = 0
        tile_2_score = 0
        all_cells = [Position(*coor) for coor in itertools.product(*[range(i) for i in Settings.dimensions])]
        for cell in all_cells:
            if board.get_value(cell) == Settings.tile_1:
                tile_1_score += 1
            if board.get_value(cell) == Settings.tile_2:
                tile_2_score += 1
        return {Settings.tile_1: tile_1_score, Settings.tile_2: tile_2_score}

    @staticmethod
    def make_move(board: Board, tile: Any, position: Position) -> bool:
        # Place the tile on the board at position, and flip any of the opponent's pieces.
        # Returns False if this is an invalid move, True if it is valid.
        tiles_to_flip = Rule.get_move_result(board, tile, position)

        if len(tiles_to_flip) == 0:
            return False

        board.set_value(position, tile)
        for position in tiles_to_flip:
            board.set_value(position, tile)

        return True
