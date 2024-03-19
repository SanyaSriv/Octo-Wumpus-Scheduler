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
        self.epoch_wumpus_queue = [] # reset for each sepoch

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
        print("1 epoch has been completed - going to initiate the Octo Wumpus protocol.") 
        if self.octo_wumpus.protocol == 1: # queue
            self.epoch_wumpus_queue = self.octo_wumpus.initiate_protocol()
            print("Current Wumpus Queue: ", self.epoch_wumpus_queue)
        else:
            self.octo_wumpus.initiate_protocol() # alpha inflation
        
    def run_quantas(self):
        """Actual integration code"""
        quanta_count = 0
        while self.total_num_processes >= 1:
            # we will keep selecting winners till there is a single process in our scheduler
            winning_ticket = self.lottery_scheduler.choose_winner()
            winning_process = self.lottery_scheduler.process_tree.find_lottery_winner(winning_ticket) # should return a node
            winning_process_pid = winning_process.pid
            print("Winning process in quanta: {} is: {}".format(quanta_count, winning_process_pid)) # printing some stats
            start_time = time.time()
            end_time = start_time + (self.quanta_value / 1000000) # finish executing this because the quanta is over 
            self.execute_process_thread(winning_process_pid) # start executing this process
            while time.time() < end_time:
                continue # execute this thread for quanta amount of time
            self.pause_process(winning_process_pid) # quanta is over -> pause process
            if self.check_execution_status(winning_process_pid) == 2:
                self.kill_process(winning_process_pid) # is process has declared completion, kill it
            quanta_count += 1
            if (quanta_count % self.lottery_scheduler.total_num_tickets == 0):
                # 1 epoch has been completed
                self.epoch_completed()

                # execute the wumpus queue
                # note: we do not need to check the value of self.octo_wumpus.protocol here
                # if self.octo_wumpus.protocol was not 1, then the length of the queue would
                # automatically be 0.
                if len(self.octo_wumpus_queue) > 0:
                    # execute the processes for the quantas they could not get executed
                    print("Executing the Wumpus Queue: ".format(self.octo_wumpus_queue))
                    for i in range(0, len(self.octo_wumpus_queue)):
                        node = self.octo_wumpus_queue[i]
                        quantas_left = node.tickets - node.turns
                        total_execution_time = self.quanta_value * quantas_left # total time this node will get to execute
                        print("Executing process: {} for {} quantas.".format(node.pid, quantas_left))
                        start_time = time.time()
                        end_time = start_time + (total_execution_time / 1000000)
                        self.execute_process_thread(node.pid) # start executing this process
                        while time.time() < end_time:
                            continue # execute the process
                        self.pause_process(node.pid) # quanta is over -> pause process
                        if self.check_execution_status(node.pid) == 2:
                            self.kill_process(node.pid) # is process has declared completion, kill it
                    self.octo_wumpus_queue = [] # reset for the next epoch
                print("Next epoch begin: {}".format((quanta_count % self.lottery_scheduler.total_num_tickets) + 1))
    