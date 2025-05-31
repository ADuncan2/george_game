
# agents.py
class Agent:
    def __init__(self,name,random):
        self.hand = []
        self.name = name
        self.random = random
        self.strategy = None

    def where_to_place(self, game_state, rules, move):
        
        # Consult the rules and board to see where a tile can go
        legal_placements = rules.get_legal_placements(game_state)

        # Choose a tile from the agents hand to play (random atm)
        index = self.random.randrange(len(self.hand))
        tile_to_play = self.hand.pop(index)

        # Choose a valid place to play the tile (random atm)
        target_location = self.random.randrange(len(legal_placements))

        ## Finalise the move
        move.tile = tile_to_play
        move.target_location = target_location

        return move

        

    # def select_actions(self, turn):

    #     if turn.turn_type == "place_tile":
    #         # Select a random tile from hand
    #         index = self.random.randrange(len(self.hand))
    #         tile_to_play = self.hand.pop(index)

    #         placement = turn.legal_actions[random.randrange(len(turn.legal_actions))]

    #         turn.move = {placement: tile_to_play}
    #         print(f"{self.name} placed a tile")
            
    #         turn.end_turn = True
    #     else:
    #         # Roll the dice
    #         dice = self.random.randrange(5) + 1
    #         print(f"{self.name} rolled a {dice}")

    #         # Find the tiles that are activated by the throw
    #         activated_tiles = self.get_activated_tiles(turn,dice)

    #         # Look through your hand to see if you can develop any of the active houses
    #         for tile in activated_tiles.values():
    #             if tile.stack_height==2:
    #                 placement = [key for key, val in activated_tiles.items() if val == tile]
                    
    #                 tower_tile = Tile("tower", tile.colour, "X")
    #                 tower_tile.stack_height = 3
    #                 turn.move[placement[0]] = tower_tile
    #                 print("Developed a tower")
    #             else:
    #                 if tile.type == "house":
    #                     tile_colour = tile.colour
    #                     # Check if agent has any of the colour of the active house in their hand
    #                     colour_in_hand = self.check_colours_in_hand(tile_colour)

    #                     # If you have a tile to play
    #                     if len(colour_in_hand) > 0:
    #                         # If there are more than one tiles in the agents hand of the right colour, play the lowst value
    #                         tile_to_play = min(colour_in_hand, key=lambda tile: tile.value)


    #                         # Find the coordinates of where to place it
    #                         placement = [key for key, val in activated_tiles.items() if val == tile]
                            
    #                         # Amend the stack height
    #                         tile_to_play.stack_height = 2

    #                         # Remove the tile from the agents hand ahead of playing it
    #                         self.hand.remove(tile_to_play)

    #                         # Put a move
    #                         turn.move[placement[0]] = tile_to_play
    #                         print("Developed a house")
    #                     else:
    #                         pass
    #                 else:
    #                     pass

    #         turn.end_turn = True


    #     return turn
    
    def check_colours_in_hand(self,colour):
        tile_of_colour = list()
        for tile in self.hand:
            if tile.colour == colour and tile.type=="house":
                tile_of_colour.append(tile)
            else:
                pass
        return tile_of_colour

    def decide_roll_or_place(self):
        # Options to the question 'am I going to roll die?'
        turn_options = [True, False]

        index = self.random.randrange(len(turn_options))

        roll_die = turn_options[index]

        return roll_die
