from agent import Agent
import time
from oxono import State, Game


class MyAgent(Agent):
    def act(self, state, remaining_time):
        try:
            t_time = (min(0.2, remaining_time * 0.1))
            return Iterative_deepening_alpha_beta_search(Game, state, t_time)
        except TimeoutError:
            return None


def Iterative_deepening_alpha_beta_search(game: Game, state: State, remaining_time: float):
        depth = 1
        move = None
        s_time = time.time()
        while True:
            if time.time() - s_time >= remaining_time:
                break
            try:
                result = alpha_beta_search(game, state, remaining_time - (time.time() - s_time), depth, move)
                if result != (None, None):
                    move = result
                depth += 1
            except TimeoutError:
                break
        return move


def alpha_beta_search(game: Game, state: State, remaining_time: float, depth: float, f_move=None):
    """chose the best action"""
    time_start = time.time()
    if time_left(remaining_time, time_start) <= 0:
        raise TimeoutError("timeout")

    player = game.to_move(state)
    value, move = max_value(game, state, float('-inf'), float('inf'), player, remaining_time, time_start, depth, f_move)
    return move


def max_value(game: Game, state: State, alpha: float, beta: float, player: str, remaining_time: float,
              time_start: float, depth: float, f_move=None):
    ## remplacer terminal par if game.IS-CUTOFF(state, depth) then return game.EVAL(state, player), null
    ## eval = 
    #if game.is_terminal(state) or depth == 0:
     #   return game.utility(state, player), None

    if is_cutOff(game,state,depth,remaining_time,time_start):
        return eval(state,player,game), None

    if time_left(remaining_time, time_start) <= 0:
        raise TimeoutError("timeout")

    v = -float('inf')
    move = None

    actions = game.actions(state)
    if f_move in actions:
        actions.remove(f_move)
        actions = [f_move]+ actions

    for a in actions:
        v2, a2 = min_value(game, result(game, state, a), alpha, beta, player, remaining_time, time_start, depth - 1)
        if v2 > v:
            move, v = a, v2
            alpha = max(alpha, v)
        # pruning
        if v >= beta:
            return v, move
    return v, move


def min_value(game: Game, state: State, alpha: float, beta: float, player: str, remaining_time: float, time_start: float, depth: float):
    
    if is_cutOff(game,state,depth,remaining_time,time_start):
        return eval(state,player,game), None

    if time_left(remaining_time, time_start) <= 0:
        raise TimeoutError("timeout")

    v = float('inf')
    move = None
    for a in game.actions(state):
        v2, a2 = max_value(game, result(game, state, a), alpha, beta, player, remaining_time, time_start, depth - 1)
        if v2 < v:
            move, v = a, v2
            beta = min(beta, v)
        # pruning
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

## somme des value*poids des coups possibles
## on a des features et donc des facteurs qui impacte le jeux
## on a des poids pour  l'importance de chaque facteur
## EVAL(s) =w1f1(s)+w2f2(s)+···+wnfn(s) = n ∑ i=1 wi fi(s),
def eval(state: State, player: str, game:Game):
    ## For terminal states, it must be that EVAL(s,p)=UTILITY(s,p)
    if game.is_terminal(state): 
        return game.utility(state, player)
    
    ## feature 1
    my_x_pieces_left = state.pieces_x[player]
    my_o_pieces_left = state.pieces_o[player]
    opps = 1 - player
    
    opps_x_pieces_left = state.pieces_x[opps]
    opps_o_pieces_left= state.pieces_o[opps]

    w1 = 2

    w1_f1 = ((my_x_pieces_left + my_o_pieces_left)- (opps_x_pieces_left+opps_o_pieces_left))*w1


    ## feature 2 : combien de ma couleur sont sur ma line ou column 
    ## feature 2 : combien de même signe o ou x sont sur ma line ou column 

    last_move = state.last_move
    w2 = 1
    count_l = 0
    count_c = 0
    
    if last_move is not None:
        line = last_move[0]
        column = last_move[1]
        for i in range(6):
            if state.board[line][i] is not None and state.board[line][i][1] == player:
                count_l +=1
            if state.board[i][column] is not None and state.board[i][column][1] == player:
                count_c +=1
            
    w2_f2 = w2 * (count_l + count_c ) 

    ## feature 3 : 
    w3_f3 = 0.2 * len(game.actions(state))

    
    #result 
    result =  w1_f1 + w2_f2 + w3_f3 
    
    return result


def is_cutOff(game: Game,state: State, depth: float, remaining_time: float, time_start: float ):
    if game.is_terminal(state) or depth == 0:
        return True
    
    return False