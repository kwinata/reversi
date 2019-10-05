import itertools

from data_structs import Position, Vector
from settings import Settings


class Rule:
    @staticmethod
    def get_tiles_to_flip_for_move(board, position, tile):
        if tile == Settings.tile_1:
            other_tile = Settings.tile_2
        else:
            other_tile = Settings.tile_1

        start_loc = position

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
            while current_loc.is_on_board() and board._board_array[current_loc.get_coordinate(0)][current_loc.get_coordinate(1)] == other_tile:
                current_loc.offset(direction)
            if not current_loc.is_on_board():
                continue
            if board._board_array[current_loc.get_coordinate(0)][current_loc.get_coordinate(1)] == tile:
                current_loc.offset(direction, reverse=True)
                while current_loc != start_loc:
                    tiles_to_flip.append([current_loc.get_coordinate(0), current_loc.get_coordinate(1)])
                    current_loc.offset(direction, reverse=True)
        return tiles_to_flip

    @staticmethod
    def get_move_result(board, tile, xstart, ystart):
        if not board.is_empty_and_on_board(Position(xstart, ystart)):
            return False

        position = Position(xstart, ystart)
        tiles_to_flip = Rule.get_tiles_to_flip_for_move(board, position, tile)

        if len(tiles_to_flip) == 0:
            return False
        return tiles_to_flip

    @staticmethod
    def is_valid_move(self, tile, xstart, ystart):
        if Rule.get_move_result(self, tile, xstart, ystart):
            return True
        return False

    @staticmethod
    def get_board_with_hints(board, tile):
        new_board_for_printing_only = board.duplicate_board()

        for x, y in Rule.get_valid_moves(board, tile):
            new_board_for_printing_only.board[x][y] = Settings.tile_hint

        return new_board_for_printing_only

    @staticmethod
    def get_valid_moves(self, tile):
        # Returns a list of [x,y] lists of valid moves for the given player on the given board.
        validMoves = []

        for x in range(8):
            for y in range(8):
                if Rule.is_valid_move(self, tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves

    @staticmethod
    def getScoreOfBoard(self):
        # Determine the score by counting the tiles. Returns a dictionary with keys Settings.tile_1 and Settings.tile_2.
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if self._board_array[x][y] == Settings.tile_1:
                    xscore += 3
                if self._board_array[x][y] == Settings.tile_2:
                    oscore += 3
        return {Settings.tile_1:xscore, Settings.tile_2:oscore}

    @staticmethod
    def getPointBoard(board):
        # Determine the score by counting the tiles. Returns a dictionary with keys Settings.tile_1 and Settings.tile_2.
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if board._board_array[x][y] == Settings.tile_1:
                    xscore += 1
                if board._board_array[x][y] == Settings.tile_2:
                    oscore += 1
        return {Settings.tile_1:xscore, Settings.tile_2:oscore}

    @staticmethod
    def makeMove(self, tile, xstart, ystart):
        # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
        # Returns False if this is an invalid move, True if it is valid.
        tiles_to_flip = Rule.get_move_result(self, tile, xstart, ystart)

        if tiles_to_flip == False:
            return False

        self._board_array[xstart][ystart] = tile
        for x, y in tiles_to_flip:
            self._board_array[x][y] = tile
        return True