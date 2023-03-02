def alphabeta_policy(depth, h):
    def fxn(pos):
        alpha = -h.inf
        beta = h.inf
        table = {}
        value, move = alphabeta(pos, depth, h, alpha, beta, table)
        return move
    return fxn

def alphabeta(pos, depth, h, alpha, beta, table):
    ''' Returns the alphabeta value of the given position, with the given heuristic function
        applied at the given depth.

        pos -- a game position
        depth -- a nonnegative integer
        h -- a heuristic function that can be applied to pos and all its successors
    '''
    
    if pos in table:
        return table[pos]

    if pos.is_terminal() or depth == 0:
        return (h.evaluate(pos), None)
    else:
        if pos.actor() == 0:
            best_value = -h.inf
            best_move = None
            moves = pos.get_actions()
            for move in moves:
                child = pos.successor(move)
                value, _ = alphabeta(child, depth - 1, h, alpha, beta, table)
                if value > best_value:
                    best_value = value
                    best_move = move
                    if best_value > alpha:
                        alpha = best_value
                        if beta <= alpha:
                            break
            table[pos] = (best_value, best_move)
            return table[pos]
        else:
            best_value = h.inf
            best_move = None
            moves = pos.get_actions()
            for move in moves:
                child = pos.successor(move)
                value, _ = alphabeta(child, depth - 1, h, alpha, beta, table)
                if value < best_value:
                    best_value = value
                    best_move = move
                    if best_value < beta:
                        beta = best_value
                        if beta <= alpha:
                            break
            table[pos] = (best_value, best_move)
            return table[pos]




def alphabeta_heuristic_policy(depth, h):
    def fxn(pos):
        alpha = -h.inf
        beta = h.inf
        table = {}
        value, move = alphabeta_heuristic(pos, depth, h, alpha, beta, table)
        return move
    return fxn

def alphabeta_heuristic(pos, depth, h, alpha, beta, table):
    """Uses heuristic_successor function to compute scores for more efficient pruning"""
    if pos in table:
        return table[pos]

    if pos.is_terminal() or depth == 0:
        return (h.evaluate(pos), None)
    else:
        if pos.actor() == 0:
            best_value = -h.inf
            best_move = None
            moves = pos.get_actions()
            for move in moves:
                child = pos.heuristic_successor(move)
                value, _ = alphabeta(child, depth - 1, h, alpha, beta, table)
                if value > best_value:
                    best_value = value
                    best_move = move
                    if best_value > alpha:
                        alpha = best_value
                        if beta <= alpha:
                            break
            table[pos] = (best_value, best_move)
            return table[pos]
        else:
            best_value = h.inf
            best_move = None
            moves = pos.get_actions()
            for move in moves:
                child = pos.heuristic_successor(move)
                value, _ = alphabeta(child, depth - 1, h, alpha, beta, table)
                if value < best_value:
                    best_value = value
                    best_move = move
                    if best_value < beta:
                        beta = best_value
                        if beta <= alpha:
                            break
            table[pos] = (best_value, best_move)
            return table[pos]
