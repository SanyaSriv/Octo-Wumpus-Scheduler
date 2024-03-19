class Currency:
    def __init__(self, id):
        self.currency_id = id # every currency should start with an ID

class Node:
    def __init__(self, tickets, currency_id, left_node=None, right_node=None, left_range=0, right_range=0, height=1, parent=None):
        self.tickets = tickets
        self.currency_id = currency_id
        self.left_node = left_node
        self.right_node = right_node
        self.left_range = left_range
        self.right_range =  right_range
        self.height = height # by default
        self.turns = 0 # To track how many turns the process has received to execute
        self.parent = parent # Needed for inflation

        # important features for the OctoWumpus protocol
        # these are the amount of chances this process got in 1 epoch
        self.num_lottery_chances = 0
    
    def change_num_tickets(self, new_number_tickets, left_range, right_range):
        self.tickets = new_number_tickets
        self.left_range = left_range
        self.right_range = right_range
    
    def change_currency_id(self, new_id):
        self.currency_id = new_id
    
    def reset_num_lottery_chances(self):
        """Should reset after every epoch."""
        self.num_lottery_chances = 0