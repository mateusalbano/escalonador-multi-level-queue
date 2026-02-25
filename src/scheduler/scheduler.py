import queue

import random
import threading
import time

from cpu import Cpu
from prioritized_item import PrioritizedItem
from process.process import Process
from scheduler.scheduler_interface import SchedulerInterface

class Scheduler(SchedulerInterface):

    def __init__(self, time_slice = 5, n_cpus = 4, clock = 1):
        self.__next_pid = 0
        self.__system_processes = queue.Queue()
        self.__interactive_processes = queue.PriorityQueue()
        self.__batch_processes = queue.Queue()
        self.__wait_processes = []
        self.__cpus = []

        for i in range(n_cpus):
            self.__cpus.append(Cpu(self, i, clock))

        self.__dead_processes = []
        self.__clock = clock
        self.__time_slice = time_slice
        self.__started = False


    def start(self):
        if self.__started:
            raise RuntimeError("scheduler already started")
        self.__started = True

        self.__start_wait_process_check()
        self.__start_cpus()


    def __start_wait_process_check(self):
        thread = threading.Thread(target=self.__wait_process_check, args=())
        thread.start()


    def __start_cpus(self):
        for cpu in self.__cpus:
            cpu.start()


    def stop(self):
        if not self.__started:
            raise RuntimeError("scheduler is not running")
        
        self.__started = False
        for cpu in self.__cpus:
            cpu.stop()
        

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


    def __wait_process_check(self):
        while self.__started:

            ready_process_list = []

            for process in self.__wait_processes:
                process.wait()

                if process.can_execute():
                    ready_process_list.append(process)

            self.__wake_up_process_list(ready_process_list)
            time.sleep(self.__clock)


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

    def __enqueue_interactive(self, process: Process):

        # wrap entries in a PrioritizedItem so the queue can order them
        # solely by priority.  Tuples would cause a TypeError when two
        # priorities are equal, because Python would try to compare the
        # InteractiveProcess instances themselves.
        self.__interactive_processes.put(PrioritizedItem(process.get_priority(), process))

    def __pop_interactive(self) -> Process:
        return self.__interactive_processes.get().item
    
    # def get_context(self) -> str:
    #     sc = SchedulerContext(self)
    #     return sc.get()

    def is_over(self) -> bool:
        for cpu in self.__cpus:
            if not cpu.is_idle():
                return False
        
        if not self.__system_processes.empty():
            return False
        
        if not self.__interactive_processes.empty():
            return False
        
        if not self.__batch_processes.empty():
            return False
        
        if len(self.__wait_processes) != 0:
            return False
        
        return True
    
    def started(self) -> bool:
        return self.__started

    def get_time_slice(self) -> int:
        return self.__time_slice

    def get_clock(self) -> int:
        return self.__clock

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
    
    def get_cpus(self) -> list[Cpu]:
        return list(self.__cpus)