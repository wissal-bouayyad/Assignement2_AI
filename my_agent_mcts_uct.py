import math

from agent import Agent
from oxono import Game
import random

class Node:
    def __init__(self, state):
        self.state = state   #estado del juego
        self.action = None #La accion que me llevo a este nodo
        self.parent_node = None #El nodo anterior, de donde vienes
        self.children_node = [] #lista de acciones posibles
        self.explored = 0 #Int Sirve para saber cuantas veces hemos pasado por este nodo
        self.value = 0.0 #Float Sirve para saber que tan bueno ha sido este nodo, con eso estimas que tna beuna es la jugada

    def add_child(self, node):
        self.children_node.append(node)


class MyAgentMCTS(Agent):
    def __init__(self, player):
        super().__init__(player)

    def act(self, state, remaining_time):

        first_node = Node(state.copy())

        for i in range(500): #de forma momentanea HAY QUE CAMBIARLO
            node = self.select_action(first_node)
            result = self.playout(node.state.copy())
            self.backpropagation(node, result)

        if not first_node.children_node:
            return random.choice(list(Game.actions(state)))

        return max(first_node.children_node, key=lambda c: c.explored).action

    #Por que camino del arbol bajo ahora? ESTE METODO DEBE SER EDITADO
    def select_action(self, node):
        while not Game.is_terminal(node.state): #mientras el juego no haya terminaod ene tse nodo

            #si hay acciones no exploradas -> expandir
            #Si el número de hijos que ya he creado es menor que el número de acciones posibles ...
            if len(node.children_node) < len(Game.actions(node.state)):
                return self.expand(node)
            else:
                node = self.best_child(node)  #CAMBIO
        return node

    def playout(self, state):
        while not Game.is_terminal(state):  #Mientras no se acabe el juego
            action = list(Game.actions(state)) #Vas a hacer una lista de posibles acciones que se pueden realizar en el estado que te encuentras
            choice_act = random.choice(action) #de esas posibels acciones que porias tomar elejiras una
            Game.apply(state, choice_act) #y entonces lanzaras el juego
        return Game.utility(state, self.player) #return si en etsa simualciones se gano o se perdio o quedo en empate

    def backpropagation(self, node, result):
        while node is not None: #mientras node no sea none
            node.explored += 1  #vas a agregar una visita al node
            node.value += result #sumaras el resultado  al nodo
            result = -result #NEW
            node = node.parent_node #el nodo sera el padre del hijo y luego del padre ya si hasta llegar a la raiz

    def expand (self, node):
        actions = Game.actions(node.state)
        created_actions = [child.action for child in node.children_node]

        for action in actions:
            if action not in created_actions:
                new_state = node.state.copy()
                Game.apply(new_state, action)
                child = Node(new_state)
                child.parent_node = node
                child.action = action
                node.add_child(child)
                return child
        return None

    #NEW
    def best_child(self, node, c=1.4):
        best_score = -float('inf')
        best = None

        for child in node.children_node:
            if child.explored == 0:
                return child
            exploit = child.value / child.explored
            explore = c * math.sqrt(2 * math.log(max(1, node.explored)) / child.explored)
            score = exploit + explore

            if score > best_score:
                best_score = score
                best = child

        return best
