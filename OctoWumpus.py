from Process import Node 
from Process import ProcessTree 
import heapq

class OctoWumpus:
    def __init__(self, lottery_scheduler):
        # default protocol = 1 # queue
        # switch to 2 for alpha inflation
        # 0 for basic lottery scheduler
        self.protocol = 1
        self.lottery_scheduler = lottery_scheduler
        self.prioriy_queue = [] # wumpus queue

    def switch_protocol(self, p):
        self.protocol = p
    
    def initiate_protocol(self):
        """This funciton should get triggered after each epoch. """
        if self.protocol == 0:
            # Basic lottery scheduler - No Octo-Wumpus protocol
            pass
        elif self.protocol == 1:
            # initiate the queue protocol
            self.octoWumpusQueue_protocol()
        elif self.protocol == 2:
            # initiate the alpha inflation protocol
            self.octoWumpusAlphaInflation_protocol()
        else:
            # Incorrect protocol choice
            raise ValueError("Invalid protocol. Protocol must be 0 or 1 or 2.")
        
    def calculate_fairness_diff(self, node):
        """Helper function to calculate starvation of a process node"""
        expected_fairness = node.tickets / self.lottery_scheduler.total_num_tickets
        actual_fairness = node.turns / self.lottery_scheduler.total_num_tickets
        return expected_fairness - actual_fairness
    
    def add_starved_processes_to_queue(self, node):
        """Function to recursively search the prcess tree for fairness starved nodes"""
        
        if node is None:
            return
        
        # Calculate the fairness starvation of current node
        fairness_diff = calculate_fairness_diff(node)
        
        # Check if node is starved off of fairness
        if fairness_diff > 0:
            # USing negative value since we want most starved first
            heapq.heappush(self.prioriy_queue, (-fairness_diff, node))
        
        # Recurse on right sub tree
        self.add_starved_processes_to_queue(node.right_node)
        # Recurse on left sub tree
        self.add_starved_processes_to_queue(node.left_node)
    
    def octoWumpusQueue_protocol(self):
        """Function initiates the Octo-Wumpus queue protocol"""
        self.priority_queue = []

        self.add_starved_processes_to_queue(self.lottery_scheduler.process_tree.root)

        return self.priority_queue

    def calculate_alpha(self, node, nodes_and_alphas):
        # Function to calculate alpha for a given node
        # using inverse of starvation factor 
        # minimum value starvation factor can have is 2
        if node is None:
            return 
        if node.turns < node.tickets:
            alpha = max(2, node.tickets / max(1, node.turns))
            nodes_and_alphas.append((node, alpha))

        self.calculate_alpha(node.left_node, nodes_and_alphas)
        self.calculate_alpha(node.right_node, nodes_and_alphas)

    def octoWumpusAlphaInflation_protocol(self):
        """Function is supposed to initiate the Octo-Wumpus Alpha inflation protocol"""
        
        nodes_and_alphas = []
        # Find starved processes and calculate their inflaction value
        self.calculate_alpha(self.lottery_scheduler.process_tree.root)
        # Sort the starved processes by range 
        nodes_and_alphas.sort(key=lambda node: node[1].left_range, reverse=True)
        for node, alpha in nodes_and_alphas:
            # Count the increase in the number of tickets for the node
            extra_tickets = int(node.tickets * (alpha - 1))
            node.tickets = node.tickets + extra_tickets
            # Recursively update the ticket ranges of nodes right subtree only
            self.lottery_scheduler.process_tree.update_ranges(node.right_node, extra_tickets)
            if node.parent.left_node == node:
                # Propogate the range update to parent and its right sibling node
                self.lottery_scheduler.process_tree.update_ranges_upwards(node.parent, extra_tickets)