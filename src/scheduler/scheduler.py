from queue import Queue, PriorityQueue

import random
from typing import Optional, Tuple

from prioritized_item import PrioritizedItem
from process.process import Process, ProcessType
from scheduler.scheduler_interface import SchedulerInterface
from process.interactive_process import InteractiveProcess
from scheduler.id_generator import IdGenerator

class Scheduler(SchedulerInterface):

    def __init__(self, time_slice = 5):
        self.__id_generator = IdGenerator()

        self.__system_processes = Queue()
        self.__interactive_processes: PriorityQueue[PrioritizedItem] = PriorityQueue()
        self.__batch_processes = Queue()

        self.__waiting_processes: list[InteractiveProcess] = []
        self.__dead_processes: list[Process] = []

        self.__time_slice = time_slice
        

    def add_process(self, process: Process):
        pid = self.__get_next_pid()
        process.set_pid(pid)
        self.__add_process_to_ready(process)


    """Receives a process and gives another one and a time slice"""
    def context_switch(self, process: Optional[Process]) -> Tuple[Optional[Process], int]:
        if process:
            self.__schedule_process(process)

        type = self.__choose_process_type()

        if type == ProcessType.SYSTEM_PROCESS:
            return self.__system_processes.get(), self.__time_slice
        if type == ProcessType.INTERACTIVE_PROCESS:
            # return the actual process object, not the PrioritizedItem wrapper
            return self.__pop_interactive(), self.__time_slice
        elif type == ProcessType.BATCH_PROCESS:
            return self.__batch_processes.get(), self.__time_slice
        
        return None, 0
    

    def __schedule_process(self, process: Process):
        if process.is_over():
           self.__dispatch_process(process)
        
        elif process.can_execute():
            self.__add_process_to_ready(process)

        else:
            self.__waiting_processes.append(process)


    def __dispatch_process(self, process: Process):
        self.__dead_processes.append(process)
        self.__retrieve_pid(process.get_pid())


    def __choose_process_type(self) -> Optional[ProcessType]:
        options = self.__create_process_type_options()
        if len(options) == 0:
            return None
        
        return random.choice(options)
    
        
    """
    Return a list with the type options, notice that some types appear more than others,
    which means some types have higher priorities
    """
    def __create_process_type_options(self) -> list[ProcessType]:
        options = []
        if not self.__system_processes.empty():
            options.extend([ProcessType.SYSTEM_PROCESS, ProcessType.SYSTEM_PROCESS,
                            ProcessType.SYSTEM_PROCESS, ProcessType.SYSTEM_PROCESS])

        if not self.__interactive_processes.empty():
            options.extend([ProcessType.INTERACTIVE_PROCESS, ProcessType.INTERACTIVE_PROCESS,
                            ProcessType.INTERACTIVE_PROCESS])

        if not self.__batch_processes.empty():
            options.extend([ProcessType.BATCH_PROCESS, ProcessType.BATCH_PROCESS])

        return options


    def __get_next_pid(self) -> int:
        pid = self.__id_generator.get_next_id()
        return pid
    
    def __retrieve_pid(self, id: int):
        self.__id_generator.retrieve_id(id)
    
    def wait_process_check(self):

        for process in self.__waiting_processes:
            process.wait()

            if process.can_execute():
                self.__wake_up_process(process)


    def __wake_up_process(self, process: Process):
        self.__waiting_processes.remove(process)
        self.__add_process_to_ready(process)

    
    def __add_process_to_ready(self, process: Process):
        type = process.get_type()

        if type == ProcessType.SYSTEM_PROCESS:
            self.__system_processes.put(process)
        elif type == ProcessType.INTERACTIVE_PROCESS:
            self.__enqueue_interactive(process)
        elif type == ProcessType.BATCH_PROCESS:
            self.__batch_processes.put(process)


    """
    wrap entries in a PrioritizedItem so the queue can order them
    solely by priority. Tuples would cause a TypeError when two
    priorities are equal, because Python would try to compare the
    InteractiveProcess instances themselves.
    """
    def __enqueue_interactive(self, process: InteractiveProcess):
        self.__interactive_processes.put(PrioritizedItem(process.get_priority(), process))


    def __pop_interactive(self) -> InteractiveProcess:
        return self.__interactive_processes.get().item


    def has_alive_processes(self) -> bool:
        
        if not self.__system_processes.empty():
            return True
        
        if not self.__interactive_processes.empty():
            return True
        
        if not self.__batch_processes.empty():
            return True
        
        if len(self.__waiting_processes) != 0:
            return True
        
        return False
    

    def get_time_slice(self) -> int:
        return self.__time_slice

    def get_system_processes(self) -> list[Process]:
        return list(self.__system_processes.queue)

    def get_interactive_processes(self) -> list[Process]:
        temp = list(self.__interactive_processes.queue)
        return [p.item for p in temp]

    def get_batch_processes(self) -> list[Process]:
        return list(self.__batch_processes.queue)

    def get_waiting_processes(self) -> list[Process]:
        return list(self.__waiting_processes)

    def get_dead_processes(self) -> list[Process]:
        return list(self.__dead_processes)