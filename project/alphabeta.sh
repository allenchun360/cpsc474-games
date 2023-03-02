#!/bin/bash

echo "I'm using alphabeta pruning with transposition tables to play a perfect information pegging game in Cribbage.
The alphabeta model also uses modified heurisitics in the 'heuristics_successor' function that takes into consideration the rank of a potential pegging card and the current state of the game to prune more efficiently.
The NET value is the average payoff to an alphabeta agent with heuristics searching to depth 10 over 1000 games when playing with an alphabeta agent searching to depth 8.
The WINS value is the average number of wins for the alphabeta agent with heuristics searching to depth 10 vs. the alphabeta agent with depth 8:"
python3 test_alphabeta.py --count=1000 --alphaBetaHeuristicDepth=10 --alphaBetaDepth=8

echo "
Results for both at depth 8:"
python3 test_alphabeta.py --count=1000 --alphaBetaHeuristicDepth=8 --alphaBetaDepth=8