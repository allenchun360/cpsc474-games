import sys
from itertools import combinations
from decimal import Decimal
import math

two_dice_probs = {
        '2': 1/36,
        '3': 2/36,
        '4': 3/36,
        '5': 4/36,
        '6': 5/36,
        '7': 6/36,
        '8': 5/36,
        '9': 4/36,
        '10': 3/36,
        '11': 2/36,
        '12': 1/36,
    }

EV_dict = {}

def find_all_sums(state, roll):

    numbers = []

    for c in state:
        numbers.append(int(c))
    result = []
    for i in range(1,5):
        for seq in combinations(numbers, i):
            if sum(seq) == roll:
                result.append(seq)

    new_result = []

    for element in result:
        state_str = ''
        for i in element:
            state_str += str(i)
        new_result.append(state_str)
        
    return new_result

def subtract_sum_from_state(state, move):
    state_list = []
    move_list = []
    for i in state:
        state_list.append(i)
    for i in move:
        move_list.append(i)

    result_list = [x for x in state_list if x not in move_list]

    result = ''
    for i in result_list:
        result += i
    return result


def eval(state, target, roll):

    sum = 0
    min_roll = 1
    max_roll = 6

    for i in state:
        sum += int(i)

    if sum > 6:
        min_roll = 2
        max_roll = 12

    ev = 0
    best_move = None
    for r in range(min_roll, max_roll + 1):
        best_ev = 0
        all_sums = find_all_sums(state, r)
        length = len(all_sums)

        # no more next moves
        if length == 0 and sum > target:
            best_ev = 0
        if length == 0 and sum == target:
            best_ev = 0.5
        if length == 0 and sum < target:
            best_ev = 1
        elif length != 0:
            for move in all_sums:
                next_state = subtract_sum_from_state(state, move)
                if (next_state, target) in EV_dict:
                    new_ev = EV_dict[(next_state, target)]
                else:
                    new_ev = eval(next_state, target, roll)[0]
                if new_ev > best_ev:
                    best_ev = new_ev
                    if roll == r:
                        move_list = []
                        for s in move:
                            move_list.append(int(s))
                        best_move = move_list

        if sum > 6:
            ev += two_dice_probs[str(r)] * best_ev
        else:
            ev += (1/6) * best_ev

    EV_dict[(state, target)] = ev

    return EV_dict[(state, target)], best_move

def eval2(state, roll):

    sum = 0
    min_roll = 1
    max_roll = 6

    for i in state:
        sum += int(i)

    if sum > 6:
        min_roll = 2
        max_roll = 12

    ev = 0
    best_move = None
    for r in range(min_roll, max_roll + 1):
        best_ev = 0
        all_sums = find_all_sums(state, r)
        length = len(all_sums)

        if length == 0 and state == '':
            best_ev = 1
        # no more next moves
        elif length == 0 and state != '':
            for i in range(2, 13):
                best_ev += two_dice_probs[str(i)] * (1 - eval('123456789', sum, i)[0])
        elif length != 0:
            for move in all_sums:
                next_state = subtract_sum_from_state(state, move)
                if next_state in EV_dict:
                    new_ev = EV_dict[next_state]
                else:
                    new_ev = eval2(next_state, roll)[0]
                if new_ev > best_ev:
                    best_ev = new_ev
                    if roll == r:
                        move_list = []
                        for s in move:
                            move_list.append(int(s))
                        best_move = move_list

        if sum > 6:
            ev += two_dice_probs[str(r)] * best_ev
        else:
            ev += (1/6) * best_ev

    EV_dict[state] = ev

    return EV_dict[state], best_move


def main(arg):
    # if arg[0]
    # state_list = create_states(9)
    dice_sides = 6
    # dictionary has keys as tuples of (S, r, t) and expected values as values
    EV_dict = {}

    if arg[1] == '--two' and arg[2] == '--expect':
        state = arg[3]
        target = int(arg[4])
        print("%.6f" % eval(state, target, None)[0])
    elif arg[1] == '--two' and arg[2] == '--move':
        state = arg[3]
        target = int(arg[4])
        roll = int(arg[5])
        print(eval(state, target, roll)[1])
    elif arg[1] == '--one' and arg[2] == '--expect':
        state = arg[3]
        print("%.6f" % eval2(state, None)[0])
    elif arg[1] == '--one' and arg[2] == '--move':
        state = arg[3]
        roll = int(arg[4])
        print(eval2(state, roll)[1])

    return arg

if __name__ == '__main__':
    main(sys.argv)
