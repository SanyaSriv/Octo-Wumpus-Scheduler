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
        self.quanta_value = 40 # init value, can also change this later on
        self.execution_status_dictionary = {} # 0 -> not allowed to begin/pause, 1 --> start, 2 --> finished execution
        self.m = Lock() # for safely accessing self.execution_status_dictionary
        self.epoch_wumpus_queue = [] # reset for each sepoch
        self.in_progress = True

    def change_quanta(self, val):
        """ Function to change the size of 1 quanta (amount of time given to each winning process for execution)
        Useful to check how changing the size of the quanta affects the fairness of lottery scheduler."""
        self.quanta_value = val
    
    def reset_turns(self):
        for i in self.node_pid_dictionary:
            node = self.node_pid_dictionary[i]
            node.turns = 0 # resetting it
    
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
        self.m.acquire()
        self.total_num_processes -= 1
        self.execution_status_dictionary.pop(pid)
        self.node_pid_dictionary[pid].alive = False # marking that the node is not alive anymore
        self.node_pid_dictionary.pop(pid)
        self.m.release()
    
    def remove_process_from_tree(self):
        """Funciton to remove a process from the tree after an epoch if it finished midway."""
        num_alive_nodes = self.lottery_scheduler.delete_dead_nodes()
        self.total_num_processes = num_alive_nodes # now these are the processes that are left
        return num_alive_nodes

    def check_execution_status(self, pid):
        """Function for checking the execution statis of a process: whether it is allowed to begin (1), 
        whether it is paused (0) or whether it is finished (2)."""
        while (self.m.acquire() == False):
            print("hfkjhg kfjhgdk fgh kdjfhg")
        if pid in self.execution_status_dictionary:
            t = self.execution_status_dictionary[pid]
            self.m.release()
            return t
        # if the process is not in the dictionary, then it is by default not allowed to begin, so return 0
        self.m.release()
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
        if pid in self.execution_status_dictionary:
            if (self.execution_status_dictionary[pid] == 0): # do not overwrite, if the thread has declared that it is finished
                self.execution_status_dictionary[pid] = 1 # send a flag to the thread signaling it to begin
                self.node_pid_dictionary[pid].turns += 1
        self.m.release()
    
    def epoch_completed(self):
        """Call the OctoWumpus protocol"""
        print("1 epoch has been completed - going to initiate the Octo Wumpus protocol.") 
        if self.octo_wumpus.protocol == 1: # queue
            self.epoch_wumpus_queue = self.octo_wumpus.initiate_protocol()
        else:
            self.octo_wumpus.initiate_protocol() # alpha inflation
        
    def run_quantas(self):
        """Actual integration code"""
        quanta_count = 0
        self.in_progress = True
        while self.total_num_processes >= 1:
            # we will keep selecting winners till there is a single process in our scheduler
            winning_ticket = self.lottery_scheduler.choose_winner()
            winning_process = self.lottery_scheduler.process_tree.find_lottery_winner(winning_ticket) # should return a node
            winning_process_pid = winning_process.pid

            # we need to check if the winning process is the one that has finished execution
            if winning_process_pid not in self.execution_status_dictionary:
                # the lottery scheduler has selected a finisged process for execution
                continue # waste this quanta

            print("Winning process in quanta: {} is: {} with total tickets: {}".format(quanta_count, winning_process_pid, winning_process.tickets)) # printing some stats
            start_time = time.time()
            end_time = start_time + (self.quanta_value / 1000000) # finish executing this because the quanta is over 
            self.execute_process_thread(winning_process_pid) # start executing this process
            while time.time() < end_time:
                continue # execute this thread for quanta amount of time
            self.pause_process(winning_process_pid) # quanta is over -> pause process
            if self.check_execution_status(winning_process_pid) == 2:
                print("Process: {} has finished execution; removing from tree.".format(winning_process_pid))
                self.kill_process(winning_process_pid) # is process has declared completion, kill it
            quanta_count += 1
            # if (self.total_num_processes == 0):
            #     self.in_progress = False
            #     print("I am out of epochs")
            #     return
            print("Values for if", quanta_count, self.lottery_scheduler.total_num_tickets)
            if (quanta_count % self.lottery_scheduler.total_num_tickets == 0):
                # first let's remove all the dead processes
                alive_nodes = self.remove_process_from_tree()
                # if (alive_nodes == 0):
                #     self.in_progress = False # scheduler's job is over
                #     print("I am out of epochs")
                #     return
                # 1 epoch has been completed --> initiate the OctoWumpus protocol
                self.epoch_completed()
                self.lottery_scheduler.process_tree.print_tree(self.lottery_scheduler.process_tree.root)
                # execute the wumpus queue
                # note: we do not need to check the value of self.octo_wumpus.protocol here
                # if self.octo_wumpus.protocol was not 1, then the length of the queue would
                # automatically be 0.
                if len(self.epoch_wumpus_queue) > 0:
                    # execute the processes for the quantas they could not get executed
                    print("Executing the Wumpus Queue: ".format(self.epoch_wumpus_queue))
                    for i in range(0, len(self.epoch_wumpus_queue)):
                        node = self.node_pid_dictionary[self.epoch_wumpus_queue[i][0]]
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
                            print("Process: {} has finished execution; removing from tree.".format(node.pid))
                            self.kill_process(node.pid) # is process has declared completion, kill it
                    self.epoch_wumpus_queue = [] # reset for the next epoch
                    self.remove_process_from_tree()
                if self.lottery_scheduler.total_num_tickets > 0:
                    print("Next epoch begin: {}".format((quanta_count // self.lottery_scheduler.total_num_tickets) + 1))
                
                # Reset quanta for new epoch
                quanta_count = 0
                self.reset_turns()
                print("total tickets", self.lottery_scheduler.total_num_tickets)
        self.in_progress = False # scheduler's job is over
    