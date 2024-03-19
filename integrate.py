""" will be integrating the OctoWumpus and the lottery scheduler here """
from Process import Node 
from Process import ProcessTree
from LotteryScheduler import LotteryScheduler
from OctoWumpus import OctoWumpus
from threading import Lock
import time


class Scheduler():
    def __init__(self):
        self.lottery_scheduler = LotteryScheduler() # lottery scheduler instance
        self.octo_wumpus = OctoWumpus(self.lottery_scheduler) # OctoWumpus instance
        self.total_num_processes = 0 # = number of nodes in the tree
        self.node_pid_dictionary = {} # maps nodes to the process ID for quicker access
        self.quanta_value = 5 # init value, can also change this later on
        self.execution_status_dictionary = {} # 0 -> not allowed to begin/pause, 1 --> start, 2 --> finished execution
        self.m = Lock() # for safely accessing self.execution_status_dictionary

    def change_quanta(self, val):
        """ Function to change the size of 1 quanta (amount of time given to each winning process for execution)
        Useful to check how changing the size of the quanta affects the fairness of lottery scheduler."""
        self.quanta_value = val
    
    def add_process(self, pid, phi):
        """Function for adding a process to our scheduler"""
        self.total_num_processes += 1
        node = self.lottery_scheduler.add_process(pid, phi)
        self.node_pid_dictionary[pid] = node
        self.execution_status_dictionary[pid] = 0 # not allowed to begin initially