# adapted from assignment 4
import random
import sys
import argparse
import alphabeta
import heuristic

from peg_game import PeggingGame

def random_choice(position):
    moves = position.get_actions()
    return random.choice(moves)


def compare_policies(game, p1, p2, games, prob):
    p1_wins = 0
    p2_wins = 0
    p1_score = 0

    for i in range(games):
        # start with fresh copies of the policy functions
        p1_policy = p1()
        p2_policy = p2()
        position = game.initial_state()
        copy = position
        
        while not position.is_terminal():
            if random.random() < prob:
                if position.actor() == i % 2:
                    move = p1_policy(position)
                else:
                    move = p2_policy(position)
            else:
                move = random_choice(position)
            position = position.successor(move)

        p1_score += position.payoff() * (1 if i % 2 == 0 else -1)
        if position.payoff() == 0:
            p1_wins += 0.5
            p2_wins += 0.5
        elif (position.payoff() > 0 and i % 2 == 0) or (position.payoff() < 0 and i % 2 == 1):
            p1_wins += 1
        else:
            p2_wins += 1

    return p1_score / games, p1_wins / games


def test_game(game, count, p_random, p1_policy_fxn, p2_policy_fxn):
    ''' Tests a search policy through a series of pegging games of Cribbage.
        The test passes if the search wins at least the given percentage of
        games and calls its heuristic function at most the given proportion of times
        relative to alphabeta pruning.  Writes the winning percentage of the second
        policy to standard output.

        game -- a game
        count -- a positive integer
        p_random -- the probability of making a random move instead of the suggested move
        p1_policy_fxn -- a function that takes no arguments and returns
                         a function that takes a position and returns the
                       suggested move
        p2_policy_fxn -- a function that takes no arguments and returns
                         a function that takes a position and returns the
                       suggested move
                      
    '''
    margin, wins = compare_policies(game, p1_policy_fxn, p2_policy_fxn, count, 1.0 - p_random)

    print("NET: ", margin, "; WINS: ", wins, sep="")

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test alphabeta agent")
    parser.add_argument('--count', dest='count', type=int, action="store", default=2, help='number of games to play (default=2')
    parser.add_argument('--alphaBetaHeuristicDepth', dest='depth1', type=int, action='store', default=2, help='depth of alphabeta search for agent 1 (default=2)')
    parser.add_argument('--alphaBetaDepth', dest='depth2', type=int, action='store', default=2, help='depth of alphabeta search for agent 2 (default=2)')
    parser.add_argument('--random', dest="p_random", type=float, action="store", default = 0.0, help="p(random instead of alphabeta) (default=0.0)")
    args = parser.parse_args()

    game = PeggingGame(4)
    h = (lambda pos: pos.score()[0] - pos.score()[1])

    test_game(game,
                args.count,
                args.p_random,
                lambda: alphabeta.alphabeta_heuristic_policy(args.depth1, heuristic.Heuristic(h)),
                lambda: alphabeta.alphabeta_policy(args.depth2, heuristic.Heuristic(h)))
    sys.exit(0)
