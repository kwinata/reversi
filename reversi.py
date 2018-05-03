# Reversi

import random
import sys

# Copy from match.py
# input
depth = 2

def getComputerMove(board, computerTile, scoretables):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.

    global depth

    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # get the player tile (=oppTile)
    if(computerTile=='X'):
        oppTile='O'
    else:
        oppTile='X'

    # Go through all the possible moves and remember the best scoring move
    bestScore = -1e5

    #to avoid bestMove referenced in the return function call before it is initialized
    try:
        bestMove = possibleMoves[0]
    except:
        bestMove=None

    for x, y in possibleMoves:
        #print("considering ", x+1, y+1) # ux
        score = alphabeta(board, depth, -1e9, 1e9, computerTile, computerTile, scoretables) # get the state of the best minimax board

        if score > bestScore:
            bestMove = [x, y]
            bestScore = score

    return bestMove

def alphabeta(board, depth, alpha, beta,computerTile, tile, scoretables):
    # implementation of alphabeta pruning

    possibleMoves = getValidMoves(board, tile)

    # check for terminal node
    if depth == 0 or possibleMoves == []:
        scoretable=scoretables[stagecheck(board)]
        return getScoreOfBoard(board, scoretable)[computerTile]

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
            
            # check which scoretable from scortables should be use
            # using stage analysis
            scoretable = scoretables[stagecheck(board)]
            
            v = alphabeta(child, depth-1, alpha, beta, computerTile, oppTile, scoretables)

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
            
            # check which scoretable from scortables should be use
            # using stage analysis
            scoretable = scoretables[stagecheck(board)]

            v = alphabeta(child, depth-1, alpha, beta, computerTile, oppTile, scoretables)

            beta = min(beta, v)

            if beta<=alpha:
                break
        return v

def stagecheck(board):
    flag=0
    for i in range(8):
        if board[i][0]!=' ': flag=1
        if board[i][1]!=' ': flag=1
        if board[i][6]!=' ': flag=1
        if board[i][7]!=' ': flag=1
    for i in range(0,2):
        for j in range(8):
            if board[i][j]!=' ': flag=1
    for i in range(6,8):
        for j in range(8):
            if board[i][j]!=' ': flag=1
    if flag == 0:
        if board[2][2]!=' ': flag=2
        if board[2][5]!=' ': flag=2
        if board[5][5]!=' ': flag=2
        if board[5][2]!=' ': flag=2
    elif flag == 1:
        if board[1][1]!=' ': flag=3
        if board[1][6]!=' ': flag=3
        if board[6][6]!=' ': flag=3
        if board[6][1]!=' ': flag=3
    for i in range(0,8):
        if board[0][i]!=' ': flag=4
        if board[i][0]!=' ': flag=4
        if board[7][i]!=' ': flag=4
        if board[i][7]!=' ': flag=4

    return flag

# End of copy from match.py

# copy from ga.py

def tablesFromGen(gen):
    scoretables=[]
    for i in range(len(gen)):
        tmp = gen[i]
        scoretable = []
        scoretable.append(tmp[0:4]+tmp[3::-1])
        scoretable.append(tmp[4:8]+tmp[7:3:-1])
        scoretable.append(tmp[8:12]+tmp[11:7:-1])
        scoretable.append(tmp[12:16]+tmp[15:11:-1])
        scoretable.append(tmp[12:16]+tmp[15:11:-1])
        scoretable.append(tmp[8:12]+tmp[11:7:-1])
        scoretable.append(tmp[4:8]+tmp[7:3:-1])
        scoretable.append(tmp[0:4]+tmp[3::-1])
        scoretables.append(scoretable)
    return scoretables

# end of copy from ga.py


def drawBoard(board):
    # This function prints out the board that it was passed. Returns None.
    HLINE = '  +-----+-----+-----+-----+-----+-----+-----+-----+'
    VLINE = '  |     |     |     |     |     |     |     |     |'

    print('     1     2     3     4     5     6     7     8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('|  %s ' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)


def resetBoard(board):
    # Blanks out the board it is passed, except for the original starting position.
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([' '] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
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


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <=7


def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board,scoretable):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += scoretable[x][y]
                oscore -= scoretable[x][y]
            if board[x][y] == 'O':
                oscore += scoretable[x][y]
                xscore += scoretable[x][y]
    return {'X':xscore, 'O':oscore}

def getPointBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}


def enterPlayerTile():
    # Lets the player type which tile they want to be.
    # Returns a list with the player's tile as the first item, and the computer's tile as the second.
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    # the first element in the tuple is the player's tile, the second is the computer's tile.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


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
    dupeBoard = getNewBoard()

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


def showPoints(playerTile, computerTile, board):
    # Prints out the current score.
    scores = getPointBoard(board)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))


def play():
    print('Welcome to Reversi!')
    
    import csv
    with open('try.csv', newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        out = []
        for row in spamreader:
            out.append(row)
        spamreader = out
        
        for i in range(40):
            for j in range(8):
                out[i][j] = int(out[i][j])
                
        scoretables = []
        scoretables.append(spamreader[0:8])
        scoretables.append(spamreader[8:16])
        scoretables.append(spamreader[16:24])
        scoretables.append(spamreader[24:32])
        scoretables.append(spamreader[32:40])
    

    while True:
        # Reset the board and game.
        mainBoard = getNewBoard()
        resetBoard(mainBoard)
        playerTile, computerTile = enterPlayerTile()
        showHints = False
        turn = whoGoesFirst()
        print('The ' + turn + ' will go first.')

        while True:
            if turn == 'player':
                # Player's turn.
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(mainBoard)
                if getValidMoves(mainBoard, playerTile) == []:
                    print("No valid moves\n")
                else:
                    showPoints(playerTile, computerTile, mainBoard)
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
                drawBoard(mainBoard)
                if getValidMoves(mainBoard, computerTile) == []:
                    if getValidMoves(mainBoard, playerTile) == []:
                        print("Game ends: No move possible")
                        break
                    print("No valid move\n")
                else:
                    showPoints(playerTile, computerTile, mainBoard)
                    print("I'm thinking...")
                    x, y = getComputerMove(mainBoard, computerTile,scoretables)
                    makeMove(mainBoard, computerTile, x, y)
                    print("My move: ", x+1, y+1)
                turn = 'player'
    
        # Display the final score.
        drawBoard(mainBoard)
        scores = getPointBoard(mainBoard)
        print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
        if scores[playerTile] > scores[computerTile]:
            print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
        elif scores[playerTile] < scores[computerTile]:
            print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
        else:
            print('The game was a tie!')
    
        if not playAgain():
            break

play()
