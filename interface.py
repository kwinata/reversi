from algorithm import Algorithm
from data_structs import Position
from exceptions import ExitException
from rule import Rule
from settings import Settings


class MyInput:
    args = [Settings.tile_1, "quit"]

    @staticmethod
    def getInput():
        # return input()
        return MyInput.args.pop(0)


# remove class, just use interface.py as module
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
                print('| ' + board._board_array[x][y], end=' ')
            print('| ' + str(y + 1))
            print(horizontal_line)
        print('    1   2   3   4   5   6   7   8')
        print()

    @staticmethod
    def get_player_tile():
        tile = ''
        while not (tile == Settings.tile_1 or tile == Settings.tile_2):
            print('Do you want to be %s or %s?' % (Settings.tile_1, Settings.tile_2))
            tile = MyInput.getInput().upper()

        if tile == Settings.tile_1:
            return [Settings.tile_1, Settings.tile_2]
        else:
            return [Settings.tile_2, Settings.tile_1]

    @staticmethod
    def get_first_turn():
        turn = 'player'
        print('The ' + turn + ' will go first.')
        return turn

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
                raise ExitException
            if move == 'hints':
                # Manager.switch_hints()
                return

            if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if Rule.is_valid_move(board, playerTile, Position(x, y)) == False:
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

        possibleMoves = Rule.get_valid_moves(board, computerTile)

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
            score = Algorithm.alpha_beta(board, 5, -1e9, 1e9, computerTile, computerTile) # get the state of the best minimax board
            score += Algorithm.score_table[x][y] # add with the cost of the move

            if score > bestScore:
                bestMove = [x, y]
                bestScore = score

        return bestMove

    @staticmethod
    def show_points(playerTile, computerTile, mainBoard):
        # Prints out the current score.
        scores = Rule.get_point_board(mainBoard)
        print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))




