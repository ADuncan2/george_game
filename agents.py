import random
import copy

# agents.py
class Agent:
    def __init__(self,name):
        self.hand = []
        self.name = name
        self.random = None

    def select_action(self, turn):

        turn = self.decide_roll_or_place(turn)

        if turn.turn_type == "place_tile":
            # Select a random tile from hand
            index = self.random.randrange(len(self.hand))
            tile_to_play = self.hand.pop(index)

            placement = turn.legal_actions[random.randrange(len(turn.legal_actions))]

            turn.move = {placement: tile_to_play}
            
            turn.end_turn = True
        else:
            dice = self.random.randrange(5) + 1
            print(f"{self.name} rolled a {dice}")

            activated_tiles = self.get_activated_tiles(turn,dice)

            if

            turn.end_turn = True


        return turn
    
    def decide_roll_or_place(self, turn):
        turn_options = ["roll", "place_tile"]

        index = self.random.randrange(len(turn_options))

        turn.turn_type = turn_options[index]

        return turn

    def get_activated_tiles(self, turn, dice):
        directions = [  # 8 directions: diagonals included
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]

        # Create a list of activated tiles to fill
        actived_tiles = dict()


        # Filter to get board tiles with number on dice
        for x,y in turn.game_state.items():
            if y is not None:
                if y.value == dice:
                    actived_tiles[x] = y
                else:
                    pass
            else:
                pass
        
        actived_tiles_copy = copy.deepcopy(actived_tiles)

        for (x, y), tile in actived_tiles_copy.items():

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # Only add if the neighbor is in bounds and empty
                if (nx, ny) in turn.game_state and turn.game_state[(nx, ny)] is not None and turn.game_state[(nx, ny)].type == "advanced":
                    actived_tiles[(nx, ny)] = turn.game_state[(nx, ny)]
        
        print(f"number of activated tiles: {len(activated_tiles}")
        return actived_tiles

