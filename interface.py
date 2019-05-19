from reversi import Board

tile_1 = '#'
tile_2 = '.'
tile_hint = '?'


class MyInput:
    args = [tile_1, "quit"]

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
        while not (tile == tile_1 or tile == tile_2):
            print('Do you want to be %s or %s?' % (tile_1, tile_2))
            tile = MyInput.getInput().upper()

        # the first element in the tuple is the player's tile, the second is the computer's tile.
        if tile == tile_1:
            return [tile_1, tile_2]
        else:
            return [tile_2, tile_1]

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
        scores = mainBoard.getPointBoard()
        print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))

    @staticmethod
    def main():
        print('Welcome to Reversi!')

        while True:
            # Reset the board and game.
            mainBoard = Board()
            mainBoard.reset_board()
            Interface.mainBoard = mainBoard
            playerTile, computerTile = Interface.enterPlayerTile()
            showHints = False
            turn = Interface.whoGoesFirst()
            print('The ' + turn + ' will go first.')

            while True:
                if turn == 'player':
                    # Player's turn.
                    if showHints:
                        validMovesBoard = mainBoard.get_board_with_hints(playerTile)
                        Interface.draw_board(validMovesBoard)
                    else:
                        Interface.draw_board(mainBoard)
                    if mainBoard.getValidMoves(playerTile) == []:
                        print("No valid moves\n")
                    else:
                        Interface.show_points(playerTile, computerTile, mainBoard)
                        move = Interface.getPlayerMove(mainBoard, playerTile)
                        if move == 'quit':
                            print('Thanks for playing!')
                            # sys.exit()  # terminate the program
                            return
                        elif move == 'hints':
                            showHints = not showHints
                            continue
                        else:
                            mainBoard.makeMove(playerTile, move[0], move[1])
                    turn = 'computer'

                else:
                    # Computer's turn.
                    Interface.draw_board(mainBoard)
                    if mainBoard.getValidMoves(computerTile) == []:
                        if mainBoard.getValidMoves(playerTile) == []:
                            print("Game ends: No move possible")
                            break
                        print("No valid move\n")
                    else:
                        Interface.show_points(playerTile, computerTile, mainBoard)
                        print("I'm thinking...")
                        x, y = Interface.getComputerMove(mainBoard, computerTile)
                        mainBoard.makeMove(computerTile, x, y)
                        print("My move: ", x + 1, y + 1)
                    turn = 'player'

            # Display the final score.
            Interface.draw_board(mainBoard)
            scores = mainBoard.getPointBoard()
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


        possibleMoves = board.getValidMoves(tile)

        # check for terminal node
        if depth == 0 or possibleMoves == []:
            return board.getScoreOfBoard()[computerTile]

        # get the player tile
        oppTile = "X"
        oppTile = "X"
        if(tile=="X"):
            oppTile = "O"

        if tile==computerTile: #if maximizing
            v = -1e9

            for x, y in possibleMoves:

                # get the alphabeta of child
                child = board.getBoardCopy()
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
                child = board.getBoardCopy()
                Board.makeMove(child, tile, x, y)
                v = Algorithm.alphabeta(child, depth-1, alpha, beta, computerTile, oppTile)
                v -= Algorithm.scoretable[x][y]

                beta = min(beta, v)

                if beta<=alpha:
                    break
            return v

Interface.main()


