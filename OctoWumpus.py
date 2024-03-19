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
        fairness_diff = self.calculate_fairness_diff(node)
        
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

    def octoWumpusAlphaInflation_protocol(self):
        """Function is supposed to initiate the Octo-Wumpus Alpha inflation protocol"""
        pass