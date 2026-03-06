
import threading
import time
from process.process import Process

# depend on the abstract contract rather than the concrete class
from scheduler.scheduler_interface import SchedulerInterface


class Cpu:

    def __init__(self, scheduler: SchedulerInterface, id: int, clock = 1):
        self.__scheduler = scheduler
        self.__time_slice = 0
        self.__id = id
        self.__current_process: Process = None
        self.__clock = clock
        self.__running = False
        

    def __str__(self) -> str:
        return f"CPU{self.__id}"
    
    
    def start(self):
        if self.__running:
            raise RuntimeError("core already running")
        self.__running = True
        thread = threading.Thread(target=self.__try_to_execute, args=())
        thread.start()


    def stop(self):
        if not self.__running:
            raise RuntimeError("core is not running")
        self.__running = False


    def is_idle(self) -> bool:
        return self.__current_process == None
    
    
    def set_current_process(self, new_process):
        self.__current_process = new_process

    
    def get_current_process(self) -> Process:
        return self.__current_process
    

    def get_time_slice(self) -> int:
        return self.__time_slice
    

    def get_id(self) -> int:
        return self.__id
    

    def __try_to_execute(self):
        while self.__running:
            if self.__can_execute():
                self.__execute()

            if self.__time_slice == 0 or not self.__can_execute():
                self.__context_switch()
            
            time.sleep(self.__clock)

    
    def __execute(self):
        self.__time_slice -= 1
        self.__current_process.execute()


    def __can_execute(self) -> bool:
        return not self.is_idle() and self.__current_process.can_execute()


    def __context_switch(self):
        self.__current_process, self.__time_slice = self.__scheduler.context_switch(self.__current_process)

