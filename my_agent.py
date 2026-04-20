from agent import Agent
from agent_helper_move_ordering import alpha_beta_search
from oxono import Game

class MyAgent(Agent):
    def act(self, state, remaining_time):

        try: 
            return alpha_beta_search(Game, state,remaining_time)    
        except TimeoutError:
            print("timeout")
            return None
            
        


