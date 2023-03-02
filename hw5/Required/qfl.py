# import time
# import random

# def q_learn(game, time_limit):
#     q_table = run_q_learning(game, time_limit)
#     def fxn(pos):
#         action = find_max(pos, q_table, game)[0]
#         return action
#     return fxn

# def run_q_learning(game, time_limit):
#     alpha_value = 0.25
#     epsilon = 0.2
#     gamma = 0.9998
#     q_table = create_table(game, alpha_value)
#     start_time = time.time()
#     while time.time() - start_time < time_limit:
#         pos = game.initial_position()
#         while game.game_over(pos) is False:
#             action = choose_action(epsilon, pos, q_table, game)
#             next_pos, outcome = game.result(pos, action)
#             reward = 0
#             if game.game_over(next_pos):
#                 if game.win(next_pos):
#                     reward = 1
#                 else:
#                     reward = 0
#             else:
#                 reward = find_max(next_pos, q_table, game)[1]
#             result = q_table[find_bin(pos)][action]
#             alpha = result[1]
#             result[0] += alpha * (reward - result[0])
#             result[1] *= gamma
#             pos = next_pos
#     return q_table

# def create_table(game, alpha_value):
#     table = {}
#     q_value = 0
#     for bin in range(36):
#         table[bin] = {}
#         for i in range(game.offensive_playbook_size()):
#             table[bin][i] = [q_value, alpha_value]
#     return table

# def find_bin(pos):
#     yards_to_score, downs_left, distance, ticks = pos
#     x_value = yards_to_score/ticks
#     y_value = distance/downs_left
#     x_index = 0
#     y_index = 0

#     if x_value < 1:
#         x_index = 0
#     elif x_value < 2:
#         x_index = 1
#     elif x_value < 3.5:
#         x_index = 2
#     elif x_value < 5:
#         x_index = 3
#     elif x_value < 6:
#         x_index = 4
#     else:
#         x_index = 5

#     if y_value < 1.5:
#         y_index = 0
#     elif y_value < 2.4:
#         y_index = 1
#     elif y_value < 2.5:
#         y_index = 2
#     elif y_value < 4:
#         y_index = 3
#     elif y_value < 5:
#         y_index = 4
#     else:
#         y_index = 5

#     return 6 * y_index + x_index

# def find_max(pos, table, game):
#     best_action = 0
#     best_value = 0
#     for i in range(game.offensive_playbook_size()):
#         if table[find_bin(pos)][i][0] > best_value:
#             best_value = table[find_bin(pos)][i][0]
#             best_action = i
#     return best_action, best_value

# def choose_action(epsilon, pos, q_table, game):
#     random_num = random.uniform(0, 1)
#     if random_num < epsilon:
#         return random.randint(0, 2)
#     else:
#         return find_max(pos, q_table, game)[0]

# import time
# import random

# def q_learn(game, time_limit):
#     alpha_value = 0.25
#     epsilon = 0.2
#     gamma = 0.9999
#     start_time = time.time()
#     max_qtable = None
#     max_score = 0
#     new_limit = 0
#     remaining = time_limit
#     for i in range(4):
#         q_table = create_table(game, alpha_value)
#         new_limit += remaining / (4-i)
#         while time.time() - start_time < new_limit:
#             pos = game.initial_position()
#             while game.game_over(pos) is False:
#                 action = choose_action(epsilon, pos, q_table, game)
#                 next_pos, outcome = game.result(pos, action)
#                 reward = 0
#                 if game.game_over(next_pos):
#                     if game.win(next_pos):
#                         reward = 1
#                     else:
#                         reward = 0
#                 else:
#                     reward = find_max(next_pos, q_table, game)[1]
#                 result = q_table[find_bin(pos)][action]
#                 alpha = result[1]
#                 result[0] += alpha * (reward - result[0])
#                 result[1] *= gamma
#                 pos = next_pos
#         def fxn(pos):
#             action = find_max(pos, q_table, game)[0]
#             return action
#         score = game.simulate(fxn, 10000)
#         if score > max_score:
#             max_score = score
#             max_qtable = q_table
#         remaining = time_limit - (time.time() - start_time)

#     def fxn2(pos):
#         action = find_max(pos, max_qtable, game)[0]
#         return action
#     return fxn2

# def create_table(game, alpha_value):
#     table = {}
#     q_value = 0
#     for bin in range(9):
#         table[bin] = {}
#         for i in range(game.offensive_playbook_size()):
#             table[bin][i] = [q_value, alpha_value]
#     return table

# def find_bin(pos):
#     yards_to_score, downs_left, distance, ticks = pos
#     x_value = yards_to_score/ticks
#     y_value = distance/downs_left
#     x_index = 0
#     y_index = 0

#     if x_value < 2:
#         x_index = 0
#     elif x_value < 4:
#         x_index = 1
#     else:
#         x_index = 2

#     if y_value  < 2.5:
#         y_index = 0
#     elif y_value < 5:
#         y_index = 1
#     else:
#         y_index = 2

#     return 3 * y_index + x_index

# def find_max(pos, table, game):
#     best_action = 0
#     best_value = 0
#     for i in range(game.offensive_playbook_size()):
#         if table[find_bin(pos)][i][0] > best_value:
#             best_value = table[find_bin(pos)][i][0]
#             best_action = i
#     return best_action, best_value

# def choose_action(epsilon, pos, q_table, game):
#     random_num = random.uniform(0, 1)
#     if random_num < epsilon:
#         return random.randint(0, 2)
#     else:
#         return find_max(pos, q_table, game)[0]

# import time
# import random

# def q_learn(game, time_limit):
#     q_table = run_q_learning(game, time_limit)
#     def fxn(pos):
#         action = find_max(pos, q_table, game)[0]
#         return action
#     return fxn

# def run_q_learning(game, time_limit):
#     alpha_value = 0.25
#     epsilon = 0.2
#     gamma = 0.9999
#     q_table = create_table(game, alpha_value)
#     start_time = time.time()
#     while time.time() - start_time < time_limit:
#         pos = game.initial_position()
#         while game.game_over(pos) is False:
#             action = choose_action(epsilon, pos, q_table, game)
#             next_pos, outcome = game.result(pos, action)
#             reward = 0
#             if game.game_over(next_pos):
#                 if game.win(next_pos):
#                     reward = 1
#                 else:
#                     reward = 0
#             else:
#                 reward = find_max(next_pos, q_table, game)[1]
#             result = q_table[find_bin(pos)][action]
#             alpha = result[1]
#             result[0] += alpha * (reward - result[0])
#             result[1] *= gamma
#             pos = next_pos
#     return q_table

# def create_table(game, alpha_value):
#     table = {}
#     q_value = 0
#     for bin in range(12):
#         table[bin] = {}
#         for i in range(game.offensive_playbook_size()):
#             table[bin][i] = [q_value, alpha_value]
#     return table

# def find_bin(pos):
#     yards_to_score, downs_left, distance, ticks = pos
#     x_value = yards_to_score/ticks
#     y_value = distance/downs_left
#     x_index = 0
#     y_index = 0

#     if x_value < 2:
#         x_index = 0
#     elif x_value < 4:
#         x_index = 1
#     else:
#         x_index = 2

#     if y_value < 2.4:
#         y_index = 0
#     elif y_value  < 2.5:
#         y_index = 1
#     elif y_value < 5:
#         y_index = 2
#     else:
#         y_index = 3

#     return 3 * y_index + x_index

# def find_max(pos, table, game):
#     best_action = 0
#     best_value = 0
#     for i in range(game.offensive_playbook_size()):
#         if table[find_bin(pos)][i][0] > best_value:
#             best_value = table[find_bin(pos)][i][0]
#             best_action = i
#     return best_action, best_value

# def choose_action(epsilon, pos, q_table, game):
#     random_num = random.uniform(0, 1)
#     if random_num < epsilon:
#         return random.randint(0, 2)
#     else:
#         return find_max(pos, q_table, game)[0]


import time
import random

def q_learn(game, time_limit):
    q_table = run_q_learning(game, time_limit)
    def fxn(pos):
        action = find_max(pos, q_table, game)[0]
        return action
    return fxn

def run_q_learning(game, time_limit):
    alpha_value = 0.25
    epsilon = 0.2
    gamma = 0.9999
    q_table = create_table(game, alpha_value)
    start_time = time.time()
    while time.time() - start_time < time_limit:
        pos = game.initial_position()
        while game.game_over(pos) is False:
            action = choose_action(epsilon, pos, q_table, game)
            next_pos, outcome = game.result(pos, action)
            reward = 0
            if game.game_over(next_pos):
                if game.win(next_pos):
                    reward = 1
                else:
                    reward = 0
            else:
                reward = find_max(next_pos, q_table, game)[1]
            result = q_table[find_bin(pos)][action]
            alpha = result[1]
            result[0] += alpha * (reward - result[0])
            result[1] *= gamma
            pos = next_pos
    return q_table

def create_table(game, alpha_value):
    table = {}
    q_value = 0
    for bin in range(9):
        table[bin] = {}
        for i in range(game.offensive_playbook_size()):
            table[bin][i] = [q_value, alpha_value]
    return table

def find_bin(pos):
    yards_to_score, downs_left, distance, ticks = pos
    x_value = yards_to_score/ticks
    y_value = distance/downs_left
    x_index = 0
    y_index = 0

    if x_value < 2:
        x_index = 0
    elif x_value < 4:
        x_index = 1
    else:
        x_index = 2

    if y_value  < 2.5:
        y_index = 0
    elif y_value < 5:
        y_index = 1
    else:
        y_index = 2

    return 3 * y_index + x_index

def find_max(pos, table, game):
    best_action = 0
    best_value = 0
    for i in range(game.offensive_playbook_size()):
        if table[find_bin(pos)][i][0] > best_value:
            best_value = table[find_bin(pos)][i][0]
            best_action = i
    return best_action, best_value

def choose_action(epsilon, pos, q_table, game):
    random_num = random.uniform(0, 1)
    if random_num < epsilon:
        return random.randint(0, 2)
    else:
        return find_max(pos, q_table, game)[0]