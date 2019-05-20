from algorithm import Algorithm
from data_structs import Board
from settings import Settings


class MyInput:
    args = [Settings.tile_1, "quit"]

    @staticmethod
    def getInput():
        # return input()
        return MyInput.args.pop(0)


class Interface:
    mainBoard = None

    @staticmethod
    def draw_board(board):
        horizontal_line = '  ---------------------------------'

        print()
        print('    1   2   3   4   5   6   7   8')
        print(horizontal_line)
        for y in range(8):
            print(y + 1, end=' ')
            for x in range(8):
                print('| ' + board.board[x][y], end=' ')
            print('| ' + str(y + 1))
            print(horizontal_line)
        print('    1   2   3   4   5   6   7   8')
        print()

    @staticmethod
    def enterPlayerTile():
        # Lets the player type which tile they want to be.
        # Returns a list with the player's tile as the first item, and the computer's tile as the second.
        tile = ''
        while not (tile == Settings.tile_1 or tile == Settings.tile_2):
            print('Do you want to be %s or %s?' % (Settings.tile_1, Settings.tile_2))
            tile = MyInput.getInput().upper()

        # the first element in the tuple is the player's tile, the second is the computer's tile.
        if tile == Settings.tile_1:
            return [Settings.tile_1, Settings.tile_2]
        else:
            return [Settings.tile_2, Settings.tile_1]

    @staticmethod
    def whoGoesFirst():
        return 'player'

    @staticmethod
    def playAgain():
        # This function returns True if the player wants to play again, otherwise it returns False.
        print('Do you want to play again? (yes or no)')
        return MyInput.getInput().lower().startswith('y')


    @staticmethod
    def getPlayerMove(board, playerTile):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
        while True:
            print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
            move = MyInput.getInput().lower()
            if move == 'quit':
                return 'quit'
            if move == 'hints':
                return 'hints'

            if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(playerTile, x, y) == False:
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

        possibleMoves = board.getValidMoves(computerTile)

        # get the player tile (=oppTile)
        if(computerTile==Settings.tile_1):
            oppTile=Settings.tile_2
        else:
            oppTile=Settings.tile_1

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
        scores = mainBoard.getPointBoard()
        print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))




