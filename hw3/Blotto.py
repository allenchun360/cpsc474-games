import sys
import itertools
import numpy as np
import scipy.optimize

ev_matrix = []
score_matrix = []
lottery_matrix = []

def partitions(n, k):
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]

def create_matrix(units, battlefields, lowest_score_value, lowest_lottery_value):
    num_of_battlefields = len(battlefields)
    strategies = list(partitions(units, num_of_battlefields))
    size_of_matrix = len(strategies)

    for i in range(size_of_matrix):
        ev_matrix.append([])
        score_matrix.append([])
        lottery_matrix.append([])
        for j in range(size_of_matrix):
            player1_score = 0
            player2_score = 0
            player1_lottery_value = 0

            for k in range(num_of_battlefields):
                if strategies[i][k] == 0 and strategies[j][k] == 0:
                    probability = 0.5
                    player1_lottery_value += probability * int(battlefields[k])
                else:
                    probability = (strategies[i][k] ** 2)/((strategies[i][k] ** 2) + (strategies[j][k] ** 2))
                    player1_lottery_value += probability * int(battlefields[k])

                if strategies[i][k] > strategies[j][k]:
                    player1_score += int(battlefields[k])
                elif strategies[i][k] < strategies[j][k]:
                    player2_score += int(battlefields[k])
                elif strategies[i][k] == strategies[j][k]:
                    player1_score += int(battlefields[k])/2
                    player2_score += int(battlefields[k])/2

            if player1_score > player2_score:
                ev_matrix[i].append(2)
            elif player1_score < player2_score:
                ev_matrix[i].append(1)
            elif player1_score == player2_score:
                ev_matrix[i].append(1.5)
            
            if player1_score < lowest_score_value:
                lowest_score_value = player1_score
            score_matrix[i].append(player1_score)

            if player1_lottery_value < lowest_lottery_value:
                lowest_lottery_value = player1_lottery_value
            lottery_matrix[i].append(player1_lottery_value)

    return strategies, lowest_score_value, lowest_lottery_value

def linear_programming(matrix, strategies, tolerance, lowest_value):
    transposed_matrix = np.array(matrix).T.tolist()
    negated_matrix = [[j*(-1) for j in i] for i in transposed_matrix]
    rows = len(matrix)
    cols = rows
    bounds = (0.0, 1.0 / lowest_value)
    b_ub = [-1.0] * cols
    c = [1.0] * rows

    result = scipy.optimize.linprog(c, negated_matrix, b_ub, None, None, bounds)

    value = 1.0 / result.fun
    x = [xi * value for xi in result.x]

    count = 0
    for value in x:
        if value > tolerance:
            result = ''
            for i in range(len(strategies[count])):
                result += str(strategies[count][i]) + ','
            result += str(value)
            print(result)
        count += 1

def verify(expected_value, moves, battlefields, tolerance, objective):
    num_of_battlefields = len(battlefields)
    mixed_strategies = []
    probabilities = []
    for move in moves:
        value = ''
        strategy = []
        count = 0
        for character in move:
            if character == ',':
                strategy.append(int(value))
                value = ''
                count += 1
            elif character == '\n':
                probabilities.append(float(value))
                value = ''
            else:
                value += character
        mixed_strategies.append(strategy)

    units = 0
    if mixed_strategies != []:
        for i in mixed_strategies[0]:
            units += i
            
    pure_strategies = list(partitions(units, num_of_battlefields))

    for i in range(len(pure_strategies)):
        player1_expected_score = 0
        player2_expected_score = 0
        player1_lottery_value = 0
        player1_win = 0
        for j in range(len(mixed_strategies)):
            player1_score = 0
            player2_score = 0

            for k in range(num_of_battlefields):
                if pure_strategies[i][k] == 0 and mixed_strategies[j][k] == 0:
                    probability = 0.5
                    player1_lottery_value += probability * int(battlefields[k]) * probabilities[j]
                else:
                    probability = (pure_strategies[i][k] ** 2)/((pure_strategies[i][k] ** 2) + (mixed_strategies[j][k] ** 2))
                    player1_lottery_value += probability * int(battlefields[k]) * probabilities[j]

                if pure_strategies[i][k] > mixed_strategies[j][k]:
                    player1_score += int(battlefields[k])
                    player1_expected_score += int(battlefields[k]) * probabilities[j]
                elif pure_strategies[i][k] < mixed_strategies[j][k]:
                    player2_score += int(battlefields[k])
                    player2_expected_score += int(battlefields[k]) * probabilities[j]
                elif pure_strategies[i][k] == mixed_strategies[j][k]:
                    player1_score += int(battlefields[k])/2
                    player2_score += int(battlefields[k])/2
                    player1_expected_score += (int(battlefields[k])/2) * probabilities[j]
                    player2_expected_score += (int(battlefields[k])/2) * probabilities[j]
            
            if player1_score > player2_score:
                player1_win += 2 * probabilities[j]
            elif player1_score < player2_score:
                player1_win += 1 * probabilities[j]
            elif player1_score == player2_score:
                player1_win += 1.5 * probabilities[j]

        if objective == 'win':
            if player1_win > 1.5:
                if player1_win - 1.5 > tolerance:
                    print(expected_value - player1_expected_score)
                    print("Not equilibrium")
                    return

        if objective == 'score':
            if player1_expected_score > expected_value:
                if player1_expected_score - expected_value > tolerance:
                    print(expected_value - player1_expected_score)
                    print("Not equilibrium")
                    return

        if objective == 'lottery':
            if player1_lottery_value > expected_value:
                if player1_lottery_value - expected_value > tolerance:
                    print(player1_lottery_value - expected_value)
                    print("Not equilibrium")
                    return
                        
    print("PASSED")
    return


def main(args):
    if args[1] == '--find' and args[2] == '--win' and args[3] == '--units':
        battlefields = args[5:len(args)]
        strategies = create_matrix(int(args[4]), battlefields, 0, 1)[0]
        linear_programming(ev_matrix, strategies, 1e-6, 1)
    elif args[1] == '--find' and args[2] == '--score' and args[3] == '--units':
        battlefields = args[5:len(args)]
        total_points = 0
        for i in battlefields:
            total_points += int(i)
        lowest_score_value = total_points
        lowest_lottery_value = 1
        result = create_matrix(int(args[4]), battlefields, lowest_score_value, lowest_lottery_value)
        strategies = result[0]
        linear_programming(score_matrix, strategies, 1e-6, result[1])
    elif args[1] == '--find' and args[2] == '--lottery' and args[3] == '--units':
        battlefields = args[5:len(args)]
        lowest_score_value = 0
        lowest_lottery_value = 1
        result = create_matrix(int(args[4]), battlefields, lowest_score_value, lowest_lottery_value)
        strategies = result[0]
        linear_programming(lottery_matrix, strategies, 1e-6, result[2])
    elif args[1] == '--find' and args[2] == '--tolerance' and args[4] == '--win' and args[5] == '--units':
        battlefields = args[7:len(args)]
        strategies = create_matrix(int(args[6]), battlefields, 0, 1)[0]
        tolerance = float(args[3])
        linear_programming(ev_matrix, strategies, tolerance, 1)
    elif args[1] == '--find' and args[2] == '--tolerance' and args[4] == '--score' and args[5] == '--units':
        battlefields = args[7:len(args)]
        total_points = 0
        for i in battlefields:
            total_points += int(i)
        lowest_score_value = total_points
        lowest_lottery_value = 1
        result = create_matrix(int(args[6]), battlefields, lowest_score_value, lowest_lottery_value)
        result[0] = strategies
        tolerance = float(args[3])
        linear_programming(score_matrix, strategies, tolerance, result[1])
    elif args[1] == '--find' and args[2] == '--tolerance' and args[4] == '--lottery' and args[5] == '--units':
        battlefields = args[7:len(args)]
        lowest_score_value = 0
        lowest_lottery_value = 1
        result = create_matrix(int(args[6]), battlefields)
        strategies = result[0]
        tolerance = float(args[3])
        linear_programming(lottery_matrix, strategies, tolerance, result[2])
    elif args[1] == '--verify' and args[2] == '--win':
        battlefields = args[3:len(args)]
        total_points = 0
        for i in battlefields:
            total_points += int(i)
        expected_value = total_points / 2
        verify(expected_value, sys.stdin, battlefields, 1e-6, 'win')
    elif args[1] == '--verify' and args[2] == '--score':
        battlefields = args[3:len(args)]
        total_points = 0
        for i in battlefields:
            total_points += int(i)
        expected_value = total_points / 2
        verify(expected_value, sys.stdin, battlefields, 1e-6, 'score')
    elif args[1] == '--verify' and args[2] == '--lottery':
        battlefields = args[3:len(args)]
        total_points = 0
        for i in battlefields:
            total_points += int(i)
        expected_value = total_points / 2
        verify(expected_value, sys.stdin, battlefields, 1e-6, 'lottery')
    elif args[1] == '--verify' and args[2] == '--tolerance' and args[4] == '--win':
        battlefields = args[5:len(args)]
        total_points = 0
        for i in battlefields:
            total_points += int(i)
        expected_value = total_points / 2
        verify(expected_value, sys.stdin, battlefields, float(args[3]), 'win')
    elif args[1] == '--verify' and args[2] == '--tolerance' and args[4] == '--score':
        battlefields = args[5:len(args)]
        total_points = 0
        for i in battlefields:
            total_points += int(i)
        expected_value = total_points / 2
        verify(expected_value, sys.stdin, battlefields, float(args[3]), 'score')
    elif args[1] == '--verify' and args[2] == '--tolerance' and args[4] == '--lottery':
        battlefields = args[5:len(args)]
        total_points = 0
        for i in battlefields:
            total_points += int(i)
        expected_value = total_points / 2
        verify(expected_value, sys.stdin, battlefields, float(args[3]), 'lottery')

if __name__ == '__main__':
    main(sys.argv)