import random
from pieces import Tile, Dice, Board, Bag, Rules
from agents import Agent
from actions import Turn, Move
from collections import Counter, defaultdict

# game_engine.py
class Game:
    def __init__(self, agents, random):
        # List of agents
        self.agents = agents
        # Set which agent will go first
        self.current_agent_index= 0

        # Define the chance engine for the game
        self.random = random

        # Create a dice for the game
        self.dice = Dice(random)

        # Create a bag full of tiles
        self.bag = Bag(random)

        # Create a board to play on and add the first tiles from the bag
        self.board = Board(self.bag)

        # Create a copy of the rules to play with
        self.rules = Rules()
        #Define a marker to track if the game is over
        self.end_game = False

    def play_game(self):
        turn_count = 1

        # Start the game by getting all agents to pick up 5 tiles
        for agent in self.agents:
            self.bag.refill_agents_hand(agent)

        # Start playing turns
        while self.end_game == False:
            print(f"Starting turn {turn_count}")
            
            # Define the agent who is taking the turn
            agent = self.agents[self.current_agent_index]

            print(f"{agent.name} is playing...")

            # Start a turn for that agent
            current_turn = Turn(turn_count=turn_count, board=self.board, dice=self.dice, bag=self.bag, agent= agent, rules = self.rules)

            # Play the turn
            current_turn.play_turn()

            self.end_game = current_turn.end_game
            
            # Visualise board
            self.board.print_board()

            # Switch to next player
            self.current_agent_index = (self.current_agent_index + 1) % len(self.agents)

            turn_count = turn_count + 1
            print("\n")

            if turn_count == 100:
                self.end_game = True
        print("game ended!")












## Set up the game
if __name__ == "__main__":

    # Create chance engine that will set the game
    seed = 42
    random = random.Random(seed)

    # Create our players for the game
    agent1 = Agent("George",random)
    agent2 = Agent("Adam",random)
    agent3 = Agent("Harriet",random)
    agents = [agent1, agent2, agent3]

    # Create the game and put the players and chance in it
    game = Game(agents, random)

    # Play the game
    game.play_game()


