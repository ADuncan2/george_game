
class Move:
    def __init__(self):
        self.type = None
        self.tile = None
        self.target_location = None


class Turn:
    def __init__(self, turn_count, board, dice, bag, agent, rules):
        self.move = list()
        self.end_turn = False
        self.board = board
        self.dice = dice
        self.bag = bag
        self.agent = agent
        self.turn_count = turn_count
        self.rules = rules
        self.end_game = False

    def play_turn(self):
        
        # Decide if to roll or place a tile
        roll_die = self.agent.decide_roll_or_place()

        # If decided to place a tile
        if roll_die == False:
            # Create 1 move
            move = Move()
            
            # Get the agent to define the move
            move = self.agent.where_to_place(self.board.game_state, self.rules, move)

            # Play the move
            move_list = [move]
            self.play_moves(move_list)
            print(f"{self.agent.name} placed a tile")

        elif roll_die == True:
            # Roll the dice
            dice_value = self.dice.roll()

            print(f"{self.agent.name} rolled a {dice_value}")

        # Refill the players hand to 5
        self.bag.refill_agents_hand(self.agent)

    def play_moves(self, move_list):
        for move in move_list:
            self.board.place_tile(move)
            
            # Check if that move ended the game:

            self.end_game = self.rules.is_game_over(self.board)
            if self.end_game == True:
                print("game ended!")
                break
            else:
                pass