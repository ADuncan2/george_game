import random
from agents import Agent, Tile, Turn


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
        pass

    def place_tile(self, move):
        if not isinstance(move, dict) or len(move) != 1:
            raise ValueError("Input must be a single-item dictionary of the form {(x, y): tile}")

        (x, y), tile = next(iter(move.items()))

        if (x, y) not in self.board:
            raise ValueError(f"Position ({x}, {y}) is out of bounds.")

        if self.board[(x, y)] is not None:
            raise ValueError(f"Position ({x}, {y}) is already occupied.")

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
            turn = agent.select_action(turn = turn)

            if turn.turn_type=="place_tile":
                # Place the move selected
                self.place_tile(turn.move)
                print(f"{agent.name} placed a tile")
            else:
                pass

            # Refill the players hand to 5
            self.refill_agents_hand(agent)


    def play_game(self):
        turn_count = 1
        while self.game_ended == False:
            print(f"Starting turn {turn_count}")

            # Visualise board
            self.print_board()

            # Find the possible moves based on the board condition
            legal_actions = self.get_legal_placements()
            
            # Start the turn
            turn = Turn(game_state= self.board, legal_actions=legal_actions, turn_count = turn_count)

            # Define the agent who is taking the turn
            agent = self.agents[self.current_agent_index]

            print(f"{agent.name} is playing...")

            # Get the agent to play the turn
            self.play_turn(turn, agent)

            # Switch to next player
            self.current_agent_index = (self.current_agent_index + 1) % len(self.agents)

            turn_count = turn_count + 1
            print("\n")
    
    def print_board(self):
        width = max(x for (x, _) in self.board.keys()) + 1
        height = max(y for (_, y) in self.board.keys()) + 1

        print("Current Board State:")
        for y in range(height):
            row = []
            for x in range(width):
                tile = self.board.get((x, y))
                if tile is None:
                    row.append(" . ")  # Empty cell
                else:
                    # Use short tile label or initial
                    row.append(f" {str(tile.value)[0]} ")  # Customize display here
            print("".join(row))













## Set up the game
if __name__ == "__main__":
    agent1 = Agent("George")
    agent2 = Agent("Adam")
    agent3 = Agent("Harriet")
    agents = [agent1, agent2, agent3]
    game = Game(agents =agents, seed=42)

    game.play_game()


