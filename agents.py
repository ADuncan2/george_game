import random

# agents.py
class Agent:
    def __init__(self,name):
        self.hand = []
        self.name = name

    def select_action(self, turn, game_state, legal_actions):

        # Select a random tile from hand
        index = random.randrange(len(self.hand))
        tile_to_play = self.hand.pop(index)

        placement = legal_actions[random.randrange(len(legal_actions))]

        turn.move = {placement: tile_to_play}
        
        turn.end_turn = True

        return turn


