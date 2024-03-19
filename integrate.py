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

    def kill_process(self, pid):
        """Kill a process --> join a thread or stop a thread"""
        # remove this process from the binary tree
        # use the dictionary: self.node_pid_dictionary to get the node based upon the pid and remove it from the tree: adjust the tickets 
        # of the processes accordingly because we would not want gaps in our ticket series
        self.total_num_processes -= 1
        self.execution_status_dictionary.pop(pid)
        self.node_pid_dictionary.pop(pid)
        self.lottery_scheduler.delete_node(pid) # TODO: IMPLEMENTED THIS METHOD
    
    def check_execution_status(self, pid):
        """Function for checking the execution statis of a process: whether it is allowed to begin (1), 
        whether it is paused (0) or whether it is finished (2)."""
        self.m.acquire()
        if pid in self.execution_status_dictionary:
            t = self.execution_status_dictionary[pid]
            self.m.release()
            return t
        self.m.release()
        # if the process is not in the dictionary, then it is by default not allowed to begin, so return 0
        return 0

    def mark_finished(self,pid):
        """Function called by the process to mark its status as finished."""
        self.m.acquire()
        self.execution_status_dictionary[pid] = 2 # marked as finished
        self.m.release()

    def pause_process(self, pid):
        """Pause a process/pause a thread's execution""" 
        self.m.acquire()
        if (self.execution_status_dictionary[pid] == 1): # do not overwrite, if the thread has declared that it is finished
            self.execution_status_dictionary[pid] = 0 # send a flag to the thread signaling it to wait.
        self.m.release()
    
    def execute_process_thread(self, pid):
        """Function for signaling a thread to begin execution."""
        # signal thread to begin exeuction
        self.m.acquire() 
        if (self.execution_status_dictionary[pid] == 0): # do not overwrite, if the thread has declared that it is finished
            self.execution_status_dictionary[pid] = 1 # send a flag to the thread signaling it to begin
        self.m.release()
    
    def epoch_completed(self):
        """Call the OctoWumpus protocol"""
        print("1 quanta has been completed - going to initiate the Octo Wumpus protocol.") 
        self.octo_wumpus.initiate_protocol()
    
    def run_quantas(self):
        """Actual integration code"""
        pass