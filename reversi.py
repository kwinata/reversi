import copy

tile_1 = '#'
tile_2 = '.'
tile_hint = '?'


class ReversiException(Exception):
    pass


class InvalidLocationException(ReversiException):
    def __str__(self):
        return self.__name__


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
    board = None

    def draw_board(self):
        horizontal_line = '  ---------------------------------'

        print()
        print('    1   2   3   4   5   6   7   8')
        print(horizontal_line)
        for y in range(8):
            print(y + 1, end=' ')
            for x in range(8):
                print('| ' + self.board[x][y], end=' ')
            print('| ' + str(y + 1))
            print(horizontal_line)
        print('    1   2   3   4   5   6   7   8')
        print()

    def reset_board(self):
        for x in range(8):
            for y in range(8):
                self.board[x][y] = ' '

        # Starting pieces
        self.board[3][3] = tile_1
        self.board[3][4] = tile_2
        self.board[4][3] = tile_2
        self.board[4][4] = tile_1

    @staticmethod
    def get_blank_board():
        board_content = []

        for i in range(8):
            board_content.append([' '] * 8)

        board = Board()
        board.board = board_content

        return board

    def check_valid_location(self, x, y):
        if self.board[x][y] != ' ' or not Location(x, y).is_on_board():
            raise InvalidLocationException()

    def get_tiles_to_flip_for_move(self, xstart, ystart, tile):
        if tile == tile_1:
            other_tile = tile_2
        else:
            other_tile = tile_1

        start_loc = Location(xstart, ystart)

        tiles_to_flip = []
        for direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            current_loc = start_loc.copy()
            current_loc.offset(direction)
            while current_loc.is_on_board() and self.board[current_loc.x][current_loc.y] == other_tile:
                current_loc.offset(direction)
            if not current_loc.is_on_board():
                continue
            if self.board[current_loc.x][current_loc.y] == tile:
                current_loc.offset(direction, reverse=True)
                while current_loc != start_loc:
                    tiles_to_flip.append([current_loc.x, current_loc.y])
                    current_loc.offset(direction, reverse=True)
        return tiles_to_flip

    def get_move_result(self, tile, xstart, ystart):
        # Returns False if the player's move on space xstart, ystart is invalid.
        # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.

        try:
            self.check_valid_location(xstart, ystart)
        except:
            return False

        tiles_to_flip = self.get_tiles_to_flip_for_move(xstart, ystart, tile)

        if len(tiles_to_flip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        return tiles_to_flip

    def is_valid_move(self, tile, xstart, ystart):
        if self.get_move_result(tile, xstart, ystart):
            return True
        return False



    def get_board_with_hints(self, tile):
        new_board_for_printing_only = self.getBoardCopy()

        for x, y in self.getValidMoves(tile):
            new_board_for_printing_only.board[x][y] = tile_hint

        return new_board_for_printing_only

    def getValidMoves(self, tile):
        # Returns a list of [x,y] lists of valid moves for the given player on the given board.
        validMoves = []

        for x in range(8):
            for y in range(8):
                if self.is_valid_move(tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves


    def getScoreOfBoard(self):
        # Determine the score by counting the tiles. Returns a dictionary with keys tile_1 and tile_2.
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == tile_1:
                    xscore += 3
                if self.board[x][y] == tile_2:
                    oscore += 3
        return {tile_1:xscore, tile_2:oscore}

    def getPointBoard(self):
        # Determine the score by counting the tiles. Returns a dictionary with keys tile_1 and tile_2.
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == tile_1:
                    xscore += 1
                if self.board[x][y] == tile_2:
                    oscore += 1
        return {tile_1:xscore, tile_2:oscore}


    def makeMove(self, tile, xstart, ystart):
        # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
        # Returns False if this is an invalid move, True if it is valid.
        tiles_to_flip = self.get_move_result(tile, xstart, ystart)

        if tiles_to_flip == False:
            return False

        self.board[xstart][ystart] = tile
        for x, y in tiles_to_flip:
            self.board[x][y] = tile
        return True

    def getBoardCopy(self):
        # Make a duplicate of the board list and return the duplicate.
        board = Board()
        board.board = copy.deepcopy(self.board)
        return board



