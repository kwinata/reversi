# Reversi
AI to play reversi implemented with alpha-beta pruning principle

The idea of this project comes from https://courses.csail.mit.edu/6.034f/ai3/ch6.pdf.

## Note
The code is not written by myself. The original code is from http://inventwithpython.com/chapter15.html. But the algorithm implemented was only greedy and always-take-corner. Some insight about the strategy was taken from http://www.samsoft.org.uk/reversi/strategy.htm.

## Algorithm
I made some modification to the codes, so now it uses minimax with depth 5 (can be modified, though run time may be not feasible for depth >= 7) and also help of alpha-beta pruning principle. Further readings: https://en.wikipedia.org/wiki/Minimax,
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning.

## Heuristic value
The heuristic value of each condition is determined by the board and the last move. The board's heuristic value is simply the number of the player's tiles times 3, and each move has its own value which is taken from the 2d-array scoretable.

## To run
Best run with Python 3.6.2. Simply run "python reversi.py" for windows or "python3 reversi.py" for unix in the directory that containts the file. (No guarantee it can run in other version of python though it may run). https://www.python.org/downloads/

## Bug
This code has not gone for quite much testing. Should you encounter any bug, error, or suggestions, please kindly email to kevinwinatamichael@gmail.com with logs (if any).
