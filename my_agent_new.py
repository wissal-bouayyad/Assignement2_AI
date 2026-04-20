import math

from agent import Agent
from oxono import Game
import random

class Node:
    def __init__(self, parent_node, action_from_parent, state):
        self.parent_node = parent_node
        self.action_from_parent = action_from_parent
        self.state = state
        self.wins = 0
        self.visits = 0
        self.children = []

class mtcs_agent(Agent):
    def __init__(self, player):
        super().__init__(player)

    def act(self, state, remaining_time):
        root = Node(None, None, state)
        for _ in range(1000):
            leaf = self.select(root)
            child = self.expand(leaf)
            if child is None:
                child = leaf
            result = self.simulate(child)
            self.backpropagate(child, result)
        return max(root.children, key=lambda node: node.visits).action_from_parent

    def UCB1(self, node):
        b_value = -float('inf')
        b_child = None
        c = 1.4
        for child in node.children:
            if child.visits == 0:
                return child
        for child in node.children:
            exploitation = child.wins / child.visits
            exploration = c * math.sqrt(math.log(node.visits + 1) / child.visits)
            # exploration = c * math.sqrt(2 * math.log(max(1, node.visits + 1)) / child.visits)
            uct = exploitation + exploration
            if uct > b_value:
                b_value = uct
                b_child = child
        return b_child

    def select(self, node):

        while Game.is_terminal(node.state) is not True:
            if len(node.children) < len(list(Game.actions(node.state))):
                return node
            else:
                node = self.UCB1(node)
        return node

    def expand(self, node):
        actions = Game.actions(node.state)
        b_actions = [child.action_from_parent for child in node.children]

        for action in actions:
            if action not in b_actions:
                n_state = node.state.copy()
                Game.apply(n_state, action)

                n_leaf = Node(node, action, n_state)
                node.children.append(n_leaf)
                return n_leaf
        return None

    def simulate(self, node):
        state = node.state.copy()

        while Game.is_terminal(state) is not True:
            act_choice = random.choice(list(Game.actions(state)))
            Game.apply(state, act_choice)
        return Game.utility(state, self.player)

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            result = -result
            node = node.parent_node