import random
import copy
from collections import Counter, defaultdict

class Tile:
    def __init__(self, tile_type, colour, value):
        self.type = tile_type
        self.colour = colour
        self.value = value
        self.stack_height = 1

class Dice:
    def __init__(self,random):
        self.random = random
        self.roll()
    
    def roll(self):
        value = self.random.randrange(5) + 1
        return value

class Bag:
    def __init__(self,random):
        self.random = random
        self.create_bag()

    def create_bag(self):
        # Define the parameters
        tile_advanced = ["mill", "reservoir", "library", "forge", "temple", "market"]
        tile_colours = ["red","black","green"]
        tile_numbers = [1,2,3,4,5,6]
        bag =[]

        #Create each faction in turn
        for tile_colour in tile_colours:
            #Create the numbered house tiles
            for tile_number in tile_numbers:
                # 3 of each number
                for _ in range(3):
                    tile = Tile(tile_type="house",colour = tile_colour,value=tile_number)
                    bag.append(tile)
            # Create the advanced tiles
            for tile_advance in tile_advanced:
                tile = Tile(tile_type="advanced",colour = tile_colour,value = tile_advance)
                bag.append(tile)

        self.random.shuffle(bag)
        self.bag = bag

    def draw_tile(self):
        # Picks a random tile
        index = self.random.randrange(len(self.bag))
        # Pops it out the bag list
        return self.bag.pop(index)
    
    def replace_tiles(self, tiles):
        if isinstance(tiles, list):
            for tile in tiles:
                if isinstance(tile, Tile):
                    self.bag.append(tile)
                    self.random.shuffle(self.bag)
    
    def refill_agents_hand(self, agent):
        while len(agent.hand) <5:
            new_tile = self.draw_tile()
            agent.hand.append(new_tile)
            print(f"{agent.name} has refilled their hand to {len(agent.hand)}")

class Board:
    def __init__(self, bag):
        self.create_empty_board()
        self.set_up_board(bag)


    def create_empty_board(self, width=9, height=9):
        self.game_state = {(x, y): None for x in range(width) for y in range(height)}

    def set_up_board(self, bag):

        # Defines the starting position of tiles
        central_5 = [(4,3),(4,4),(4,5),(5,4),(3,4)]

        # Places tiles at the starting positions
        for pos in central_5:
            self.game_state[pos] = bag.draw_tile()
    
    def place_tile(self, move):
        
        (x, y) = move.target_location

        if (x, y) not in self.game_state:
            raise ValueError(f"Position ({x}, {y}) is out of bounds.")

        self.game_state[(x, y)] = move.tile 
    
    def print_board(self):
        width = max(x for (x, _) in self.game_state.keys()) + 1
        height = max(y for (_, y) in self.game_state.keys()) + 1

        print("Current Board State:")
        for y in range(height):
            row = []
            for x in range(width):
                tile = self.game_state.get((x, y))
                
                if tile is None:
                    row.append("  .  ")  # Empty cell
                else:
                    #print(tile, tile.stack_height, tile.type)

                    if tile.type == "tower":
                        row.append(f"  X  ")  # Customize display here
                    elif tile.stack_height == 2:
                        row.append(f"  {str(tile.value)[0]}* ")  # Customize display here
                    elif tile.stack_height == 1:
                        # Use short tile label or initial
                        row.append(f"  {str(tile.value)[0]}  ")  # Customize display here
            print("".join(row))

class Rules:
    def get_legal_placements(self,board):
        directions = [  # 8 directions: diagonals included
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]

        candidate_positions = set()

        for (x, y), tile in board.game_state.items():
            if tile is not None:  # Only consider placed tiles
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    # Only add if the neighbor is in bounds and empty
                    if (nx, ny) in board.game_state.board and board.game_state.board[(nx, ny)] is None:
                        candidate_positions.add((nx, ny))

        return list(candidate_positions)

    def determine_winner(self, board, agents):

        # Step 1: Count tower colours on the board
        tower_colours = []
        for tile in board.values():
            if tile is not None and getattr(tile, 'type', None) == "tower":
                tower_colours.append(tile.colour)

        # Step 2: Determine the winning colour
        colour_counts = Counter(tower_colours)
        winning_colour = max(colour_counts, key=colour_counts.get)

        print(f"Winning tower colour is: {winning_colour}")

        # Step 3: Score each agent
        agent_scores = []
        for agent in agents:
            tiles_of_colour = [tile for tile in agent.hand if tile.colour == winning_colour]

            count = len(tiles_of_colour)
            value = sum(tile.value if isinstance(tile.value, (int, float)) else 1 for tile in tiles_of_colour)

            agent_scores.append({
                'agent': agent,
                'count': count,
                'value': value
            })

        # Step 4: Determine winning agent
        # First by count, then by value
        agent_scores.sort(key=lambda x: (x['count'], x['value']), reverse=True)

        winning_agent = agent_scores[0]['agent']
        print(f"Winning agent is: {winning_agent.name if hasattr(winning_agent, 'name') else winning_agent}")
    
    def is_game_over(self, board):
        # Check win/loss/draw condition
        tower_count = 0
        for tile in board.game_state.values():
            if tile is not None:
                if tile.type == "tower":
                    tower_count = tower_count + 1
                else:
                    pass
        
        if tower_count > 7:
            end_game = True
        else:
            end_game = False
        
        return end_game

    def get_activated_tiles(self, game_state, dice_value):
        directions = [  # 8 directions: diagonals included
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]

        # Create a list of activated tiles to fill
        actived_tiles = dict()


        # Filter to get board tiles with number on dice
        for x,y in game_state.items():
            if y is not None:
                if y.value == dice_value:
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
