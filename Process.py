class Currency:
    def __init__(self, id):
        self.currency_id = id # every currency should start with an ID

class Node:
    def __init__(self, pid, tickets, currency_id, left_node=None, right_node=None, left_range=0, right_range=0, height=1, parent=None):
        self.pid = pid
        self.tickets = tickets
        self.currency_id = currency_id
        self.left_node = left_node
        self.right_node = right_node
        self.left_range = left_range
        self.right_range =  right_range
        self.height = height # by default
        self.turns = 0 # To track how many turns the process has received to execute
        self.parent = parent # Needed for inflation
        self.alive = True # a process is alive by deafult

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

class ProcessTree:
    """This is the process tree that we will iterate over for selecting the winners."""
    def __init__(self):
        self.root = None
    
    def add_node(self, node):
        """Function to add a node in the process tree."""
        if self.root is None:
            # No root present --> new node is going to be the root node
            self.root = node
            self.root.left_node = None
            self.root.right_node = None
        else:
            self.add_node_helper(self.root, node) # add it as a child of another node
    
    def add_node_helper(self, parent_node, node):
        if node.left_range > parent_node.right_range:
            # node should be the right child
            if parent_node.right_node is None:
                parent_node.right_node = node
                # children of the newly added node should be None
                parent_node.right_node.left_node = None
                parent_node.right_node.right_node = None
                parent_node.right_node.height = parent_node.height + 1
            else:
                self.add_node_helper(parent_node.right_node, node)
        elif node.right_range < parent_node.left_range:
            # node should be the left child
            if parent_node.left_node is None:
                parent_node.left_node = node
                # children of the newly added node should be None
                parent_node.left_node.left_node = None
                parent_node.left_node.right_node = None
                parent_node.left_node.height = parent_node.height + 1
            else:
                self.add_node_helper(parent_node.left_node, node)
    
    def find_lottery_winner_helper(self, node, t):
        if node is None: # base case
            return None
        if node.left_range <= t <= node.right_range:
            # winner found!
            return node
        if t < node.left_range:
            # recurse over the left subtree
            if node.left_node is not None:
                return self.find_lottery_winner_helper(node.left_node, t)
        else:
            # recurse over the right subtree
            if node.right_node is not None:
                return self.find_lottery_winner_helper(node.right_node, t)

    def find_lottery_winner(self, winning_ticket):
        """Function to return the winning node."""
        w = self.find_lottery_winner_helper(self.root, winning_ticket)
        if w is None:
            print("An invalid winner was selected -> winner is not in the process tree.")
            return None
        return w
    
    def accumulate_alive_nodes(self, root_node):
        """Returns a list of all the dead nodes in a graph."""
        if root_node == None:
            return [] # base case
        if root_node.alive == True:
            # if the node is alive
            return [root_node] + self.accumulate_alive_nodes[root_node.left_node] + self.accumulate_alive_nodes[root_node.right_node]
        return [] # no alive node
    def remove_nodes(self):
        alive_node_list = self.accumulate_alive_nodes(self.root)
        # we are recreating the tree
        # step 1 --> initialize the root node to None
        self.root = None
        # start adding the nodes again with new ranges
        current_ticket_number = 0 # will always assign it from 0
        for node in alive_node_list:
            node.left_range = current_ticket_number
            node.right_range = current_ticket_number + node.tickets
            current_ticket_number += 1 # to avoid range overlap
            self.add_node(node) # reacreating the tree by adding the alive nodes with new ranges
        return current_ticket_number, len(alive_node_list)
