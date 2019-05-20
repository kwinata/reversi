from reversi import Board


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