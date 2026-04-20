from oxono import State, Game
import time

def alpha_beta_search(game: Game, state: State, remaining_time:float):
    """help chose the best action"""

    time_start = time.time()

    if time_left(remaining_time, time_start) <= 0:
        raise TimeoutError("timeout")
    
    player = game.to_move(state)
    value, move = max_value(game, state,float('-inf'), float('inf'),player, remaining_time, time_start )
    return move


def max_value(game: Game, state: State, alpha: float, beta: float,player:str,remaining_time:float, time_start:float):
    if game.is_terminal(state):
        return game.utility(state, game.to_move(state)),None
    
    if time_left(remaining_time, time_start) <= 0:
        raise TimeoutError("timeout")
    
    v = -float('inf')
    move = None
    for a in game.actions(state):
        v2,a2 = min_value(game,result(game,state,a),alpha,beta,player,remaining_time, time_start)
        if v2 > v:
            move,v = a,v2
            alpha = max(alpha,v)
        if v >=beta: 
            return v , move 
    return v, move

def min_value(game: Game, state: State, alpha: float, beta: float,player:str,remaining_time:float, time_start:float):

    if game.is_terminal(state):
        return game.utility(state, game.to_move(state)), None
    
    if time_left(remaining_time, time_start) <= 0:
        raise TimeoutError("timeout")
   

    v = float('inf')
    move = None
    for a in game.actions(state):
        v2,a2 = max_value(game,result(game,state,a),alpha,beta,player,remaining_time, time_start)
        if v2 < v:
            move,v = a,v2
            beta = min(beta,v)
        if v <= alpha:
            return v, move
    return v, move

   
def result(game: Game, state: State, action):
    """ return the result of a action"""
    copy_state = state.copy()
    game.apply(copy_state, action)
    return copy_state


def time_left(remaining_time: float, time_start: float):
    return remaining_time - (time.time() - time_start)