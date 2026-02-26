import queue

import random

from prioritized_item import PrioritizedItem
from process.process import Process
from scheduler.scheduler_interface import SchedulerInterface
from process.interactive_process import InteractiveProcess

class Scheduler(SchedulerInterface):

    def __init__(self, time_slice = 5):
        self.__next_pid = 0

        self.__system_processes = queue.Queue()
        self.__interactive_processes = queue.PriorityQueue()
        self.__batch_processes = queue.Queue()

        self.__wait_processes = []
        self.__dead_processes = []

        self.__time_slice = time_slice
        

    def add_process(self, process: Process):
        pid = self.__get_next_pid()
        process.set_pid(pid)
        self.__add_process_to_ready(process)


    def context_switch(self, process: Process):
        if process:
            self.__schedule_process(process)

        type = self.__choose_process_type()

        if type == Process.SYSTEM_PROCESS:
            return self.__system_processes.get(), self.__time_slice
        if type == Process.INTERACTIVE_PROCESS:
            # return the actual process object, not the PrioritizedItem wrapper
            return self.__pop_interactive(), self.__time_slice
        elif type == Process.BATCH_PROCESS:
            return self.__batch_processes.get(), self.__time_slice
        
        return None, 0
    
    def __schedule_process(self, process: Process):
        if process.is_over():
           self.__dead_processes.append(process)
        
        elif process.can_execute():
            self.__add_process_to_ready(process)

        else:
            self.__wait_processes.append(process)


    def __choose_process_type(self) -> int:
        options = self.__create_process_type_options()
        if len(options) == 0:
            return -1
        
        choice = random.randint(0, len(options) - 1)
        return options[choice]
        
    
    def __create_process_type_options(self):
        options = []
        if not self.__system_processes.empty():
            options.extend([Process.SYSTEM_PROCESS, Process.SYSTEM_PROCESS, Process.SYSTEM_PROCESS, Process.SYSTEM_PROCESS])

        if not self.__interactive_processes.empty():
            options.extend([Process.INTERACTIVE_PROCESS, Process.INTERACTIVE_PROCESS, Process.INTERACTIVE_PROCESS])

        if not self.__batch_processes.empty():
            options.extend([Process.BATCH_PROCESS, Process.BATCH_PROCESS])

        return options


    def __get_next_pid(self):
        pid = self.__next_pid
        self.__next_pid += 1
        return pid
    
    def wait_process_check(self):
        ready_process_list = []

        for process in self.__wait_processes:
            process.wait()

            if process.can_execute():
                ready_process_list.append(process)

        self.__wake_up_process_list(ready_process_list)


    def __wake_up_process_list(self, process_list):
        for process in process_list:
            self.__wait_processes.remove(process)
            self.__add_process_to_ready(process) 

    
    def __add_process_to_ready(self, process: Process):
        type = process.get_type()

        if type == Process.SYSTEM_PROCESS:
            self.__system_processes.put(process)
        elif type == Process.INTERACTIVE_PROCESS:
            self.__enqueue_interactive(process)
        elif type == Process.BATCH_PROCESS:
            self.__batch_processes.put(process)

    def __enqueue_interactive(self, process: InteractiveProcess):

        # wrap entries in a PrioritizedItem so the queue can order them
        # solely by priority.  Tuples would cause a TypeError when two
        # priorities are equal, because Python would try to compare the
        # InteractiveProcess instances themselves.
        self.__interactive_processes.put(PrioritizedItem(process.get_priority(), process))

    def __pop_interactive(self) -> InteractiveProcess:
        return self.__interactive_processes.get().item
    
    # def get_context(self) -> str:
    #     sc = SchedulerContext(self)
    #     return sc.get()

    def is_idle(self) -> bool:
        
        if not self.__system_processes.empty():
            return False
        
        if not self.__interactive_processes.empty():
            return False
        
        if not self.__batch_processes.empty():
            return False
        
        if len(self.__wait_processes) != 0:
            return False
        
        return True
    

    def get_time_slice(self) -> int:
        return self.__time_slice

    def get_system_processes(self) -> list[Process]:
        return list(self.__system_processes.queue)

    def get_interactive_processes(self) -> list[Process]:
        return list(self.__interactive_processes.queue)

    def get_batch_processes(self) -> list[Process]:
        return list(self.__batch_processes.queue)

    def get_wait_processes(self) -> list[Process]:
        return list(self.__wait_processes)  

    def get_dead_processes(self) -> list[Process]:
        return list(self.__dead_processes)