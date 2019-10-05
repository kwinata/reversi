from data_structs import Board, Position
from interface import Interface
from rule import Rule
from settings import Settings


class Manager:
    board = None
    turn = None
    show_hints = None
    player_tile = None
    computer_tile = None

    @staticmethod
    def initialize():
        Manager.board = Board()
        Manager.board.reset_board()

    @staticmethod
    def get_tiles_config():
        Manager.player_tile, Manager.computer_tile = Interface.get_player_tile()
        Manager.turn = Interface.get_first_turn()
        Manager.show_hints = False

    @staticmethod
    def draw_board():
        if Manager.show_hints:
            Interface.draw_board(Rule.get_board_with_hints(Manager.board, Manager.player_tile))
        else:
            Interface.draw_board(Manager.board)

    @staticmethod
    def change_turn():
        if Manager.turn == 'player':
            Manager.turn = 'computer'
        else:
            Manager.turn = 'player'

    @staticmethod
    def switch_hints():
        Manager.show_hints = not Manager.show_hints
        
    @staticmethod
    def main():
        print('Welcome to Reversi!')

        while True:
            Manager.initialize()
            Manager.get_tiles_config()

            while True:
                if Manager.turn == 'player':
                    Manager.draw_board()

                    if not Rule.get_valid_moves(Manager.board, Manager.player_tile):
                        print("No valid moves\n")
                    else:
                        move = Interface.getPlayerMove(Manager.board, Manager.player_tile)
                        Rule.make_move(Manager.board, Manager.player_tile, Position(move[0], move[1]))

                    Interface.show_points(Manager.player_tile, Manager.computer_tile, Manager.board)
                    Manager.change_turn()

                else:
                    Manager.draw_board()

                    if not Rule.get_valid_moves(Manager.board, Manager.computer_tile):
                        if not Rule.get_valid_moves(Manager.board, Manager.player_tile):
                            print("Game ends: No move possible")
                            break
                        print("No valid move\n")
                    else:
                        print("I'm thinking...")
                        x, y = Interface.getComputerMove(Manager.board, Manager.computer_tile)
                        Rule.make_move(Manager.board, Manager.computer_tile, Position(x, y))
                        print("My move: ", x + 1, y + 1)

                    Interface.show_points(Manager.player_tile, Manager.computer_tile, Manager.board)
                    Manager.change_turn()


            # Display the final score.
            Interface.draw_board(Manager.board)
            scores = Rule.get_point_board(Manager.board)
            print('%s scored %s points. %s scored %s points.' % (Settings.tile_1, scores[Settings.tile_1], Settings.tile_2, scores[Settings.tile_2]))
            if scores[Manager.player_tile] > scores[Manager.computer_tile]:
                print('You beat the computer by %s points! Congratulations!' % (
                        scores[Manager.player_tile] - scores[Manager.computer_tile]))
            elif scores[Manager.player_tile] < scores[Manager.computer_tile]:
                print('You lost. The computer beat you by %s points.' % (scores[computer_tile] - scores[player_tile]))
            else:
                print('The game was a tie!')

            if not Interface.playAgain():

                break
