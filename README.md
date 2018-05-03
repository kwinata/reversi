# Reversi
AI reversi bot that play using minimax (alpha-beta), using naive disk evaluation score table generated using genetic algorithm

The idea of this project comes from https://courses.csail.mit.edu/6.034f/ai3/ch6.pdf.

## Note
The whole code is not written by myself. The original code for the reversi platform is from http://inventwithpython.com/chapter15.html. The algorithm implemented (from the original source) was using greedy and always-take-corner. Some insight about the further strategy to segmentize the game into stages was taken from http://www.samsoft.org.uk/reversi/strategy.htm.

## Algorithm
It uses minimax with depth 5 (can be modified, though run time may be not feasible for depth >= 7) and also help of alpha-beta pruning principle. Further readings: https://en.wikipedia.org/wiki/Minimax,
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning.

A batch of creature is initialized and given a random genotype (which translates to the values of the scoretables they hold for each stage). They play against each other and ranked. Some of the top player will survive, have crossover and mutated to replace for the new generation.

