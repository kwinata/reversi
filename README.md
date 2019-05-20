# Reversi
AI to play reversi implemented with alpha-beta pruning principle

The idea of this project comes from https://courses.csail.mit.edu/6.034f/ai3/ch6.pdf.

## Note
The whole code is not written by myself. The original code is from http://inventwithpython.com/chapter15.html. But the algorithm implemented was only greedy and always-take-corner. Some insight about the strategy was taken from http://www.samsoft.org.uk/reversi/strategy.htm.

## Algorithm
I made some modification to the codes, so now it uses minimax with depth 5 (can be modified, though run time may be not feasible for depth >= 7) and also help of alpha-beta pruning principle. Further readings: https://en.wikipedia.org/wiki/Minimax,
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning.

## Heuristic value
The heuristic value of each condition is determined by the board and the last move. The board's heuristic value is simply the number of the player's tiles times 3, and each move has its own value which is taken from the 2d-array scoretable.

## To run
Best run with Python 3.6.2. Simply run "python reversi.py" for windows or "python3 reversi.py" for unix in the directory that containts the file. (No guarantee it can run in other version of python though it may run). https://www.python.org/downloads/

## Improvement
The evaluation here doesn't care with different situation of the game. We can improve the computer play by putting different cases and stages of game. For example, when no body have put their piece outside the inner 4 x 4 box yet, or after the first piece put on the edge of the board, etc. We can implement different stages of goal for each stages of game. Those things are not done yet.

## Bug
This code has not gone for quite much testing. Should you encounter any bug, error, or suggestions, please kindly email to kevinwinatamichael@gmail.com with logs (if any).

## Diagram

### Component Diagram
![reversi component diagram](https://github.com/kevinwinatamichael/reversi/blob/master/component_diagram.png "Component Diagram")