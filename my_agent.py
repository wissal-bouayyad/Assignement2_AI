from agent import Agent
from agent_helper_baseline import alpha_beta_search
from oxono import Game

class MyAgent(Agent):
    def act(self, state, remaining_time):
        timeout=remaining_time
        try:
            if timeout >0:
                return alpha_beta_search(Game, state)    
        except:
            print("timeout")
            return None
        


