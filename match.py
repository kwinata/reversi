# Reversi

import threading
import random
import sys
from reversi import *

import time
start_time = time.time()

# input
depth = 1

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
    return flag

def match(i, numberofmatch, results, progresses, scoretables1, scoretables2):
    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = ['X','O']
    showHints = False
    turn = whoGoesFirst() 
    numturn=1
    while True:
        if turn == 'player':
            if getValidMoves(mainBoard, playerTile) == []:
                pass
            else:
                x, y = getComputerMove(mainBoard, playerTile, scoretables1)
                makeMove(mainBoard, playerTile, x, y)
            turn = 'computer'

        else:
            if getValidMoves(mainBoard, computerTile) == []:
                if getValidMoves(mainBoard, playerTile) == []:
                    break
            else:
                x, y = getComputerMove(mainBoard, computerTile, scoretables2)
                makeMove(mainBoard, computerTile, x, y) 
            turn = 'player'
        numturn+=1
        
    # Calculate Fitness
    scores = getPointBoard(mainBoard) 
    if(scores[playerTile]>scores[computerTile]):
        fit = 1
    elif(scores[playerTile]<scores[computerTile]):
        fit = 0
    else:
        fit = 0.5
    results[i]=fit

    #print("match", i, "out of", j, ":", '%2s %2s %2s' % (scores['X'], scores['O'], fit))
    
    return


def versus(numberofmatch, scoretables1, scoretables2):
    threads = []
    results= [0]*numberofmatch
    progresses = [0]*numberofmatch

    for i in range(numberofmatch):
        t = threading.Thread(target=match,
                             args=(i, numberofmatch,results, progresses, scoretables1, scoretables2))
        threads.append(t)
        t.start()

    # wait until all threads complete
    for t in threads:
        t.join()

    tmp=0
    for i in range(numberofmatch):
        tmp += results[i]
    fitness = (tmp)/numberofmatch
    print('Time spent      : %s s' % int(time.time() - start_time))
    return fitness
