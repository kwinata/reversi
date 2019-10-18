from typing import Any

from data_structs import Position, Board
from rule import Rule
from settings import Settings


class Algorithm:
    score_table = [
            [99, -8, 8, 6, 6, 8, -8, 99],
            [-8, -24, -4, -3, -3, -4, -24, -8],
            [8, -4, 7, 4, 4, 7, -4, 8],
            [6, -3, 4, 0, 0, 4, -3, 6],
            [6, -3, 4, 0, 0, 4, -3, 6],
            [8, -4, 7, 4, 4, 7, -4, 8],
            [-8, -24, -4, -3, -3, -4, -24, -8],
            [99, -8, 8, 6, 6, 8, -8, 99],
        ]

    @staticmethod
    def alpha_beta(board: Board, depth_left: int, alpha: int, beta: int, computer_tile: Any,
                   current_level_tile: Any) -> int:
        # implementation of alpha_beta pruning

        possible_moves = Rule.get_valid_moves(board, current_level_tile)

        # check for terminal node
        # TODO: when it's just skip (no possible_moves), it's not terminal, it's terminal only when both sides stalled
        if depth_left == 0 or possible_moves == []:
            return Rule.get_score_of_board(board)[computer_tile]

        possible_tile = [Settings.tile_1, Settings.tile_2]
        possible_tile.remove(current_level_tile)
        next_level_tile = possible_tile.pop(0)

        if current_level_tile == computer_tile:  # maximizing level (try to get max score)
            max_value = -1e9

            for x, y in possible_moves:

                # get the alpha_beta of child
                child = board.duplicate_board()
                Rule.make_move(child, current_level_tile, Position(x, y))
                max_value = Algorithm.alpha_beta(child, depth_left - 1, alpha, beta, computer_tile, next_level_tile)
                max_value += Algorithm.score_table[x][y]  # TODO: This does not make sense to put, remove after changing test cases

                alpha = max(alpha, max_value)

                if beta <= alpha:
                    break
            return max_value
        else:  # minimizing level (i know you, human, will choose lower score for me)
            min_value = 1e9

            for x, y in possible_moves:

                # get the alpha_beta of child
                # TODO: convert to function
                child = board.duplicate_board()
                Rule.make_move(child, current_level_tile, Position(x, y))
                min_value = Algorithm.alpha_beta(child, depth_left - 1, alpha, beta, computer_tile, next_level_tile)
                min_value -= Algorithm.score_table[x][y]

                beta = min(beta, min_value)

                if beta <= alpha:
                    break
            return min_value
