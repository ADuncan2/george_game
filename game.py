import random
from agents import Agent, Tile, Turn
from collections import Counter, defaultdict

# game_engine.py
class Game:
    def __init__(self, agents, seed=None):
        self.agents = agents
        self.rng = random.Random(seed)
        for agent in self.agents:
            agent.random = self.rng
        self.create_bag()
        self.set_up_board()
        self.current_agent_index = 0
        self.game_ended = False
        

    def create_empty_board(self, width=9, height=9):
        self.board = {(x, y): None for x in range(width) for y in range(height)}
    
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

        self.rng.shuffle(bag)
        self.bag = bag
    
    def draw_tile(self):
        index = random.randrange(len(self.bag))

        return self.bag.pop(index)

    def refill_agents_hand(self, agent):
        while len(agent.hand) <5:
            new_tile = self.draw_tile()
            agent.hand.append(new_tile)
            print(f"{agent.name} has refilled their hand to {len(agent.hand)}")

    def set_up_board(self):
        # Creates an empty board
        self.create_empty_board()

        # Defines the starting position of tiles
        central_5 = [(4,3),(4,4),(4,5),(5,4),(3,4)]

        # Places tiles at the starting positions
        for pos in central_5:
            self.board[pos] = self.draw_tile()

        for agent in self.agents:
            self.refill_agents_hand(agent)
    

    def is_game_over(self):
        # Check win/loss/draw condition
        tower_count = 0
        for tile in self.board.values():
            if tile is not None:
                if tile.type == "tower":
                    tower_count = tower_count + 1
                else:
                    pass
        
        if tower_count > 7:
            self.game_ended = True

    def place_tile(self, move):
        if not isinstance(move, dict) or len(move) != 1:
            raise ValueError("Input must be a single-item dictionary of the form {(x, y): tile}")

        (x, y), tile = next(iter(move.items()))

        if (x, y) not in self.board:
            raise ValueError(f"Position ({x}, {y}) is out of bounds.")

        self.board[(x, y)] = tile

    def get_legal_placements(self):
        directions = [  # 8 directions: diagonals included
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]

        candidate_positions = set()

        for (x, y), tile in self.board.items():
            if tile is not None:  # Only consider placed tiles
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    # Only add if the neighbor is in bounds and empty
                    if (nx, ny) in self.board and self.board[(nx, ny)] is None:
                        candidate_positions.add((nx, ny))

        return list(candidate_positions)

    def play_turn(self, turn, agent):

        while not turn.end_turn:
            # Get the agent to select the move they want to make
            turn = agent.select_actions(turn = turn)

            if bool(turn.move):
                # Place the move selected
                for key, tile in turn.move.items():
                    
                    move_dict = {key:tile}
                    self.place_tile(move_dict)

            else:
                pass

            # Refill the players hand to 5
            self.refill_agents_hand(agent)


    def play_game(self):
        turn_count = 1
        while self.game_ended == False:
            print(f"Starting turn {turn_count}")

            # Find the possible moves based on the board condition
            legal_actions = self.get_legal_placements()
            
            # Start the turn
            turn = Turn(game_state= self.board, legal_actions=legal_actions, turn_count = turn_count)

            # Define the agent who is taking the turn
            agent = self.agents[self.current_agent_index]

            print(f"{agent.name} is playing...")

            # Get the agent to play the turn
            self.play_turn(turn, agent)
            
            # Visualise board
            self.print_board()
            
            # Check if game is over
            self.is_game_over()

            # Switch to next player
            self.current_agent_index = (self.current_agent_index + 1) % len(self.agents)

            turn_count = turn_count + 1
            print("\n")
        print("game ended!")

        self.determine_winner()

    def determine_winner(self):

        # Step 1: Count tower colours on the board
        tower_colours = []
        for tile in self.board.values():
            if tile is not None and getattr(tile, 'type', None) == "tower":
                tower_colours.append(tile.colour)

        # Step 2: Determine the winning colour
        colour_counts = Counter(tower_colours)
        winning_colour = max(colour_counts, key=colour_counts.get)

        print(f"Winning tower colour is: {winning_colour}")

        # Step 3: Score each agent
        agent_scores = []
        for agent in self.agents:
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
        


    def check_who_won(self):

        tower_colours = {"red": 0,
        "green":0,
        "black":0}
        
        for tile in self.board.values():
            if tile is not None:
                if tile.type == "tower":
                    col = tile.colour
                    current_val = tower_colours[col]
                    tower_colours[col] = current_val + 1
                else:
                    pass
        
        print(tower_colours)
        
        print(tower_colours[max(tower_colours.values())])

    def print_board(self):
        width = max(x for (x, _) in self.board.keys()) + 1
        height = max(y for (_, y) in self.board.keys()) + 1

        print("Current Board State:")
        for y in range(height):
            row = []
            for x in range(width):
                tile = self.board.get((x, y))
                
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













## Set up the game
if __name__ == "__main__":
    agent1 = Agent("George")
    agent2 = Agent("Adam")
    agent3 = Agent("Harriet")
    agents = [agent1, agent2, agent3]
    game = Game(agents =agents, seed=42)

    game.play_game()


