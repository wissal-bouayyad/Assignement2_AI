from oxono import State, Game

def alpha_beta_search(game: Game, state: State):
    """help chose the best action"""
    player = game.to_move(state)
    value, move = max_value(game, state,float('-inf'), float('inf') )
    return move


def max_value(game: Game, state: State, alpha: float, beta: float):
    if game.is_terminal(state):
        return game.utility(state, game.to_move(state))
    
    v = -float('inf')
    move = None
    for a in game.actions(state):
        v2,a2 = min_value(game,game.result(state,a),alpha,beta)
        if v2 > v:
            move,v = a,v2
            alpha = max(alpha,v)
        if v >=beta: 
            return v , move 
    return v, move

def min_value(game: Game, state: State, alpha: float, beta: float):
    if game.is_terminal(state):
        return game.utility(state, game.to_move(state))
    v = float('inf')
    move = None
    for a in game.actions(state):
        v2,a2 = max_value(game,game.result(state,a),alpha,beta)
        if v2 < v:
            move,v = a,v2
            beta = min(beta,v)
        if v <= alpha:
            return v, move
    return v, move

   
