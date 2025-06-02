from colorama import Fore, Style

# agents.py
class Agent:
    def __init__(self,name,random):
        self.hand = []
        self.name = name
        self.random = random
        self.strategy = None

    def where_to_place(self, board, rules, move):
        
        # Consult the rules and board to see where a tile can go
        legal_placements = rules.get_legal_placements(board)

        # Choose a tile from the agents hand to play (random atm)
        index = self.random.randrange(len(self.hand))
        tile_to_play = self.hand.pop(index)

        # Choose a valid place to play the tile (random atm)
        index = self.random.randrange(len(legal_placements))
        target_location = legal_placements[index]

        ## Finalise the move
        move.tile = tile_to_play
        move.target_location = target_location

        return move

    def where_to_play(self, board, rules, move_list, active_tiles_dict):
        # Decide what each move should be:
        for idx, move in enumerate(move_list):
            # Pick the active tile that this move relates to (if this is move 2 out of 3, it'll pick active tile 2 out of 3)
            active_tile = list(active_tiles_dict.values())[idx]

            # If one of the tiles is 2 high already, develop it by default
            if active_tile.stack_height==2:
                placement = [key for key, val in active_tiles_dict.items() if val == active_tile]
                
                tower_tile = rules.get_tower_tile(active_tile.colour)
                tower_tile.stack_height = 3
                move.tile = tower_tile
                move.target_location = placement[0]
                print("Developed a tower")
            else:
                if active_tile.type == "house":
                    tile_colour = active_tile.colour
                    # Check if agent has any of the colour of the active house in their hand
                    colour_in_hand = self.check_colours_in_hand(tile_colour)

                    # If you have a tile to play
                    if len(colour_in_hand) > 0:
                        # If there are more than one tiles in the agents hand of the right colour, play the lowst value
                        tile_to_play = min(colour_in_hand, key=lambda tile: tile.value)


                        # Find the coordinates of where to place it
                        placement = [key for key, val in active_tiles_dict.items() if val == active_tile]
                        
                        # Amend the stack height
                        tile_to_play.stack_height = 2

                        # Remove the tile from the agents hand ahead of playing it
                        self.hand.remove(tile_to_play)

                        # Define the move
                        move.target_location = placement[0]
                        move.tile = tile_to_play
                        print(f"Developed a house at {move.target_location}")
                    else:
                        pass
                else:
                    pass

        # Filter the move_list to only include the ones that were used
        move_list = [move for move in move_list if move.tile is not None]
        
        return move_list
 
    
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
        turn_options = [ False, True]

        index = self.random.randrange(len(turn_options))

        roll_die = turn_options[index]

        return roll_die
    
    def reveal_hand(self):
        color_map = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "black": Fore.WHITE  # Treat black as white in output
        }

        tile_strings = []
        for tile in self.hand:
            color = color_map.get(tile.colour, Fore.WHITE)
            value = str(tile.value)
            colored_value = f"{color}{value}{Style.RESET_ALL}"
            tile_strings.append(colored_value)

        print(f"{self.name} had: " + ", ".join(tile_strings))
        
        
