# Reversi

import random
import sys
from reversi import *

#alphabeta depth
depth = 2

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

def getComputerMove(board, computerTile, scoretable):
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
        score = alphabeta(board, depth, -1e9, 1e9, computerTile, computerTile, scoretable) # get the state of the best minimax board
        score += scoretable[x][y] # add with the cost of the move

        if score > bestScore:
            bestMove = [x, y]
            bestScore = score

    return bestMove

def alphabeta(board, depth, alpha, beta,computerTile, tile, scoretable):
    # implementation of alphabeta pruning

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
            v = alphabeta(child, depth-1, alpha, beta, computerTile, oppTile, scoretable)
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
            v = alphabeta(child, depth-1, alpha, beta, computerTile, oppTile, scoretable)
            v -= scoretable[x][y]

            beta = min(beta, v)

            if beta<=alpha:
                break
        return v

def match():
    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = ['X','O']
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    
    while True:
        if turn == 'player':
            if getValidMoves(mainBoard, playerTile) == []:
                print("Comp1 no valid moves\n")
            else:
                showPoints(playerTile, playerTile, mainBoard)
                x, y = getComputerMove(mainBoard, playerTile, scoretable)
                makeMove(mainBoard, playerTile, x, y)
                print("Comp1",x,y) 
            turn = 'computer'

        else:
            if getValidMoves(mainBoard, computerTile) == []:
                if getValidMoves(mainBoard, playerTile) == []:
                    print("Game ends: No move possible")
                    break
                print("No valid move\n")
            else:
                showPoints(playerTile, computerTile, mainBoard)
                x, y = getComputerMove(mainBoard, computerTile, scoretable)
                makeMove(mainBoard, computerTile, x, y)
                print("Comp2",x,y)
            turn = 'player'

    # Display the final score.
    drawBoard(mainBoard)
    scores = getPointBoard(mainBoard)
    print('Comp1 scored %s points. Comp2 scored %s points.' % (scores['X'], scores['O']))
    
    # Calculate Fitness
    if(scores['X']>scores['O']):
        return 1
    elif(scores['X']<scores['O']):
        return 0
    else:
        return -1

fitness = 0
results = []
for i in range(5):
    tmp = match()
    results.append(tmp)
    fitness += tmp

print("Fitness =", fitness)
print(results)
