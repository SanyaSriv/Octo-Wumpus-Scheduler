from Process import Node 
from Process import ProcessTree 

class OctoWumpus:
    def __init__(self, lottery_scheduler):
        # default protocol = 1 # queue
        # switch to 2 for alpha inflation
        # 0 for basic lottery scheduler
        self.protocol = 1
        self.lottery_scheduler = lottery_scheduler

    def switch_protocol(self, p):
        self.protocol = p
    
    def initiate_protocol(self):
        """This funciton should get triggered after each epoch. """
        if self.protocol == 0:
            # No Octo-Wumpus protocol
            pass
        elif self.protocol == 1:
            # initiate the queue protocol
            self.octoWumpusQueue_protocol()
        elif self.protocol == 2:
            # initiate the alpha inflation protocol
            self.octoWumpusAlphaInflation_protocol()
        else:
            # Incorrect protocol choice
            raise ValueError("Invalid protocol number. Protocol must be 0 or 1 or 2.")
    
    def octoWumpusQueue_protocol(self):
        """Function is supposed to initiate the Octo-Wumpus queue protocol"""
        pass

    def octoWumpusAlphaInflation_protocol(self):
        """Function is supposed to initiate the Octo-Wumpus Alpha inflation protocol"""
        pass