import copy
import random
import sys


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
    @staticmethod
    def draw_board(board):
        horizontal_line = '  ---------------------------------'

        print()
        print('    1   2   3   4   5   6   7   8')
        print(horizontal_line)
        for y in range(8):
            print(y + 1, end=' ')
            for x in range(8):
                print('| ' + board[x][y], end=' ')
            print('| ' + str(y + 1))
            print(horizontal_line)
        print('    1   2   3   4   5   6   7   8')
        print()

    @staticmethod
    def reset_board(board):
        for x in range(8):
            for y in range(8):
                board[x][y] = ' '

        # Starting pieces
        board[3][3] = tile_1
        board[3][4] = tile_2
        board[4][3] = tile_2
        board[4][4] = tile_1

    @staticmethod
    def get_blank_board():
        board = []

        for i in range(8):
            board.append([' '] * 8)

        return board

    @staticmethod
    def check_valid_location(board, x, y):
        if board[x][y] != ' ' or not Location(x, y).is_on_board():
            raise InvalidLocationException()

    @staticmethod
    def get_tiles_to_flip_for_move(board, xstart, ystart, tile):
        if tile == tile_1:
            other_tile = tile_2
        else:
            other_tile = tile_1

        start_loc = Location(xstart, ystart)

        tiles_to_flip = []
        for direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            current_loc = start_loc.copy()
            current_loc.offset(direction)
            while current_loc.is_on_board() and board[current_loc.x][current_loc.y] == other_tile:
                current_loc.offset(direction)
            if not current_loc.is_on_board():
                continue
            if board[current_loc.x][current_loc.y] == tile:
                current_loc.offset(direction, reverse=True)
                while current_loc != start_loc:
                    tiles_to_flip.append([current_loc.x, current_loc.y])
                    current_loc.offset(direction, reverse=True)
        return tiles_to_flip

    @staticmethod
    def get_move_result(board, tile, xstart, ystart):
        # Returns False if the player's move on space xstart, ystart is invalid.
        # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.

        try:
            Board.check_valid_location(board, xstart, ystart)
        except:
            return False

        tiles_to_flip = Board.get_tiles_to_flip_for_move(board, xstart, ystart, tile)

        if len(tiles_to_flip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        return tiles_to_flip

    @staticmethod
    def is_valid_move(board, tile, xstart, ystart):
        if Board.get_move_result(board, tile, xstart, ystart):
            return True
        return False



    @staticmethod
    def get_board_with_hints(board, tile):
        new_board_for_printing_only = Board.getBoardCopy(board)

        for x, y in Board.getValidMoves(new_board_for_printing_only, tile):
            new_board_for_printing_only[x][y] = tile_hint

        return new_board_for_printing_only

    @staticmethod
    def getValidMoves(board, tile):
        # Returns a list of [x,y] lists of valid moves for the given player on the given board.
        validMoves = []

        for x in range(8):
            for y in range(8):
                if Board.is_valid_move(board, tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves


    @staticmethod
    def getScoreOfBoard(board):
        # Determine the score by counting the tiles. Returns a dictionary with keys tile_1 and tile_2.
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == tile_1:
                    xscore += 3
                if board[x][y] == tile_2:
                    oscore += 3
        return {tile_1:xscore, tile_2:oscore}

    @staticmethod
    def getPointBoard(board):
        # Determine the score by counting the tiles. Returns a dictionary with keys tile_1 and tile_2.
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == tile_1:
                    xscore += 1
                if board[x][y] == tile_2:
                    oscore += 1
        return {tile_1:xscore, tile_2:oscore}

    @staticmethod
    def makeMove(board, tile, xstart, ystart):
        # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
        # Returns False if this is an invalid move, True if it is valid.
        tiles_to_flip = Board.get_move_result(board, tile, xstart, ystart)

        if tiles_to_flip == False:
            return False

        board[xstart][ystart] = tile
        for x, y in tiles_to_flip:
            board[x][y] = tile
        return True

    @staticmethod
    def getBoardCopy(board):
        # Make a duplicate of the board list and return the duplicate.
        dupeBoard = Board.get_blank_board()

        for x in range(8):
            for y in range(8):
                dupeBoard[x][y] = board[x][y]

        return dupeBoard


class Interface:
    @staticmethod
    def enterPlayerTile():
        # Lets the player type which tile they want to be.
        # Returns a list with the player's tile as the first item, and the computer's tile as the second.
        tile = ''
        while not (tile == tile_1 or tile == tile_2):
            print('Do you want to be %s or %s?' % (tile_1, tile_2))
            tile = input().upper()

        # the first element in the tuple is the player's tile, the second is the computer's tile.
        if tile == tile_1:
            return [tile_1, tile_2]
        else:
            return [tile_2, tile_1]

    @staticmethod
    def whoGoesFirst():
        # Randomly choose the player who goes first.
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'player'

    @staticmethod
    def playAgain():
        # This function returns True if the player wants to play again, otherwise it returns False.
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')


    @staticmethod
    def getPlayerMove(board, playerTile):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
        while True:
            print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
            move = input().lower()
            if move == 'quit':
                return 'quit'
            if move == 'hints':
                return 'hints'

            if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if Board.is_valid_move(board, playerTile, x, y) == False:
                    continue
                else:
                    break
            else:
                print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
                print('For example, 81 will be the top-right corner.')

        return [x, y]

    @staticmethod
    def getComputerMove(board, computerTile):
        # Given a board and the computer's tile, determine where to
        # move and return that move as a [x, y] list.

        possibleMoves = Board.getValidMoves(board, computerTile)

        # randomize the order of the possible moves
        random.shuffle(possibleMoves)

        # get the player tile (=oppTile)
        if(computerTile==tile_1):
            oppTile=tile_2
        else:
            oppTile=tile_1

        # Go through all the possible moves and remember the best scoring move
        bestScore = -1e5

        #to avoid bestMove referenced in the return function call before it is initialized
        try:
            bestMove = possibleMoves[0]
        except:
            bestMove = None

        for x, y in possibleMoves:

            print("considering ", x+1, y+1) # ux
            score = Algorithm.alphabeta(board, 5, -1e9, 1e9, computerTile, computerTile) # get the state of the best minimax board
            score += Algorithm.scoretable[x][y] # add with the cost of the move

            if score > bestScore:
                bestMove = [x, y]
                bestScore = score

        return bestMove

    @staticmethod
    def show_points(playerTile, computerTile, mainBoard):
        # Prints out the current score.
        scores = Board.getPointBoard(mainBoard)
        print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))

    @staticmethod
    def main():
        print('Welcome to Reversi!')

        while True:
            # Reset the board and game.
            mainBoard = Board.get_blank_board()
            Board.reset_board(mainBoard)
            playerTile, computerTile = Interface.enterPlayerTile()
            showHints = False
            turn = Interface.whoGoesFirst()
            print('The ' + turn + ' will go first.')

            while True:
                if turn == 'player':
                    # Player's turn.
                    if showHints:
                        validMovesBoard = Board.get_board_with_hints(mainBoard, playerTile)
                        Board.draw_board(validMovesBoard)
                    else:
                        Board.draw_board(mainBoard)
                    if Board.getValidMoves(mainBoard, playerTile) == []:
                        print("No valid moves\n")
                    else:
                        Interface.show_points(playerTile, computerTile, mainBoard)
                        move = Interface.getPlayerMove(mainBoard, playerTile)
                        if move == 'quit':
                            print('Thanks for playing!')
                            sys.exit()  # terminate the program
                        elif move == 'hints':
                            showHints = not showHints
                            continue
                        else:
                            Board.makeMove(mainBoard, playerTile, move[0], move[1])
                    turn = 'computer'

                else:
                    # Computer's turn.
                    Board.draw_board(mainBoard)
                    if Board.getValidMoves(mainBoard, computerTile) == []:
                        if Board.getValidMoves(mainBoard, playerTile) == []:
                            print("Game ends: No move possible")
                            break
                        print("No valid move\n")
                    else:
                        Interface.show_points(playerTile, computerTile, mainBoard)
                        print("I'm thinking...")
                        x, y = Interface.getComputerMove(mainBoard, computerTile)
                        Board.makeMove(mainBoard, computerTile, x, y)
                        print("My move: ", x + 1, y + 1)
                    turn = 'player'

            # Display the final score.
            Board.draw_board(mainBoard)
            scores = Board.getPointBoard(mainBoard)
            print('%s scored %s points. %s scored %s points.' % (tile_1, scores[tile_1], tile_2, scores[tile_2]))
            if scores[playerTile] > scores[computerTile]:
                print('You beat the computer by %s points! Congratulations!' % (
                            scores[playerTile] - scores[computerTile]))
            elif scores[playerTile] < scores[computerTile]:
                print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
            else:
                print('The game was a tie!')

            if not Interface.playAgain():
                break


class Algorithm:
    scoretable = [
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
    def alphabeta(board, depth, alpha, beta ,computerTile, tile):
        # implementation of alphabeta pruning


        possibleMoves = Board.getValidMoves(board, tile)

        # check for terminal node
        if depth == 0 or possibleMoves == []:
            return Board.getScoreOfBoard(board)[computerTile]

        # get the player tile
        oppTile = "X"
        oppTile = "X"
        if(tile=="X"):
            oppTile = "O"

        if tile==computerTile: #if maximizing
            v = -1e9

            for x, y in possibleMoves:

                # get the alphabeta of child
                child = Board.getBoardCopy(board)
                Board.makeMove(child, tile, x, y)
                v = Algorithm.alphabeta(child, depth-1, alpha, beta, computerTile, oppTile)
                v += Algorithm.scoretable[x][y]

                alpha = max(alpha, v)

                if beta<=alpha:
                    break
            return v
        else:  # if minimizing
            v = 1e9

            for x, y in possibleMoves:

                # get the alphabeta of child
                child = Board.getBoardCopy(board)
                Board.makeMove(child, tile, x, y)
                v = Algorithm.alphabeta(child, depth-1, alpha, beta, computerTile, oppTile)
                v -= Algorithm.scoretable[x][y]

                beta = min(beta, v)

                if beta<=alpha:
                    break
            return v

Interface.main()



