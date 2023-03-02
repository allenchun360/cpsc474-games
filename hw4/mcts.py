import math
from random import choice
import time

total_games = 0
total_runs = 0

def traverse(tree, explore_visits, pos, explore_complete):
    moves = pos.get_actions()
    best_score = -(math.inf)
    best_child = None
    best_move = None

    for move in moves:
        child = pos.successor(move)
        if child.__hash__() not in tree:
            return child, move
        else:
            score = ucb(tree, explore_visits, pos.__hash__(), pos.actor(), child.__hash__(), explore_complete)
            if score > best_score:
                best_score = score
                best_child = child
                best_move = move

    return best_child, best_move

# tree[pos] = (visits, payoff)
# explore_visits[(parent, child)] = edge_visits # should this be explore_visits[(parent, child)] = edge_vists, payoffs

def ucb(tree, explore_visits, pos_hash, pos_actor, child_hash, explore_complete):
    child_node = tree[child_hash]
    explore = 0
    if not explore_complete:
        explore = math.sqrt(2 * math.log(tree[pos_hash][0]) / child_node[0])#explore_visits[(pos, child)]) # chil
    exploit = child_node[1] / child_node[0] # need to multiply by -1 when p2 turn  # should this be exploit = child_node[1] when explore_complete is True
    if pos_actor == 1:
        exploit = exploit * -1
    return exploit + explore
    
def expand(tree, explore_visits, child_hash, path):
    tree[child_hash] = [0, 0]
    # explore_visits[(path[-2], child)] = 0

def rollout(pos):
    children = pos.get_actions()
    if len(children) == 0:
        return pos.payoff()
    next_pos = pos.successor(choice(children))
    while not next_pos.is_terminal():
        children = next_pos.get_actions()
        next_pos = next_pos.successor(choice(children))

    return next_pos.payoff()

def backprop(tree, explore_visits, path, payoff):
    for i, node in enumerate(path):
        # node_hash = node.__hash__()
        node_hash = node.__hash__()
        tree[node_hash][0] += 1
        tree[node_hash][1] += payoff
        # if i > 0:
        #     explore_visits[(path[i-1], node)] += 1

def mcts_policy(time):
        def fxn(pos):
            move = run_mcts(pos, time)
            return move
        return fxn

def run_mcts(pos, time_limit):
    tree = {}
    # tree_hash={}
    pos.__hash__()
    tree[pos.__hash__()] = [0, 0]
    explore_visits = {}
    start_time = time.time()
    global total_games
    global total_runs
    total_games += 1
    while time.time() - start_time < time_limit:
        total_runs += 1
        temp = pos
        path = [pos]
        payoff = 0
        while temp.__hash__() in tree and not temp.is_terminal():
            temp = traverse(tree, explore_visits, temp, False)[0]
            path.append(temp)

        if temp.__hash__() not in tree:
            expand(tree, explore_visits, temp.__hash__(), path)
            payoff = rollout(temp)
        else:
            payoff = temp.payoff()

        backprop(tree, explore_visits, path, payoff)

    if total_games % 100 == 0:
        print(total_runs / total_games)

    return traverse(tree, explore_visits, pos, True)[1]