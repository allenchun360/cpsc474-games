# from assignment 4
class Heuristic:
    ''' A wrapper for a heuristic function that counts how many times the
        heuristic is called.
    '''
    def __init__(self, h):
        ''' Creates a wrapper for the given function.

            h -- a heuristic function that takes a game position and returns its heuristic value,
                 or its actual value if the position is terminal.
        '''
        self.calls = 0
        self.heuristic = h
        self.inf = float("inf") 

        
    def evaluate(self, pos):
        ''' Returns the underlying heuristic applied to the given position.

            pos -- a game position
        '''
        # calls on terminal positions don't count
        if not pos.is_terminal():
            self.calls += 1
        return self.heuristic(pos)

    
    def count_calls(self):
        ''' Returns the number of times this heuristic has been called.
        '''
        return self.calls