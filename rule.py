from data_structs import Location
from exceptions import InvalidLocationException
from settings import Settings


class Rule:
    @staticmethod
    def get_tiles_to_flip_for_move(board, xstart, ystart, tile):
        if tile == Settings.tile_1:
            other_tile = Settings.tile_2
        else:
            other_tile = Settings.tile_1

        start_loc = Location(xstart, ystart)

        tiles_to_flip = []
        for direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            current_loc = start_loc.copy()
            current_loc.offset(direction)
            while current_loc.is_on_board() and board._board_array[current_loc.x][current_loc.y] == other_tile:
                current_loc.offset(direction)
            if not current_loc.is_on_board():
                continue
            if board._board_array[current_loc.x][current_loc.y] == tile:
                current_loc.offset(direction, reverse=True)
                while current_loc != start_loc:
                    tiles_to_flip.append([current_loc.x, current_loc.y])
                    current_loc.offset(direction, reverse=True)
        return tiles_to_flip

    @staticmethod
    def get_move_result(board, tile, xstart, ystart):
        if not board.is_empty_and_on_board(Location(xstart, ystart)):
            return False

        tiles_to_flip = Rule.get_tiles_to_flip_for_move(board, xstart, ystart, tile)

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