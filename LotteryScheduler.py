from Process import Node
from Process import ProcessTree
from Lottery_pick_RNG import xorshift 
import math
class LotteryScheduler:
    def __init__(self):
        self.process_tree = ProcessTree() # Create a process tree for the scheduler
        self.base_tickets = 20 # initial number of tickets
        self.range_lower = 0 # Smallest ticket number (currently 0 but can be initialized to some value)
        self.range_upper = self.range_lower # Largest ticket number (0 initilaized)
        self.seed0 = 12345 # state or seed 1 for RNG
        self.seed1 = 67890 # State or seed 2 for RNG
        self.total_num_tickets = 0
        
    def choose_winner(self):
        # Set the initial internal states for xorshift pick
        seed = [self.seed0, self.seed1]
        # Call the xorshift algorithm to pick a winner within a range
        winning_ticket, updated_seed = xorshift(seed, self.range_lower, self.range_upper)
        # Update seeds to prepare for next picking
        self.seed0, self.seed1 = updated_seed

        return winning_ticket
    
    def add_process(self, process_id, phi = 0):
        num_t = math.ceil(self.base_tickets * (1 + phi))
        self.total_num_tickets += num_t
        new_node = Node(process_id, num_t, 0, 
                        None, None, 
                        self.range_upper, self.range_upper + num_t)
        self.range_upper += num_t
        self.process_tree.add_node(new_node)
        return new_node

    def change_base_tickets(self, new_base_tickets):
        self.base_tickets = new_base_tickets


