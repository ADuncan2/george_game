
class Move:
    def __init__(self):
        self.type = None
        self.tile = None
        self.target_location = ()


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
            move = self.agent.where_to_place(self.board, self.rules, move)

            # Play the move
            move_list = [move]
            self.play_moves(move_list)
            print(f"{self.agent.name} placed a tile")

        elif roll_die == True:
            # Roll the dice
            dice_value = self.dice.roll()

            print(f"{self.agent.name} rolled a {dice_value}")

            # See which houses are activated by the roll, this determines the number of moves you could make (not including rerolls)
            active_tiles_dict = self.rules.get_activated_tiles(self.board,dice_value)

            # Create a list of moves
            move_list = []

            # Create a move object for each potential move (they don't all need to be used)
            for _ in range(len(active_tiles_dict)):
                move = Move()
                move_list.append(move)
            
            # Let agent decide how to use the moves
            move_list = self.agent.where_to_play(self.board,self.rules,move_list,active_tiles_dict)

            # Enact the moves
            self.play_moves(move_list)

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