import copy
import time
from oxono import State, Game

from agent import Agent


class MyAgent(Agent):
    def act(self, state, remaining_time):

        try:
            return Iterative_deepening_alpha_beta_search(Game, state, remaining_time)
        except TimeoutError:
            print("timeout")
            return None


def Iterative_deepening_alpha_beta_search(game: Game, state: State, remaining_time: float):
    for depth in range(0, 100):
        move = None
        try:
            result = alpha_beta_search(game, state, remaining_time, depth)
            if result != (None, None):
                move = result
        except TimeoutError:
            print("timeout")
            return move
        return move


def alpha_beta_search(game: Game, state: State, remaining_time: float, depth: float):
    """help chose the best action"""
    # remaining time gestion
    time_start = time.time()
    if time_left(remaining_time, time_start) <= 0:
        raise TimeoutError("timeout")

    player = game.to_move(state)
    value, move = max_value(game, state, float('-inf'), float('inf'), player, remaining_time, time_start, depth)
    return move


def max_value(game: Game, state: State, alpha: float, beta: float, player: str, remaining_time: float,
              time_start: float, depth: float):
    if game.is_terminal(state) or depth < 0:
        return game.utility(state, player), None

    if time_left(remaining_time, time_start) <= 0:
        raise TimeoutError("timeout")

    v = -float('inf')
    move = None
    for a in game.actions(state):
        v2, a2 = min_value(game, result(game, state, a), alpha, beta, player, remaining_time, time_start, depth - 1)
        if v2 > v:
            move, v = a, v2
            alpha = max(alpha, v)
        # pruning
        if v >= beta:
            return v, move
    return v, move


def min_value(game: Game, state: State, alpha: float, beta: float, player: str, remaining_time: float,
              time_start: float, depth: float):
    if game.is_terminal(state) or depth < 0:
        return game.utility(state, player), None

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
    copy_state = copy.deepcopy(state)
    game.apply(copy_state, action)
    return copy_state


def time_left(remaining_time: float, time_start: float):
    return remaining_time - (time.time() - time_start)