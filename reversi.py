import random
import sys


tile_1 = '#'
tile_2 = '.'
tile_hint = '?'


def draw_board(board):
    horizontal_line = '  ---------------------------------'

    print()
    print('    1   2   3   4   5   6   7   8')
    print(horizontal_line)
    for y in range(8):
        print(y+1, end=' ')
        for x in range(8):
            print('| ' + board[x][y], end=' ')
        print('| ' + str(y+1))
        print(horizontal_line)
    print('    1   2   3   4   5   6   7   8')
    print()


def reset_board(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Starting pieces
    board[3][3] = tile_1
    board[3][4] = tile_2
    board[4][3] = tile_2
    board[4][4] = tile_1


def get_blank_board():
    board = []

    for i in range(8):
        board.append([' '] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not is_on_board(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == tile_1:
        otherTile = tile_2
    else:
        otherTile = tile_1

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if is_on_board(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not is_on_board(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not is_on_board(x, y): # break out of while loop, then continue in for loop
                    break
            if not is_on_board(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' ' # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip


def is_on_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = tile_hint
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

# create a table of score for each move in corresponding location
scoretable=[]
scoretable.append([99, -8, 8, 6, 6, 8, -8, 99])
scoretable.append([-8, -24, -4, -3, -3, -4, -24, -8])
scoretable.append([8, -4, 7, 4, 4, 7, -4, 8])
scoretable.append([6, -3, 4, 0, 0, 4, -3, 6])
scoretable.append([6, -3, 4, 0, 0, 4, -3, 6])
scoretable.append([8, -4, 7, 4, 4, 7, -4, 8])
scoretable.append([-8, -24, -4, -3, -3, -4, -24, -8])
scoretable.append([99, -8, 8, 6, 6, 8, -8, 99])

def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys tile_1 and tile_2.
    global scoretable
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == tile_1:
                xscore += 3
            if board[x][y] == tile_2:
                oscore += 3
    return {tile_1:xscore, tile_2:oscore}

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


def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = get_blank_board()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


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
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')

    return [x, y]


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.

    global scoretable

    possibleMoves = getValidMoves(board, computerTile)

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
        bestMove=None

    for x, y in possibleMoves:

        print("considering ", x+1, y+1) # ux
        score = alphabeta(board, 5, -1e9, 1e9, computerTile, computerTile) # get the state of the best minimax board
        score += scoretable[x][y] # add with the cost of the move

        if score > bestScore:
            bestMove = [x, y]
            bestScore = score

    return bestMove

def alphabeta(board, depth, alpha, beta ,computerTile, tile):
    # implementation of alphabeta pruning

    global scoretable

    possibleMoves = getValidMoves(board, tile)

    # check for terminal node
    if depth == 0 or possibleMoves == []:
        return getScoreOfBoard(board)[computerTile]

    # get the player tile
    oppTile = "X"
    if(tile=="X"):
        oppTile = "O"

    if tile==computerTile: #if maximizing
        v = -1e9

        for x, y in possibleMoves:

            # get the alphabeta of child
            child = getBoardCopy(board)
            makeMove(child, tile, x, y)
            v = alphabeta(child, depth-1, alpha, beta, computerTile, oppTile)
            v += scoretable[x][y]

            alpha = max(alpha, v)

            if beta<=alpha:
                break
        return v
    else: # if minimizing
        v = 1e9

        for x, y in possibleMoves:

            # get the alphabeta of child
            child = getBoardCopy(board)
            makeMove(child, tile, x, y)
            v = alphabeta(child, depth-1, alpha, beta, computerTile, oppTile)
            v -= scoretable[x][y]

            beta = min(beta, v)

            if beta<=alpha:
                break
        return v

def showPoints(playerTile, computerTile):
    # Prints out the current score.
    scores = getPointBoard(mainBoard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))



print('Welcome to Reversi!')

while True:
    # Reset the board and game.
    mainBoard = get_blank_board()
    reset_board(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    while True:
        if turn == 'player':
            # Player's turn.
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                draw_board(validMovesBoard)
            else:
                draw_board(mainBoard)
            if getValidMoves(mainBoard, playerTile) == []:
                print("No valid moves\n")
            else:
                showPoints(playerTile, computerTile)
                move = getPlayerMove(mainBoard, playerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit() # terminate the program
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(mainBoard, playerTile, move[0], move[1])
            turn = 'computer'

        else:
            # Computer's turn.
            draw_board(mainBoard)
            if getValidMoves(mainBoard, computerTile) == []:
                if getValidMoves(mainBoard, playerTile) == []:
                    print("Game ends: No move possible")
                    break
                print("No valid move\n")
            else:
                showPoints(playerTile, computerTile)
                print("I'm thinking...")
                x, y = getComputerMove(mainBoard, computerTile)
                makeMove(mainBoard, computerTile, x, y)
                print("My move: ", x+1, y+1)
            turn = 'player'

    # Display the final score.
    draw_board(mainBoard)
    scores = getPointBoard(mainBoard)
    print('%s scored %s points. %s scored %s points.' % (tile_1, scores[tile_1], tile_2, scores[tile_2]))
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')

    if not playAgain():
        break
