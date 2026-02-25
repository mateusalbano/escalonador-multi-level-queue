
import threading
import time
from process.process import Process

# depend on the abstract contract rather than the concrete class
from scheduler.scheduler_interface import SchedulerInterface


class Cpu:

    def __init__(self, scheduler: SchedulerInterface, core_id: int, clock = 1):
        self.__scheduler = scheduler
        self.__time_slice = 0
        self.__core_id = core_id
        self.__current_process = None
        self.__clock = clock
        self.__started = False
        
    def start(self):
        if self.__started:
            raise RuntimeError("core already started")
        self.__started = True
        thread = threading.Thread(target=self.__execute, args=())
        thread.start()

    def stop(self):
        if not self.__started:
            raise RuntimeError("core is not running")
        self.__started = False

    def is_idle(self) -> bool:
        return self.__current_process == None
    
    def set_current_process(self, new_process):
        self.__current_process = new_process
    
    def get_current_process(self) -> Process:
        return self.__current_process

    def get_time_slice(self) -> int:
        return self.__time_slice

    def get_core_id(self) -> int:
        return self.__core_id
    
    def __execute(self):
        while self.__started:
            if self.__can_execute():
                self.__current_process.execute()
                self.__decrement_time_slice()
            else:
                self.__context_switch()

            time.sleep(self.__clock)

    def __can_execute(self) -> bool:
        return not self.is_idle() and self.__current_process.can_execute()
    
    def __decrement_time_slice(self):
        self.__time_slice -= 1

        if self.__time_slice == 0:
            self.__context_switch()

    def __context_switch(self):
        self.__current_process, self.__time_slice = self.__scheduler.context_switch(self.__current_process)

