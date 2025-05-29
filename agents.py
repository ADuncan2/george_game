import random
import copy

class Tile:
    def __init__(self, tile_type, colour, value):
        self.type = tile_type
        self.colour = colour
        self.value = value
        self.stack_height = 1


class Turn:
    def __init__(self, game_state, legal_actions, turn_count):
        self.turn_type = None
        self.move = {}
        self.end_turn = False
        self.game_state = game_state
        self.legal_actions = legal_actions
        self.turn_count = turn_count


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
            # Roll the dice
            dice = self.random.randrange(5) + 1
            print(f"{self.name} rolled a {dice}")

            # Find the tiles that are activated by the throw
            activated_tiles = self.get_activated_tiles(turn,dice)

            # Look through your hand to see if you can develop any of the active houses
            for tile in activated_tiles.values():
                if tile.stack_height==2:
                    placement = activated_tiles.get(tile)
                    turn.move[placement] = Tile("tower", tile.colour, "X")
                    print("Developed a tower")
                else:
                    if tile.type == "house":
                        tile_colour = tile.colour
                        # Check if agent has any of the colour of the active house in their hand
                        colour_in_hand = self.check_colours_in_hand(tile_colour)

                        # If you have a tile to play
                        if len(colour_in_hand) > 0:
                            # If there are more than one tiles in the agents hand of the right colour, play the lowst value
                            tile_to_play = min(colour_in_hand, key=lambda tile: tile.value)
                            # Find the coordinates of where to place it
                            placement = activated_tiles.get(tile)
                            
                            # Amend the stack height
                            tile.stack_height = 2

                            # Put a move
                            turn.move[placement] = tile_to_play
                            print("Developed a house")
                        else:
                            pass
                    else:
                        pass



            turn.end_turn = True


        return turn
    
    def check_colours_in_hand(self,colour):
        tile_of_colour = list()
        for tile in self.hand:
            if tile.colour == colour and tile.type=="house":
                tile_of_colour.append(tile)
            else:
                pass
        return tile_of_colour

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

        for (x, y) in actived_tiles_copy:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # Only add if the neighbor is in bounds and empty
                if (nx, ny) in turn.game_state and turn.game_state[(nx, ny)] is not None and turn.game_state[(nx, ny)].type == "advanced":
                    actived_tiles[(nx, ny)] = turn.game_state[(nx, ny)]
        
        print(f"number of activated tiles: {len(actived_tiles)}")
        return actived_tiles

