from interface import Interface
from data_structs import Board
from settings import Settings


class Manager:

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
            print('%s scored %s points. %s scored %s points.' % (Settings.tile_1, scores[Settings.tile_1], Settings.tile_2, scores[Settings.tile_2]))
            if scores[playerTile] > scores[computerTile]:
                print('You beat the computer by %s points! Congratulations!' % (
                        scores[playerTile] - scores[computerTile]))
            elif scores[playerTile] < scores[computerTile]:
                print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
            else:
                print('The game was a tie!')

            if not Interface.playAgain():

                break

Manager.main()
