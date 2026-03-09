import threading
import time

from scheduler.scheduler import Scheduler
from cpu import Cpu
from process.process import Process
from scheduler.scheduler_context import SchedulerContext


class SchedulerSimulation:

    def __init__(self, time_slice = 5, n_cpus = 4, clock_rate = 1.0):
        self.__scheduler = Scheduler(time_slice)
        self.__cpus = self.__create_cpus(n_cpus, clock_rate)
        self.__scheduler_context = SchedulerContext(self.__scheduler, self.__cpus)

        self.__running = False
        self.__set_clock_rate(clock_rate)


    def __create_cpus(self, n_cpus: int, clock_rate: float) -> list[Cpu]:

        if n_cpus <= 0:
            raise ValueError("n_cpus must be greater than 0")

        cpus = []
        for i in range(n_cpus):
            cpus.append(Cpu(self.__scheduler, i, clock_rate))
        return cpus


    def __set_clock_rate(self, clock_rate: float):
        if clock_rate <= 0:
            raise ValueError("clock_rate must be greater than 0")
        
        self.__clock_rate = clock_rate


    def add_process(self, process: Process):
        self.__scheduler.add_process(process)
        
    def get_context(self) -> str:
        return self.__scheduler_context.get()

    def is_over(self) -> bool:
        return self.__are_all_cpus_idle() and not self.__scheduler.has_alive_processes()
    
    
    def __are_all_cpus_idle(self) -> bool:
        for cpu in self.__cpus:
            if not cpu.is_idle():
                return False
            
        return True


    def start(self):
        if self.__running:
            raise RuntimeError("scheduler already started")
        self.__running = True

        self.__start_wait_process_check()
        self.__start_cpus()


    def stop(self):
        if not self.__running:
            raise RuntimeError("scheduler is not running")
        
        self.__running = False
        self.__stop_cpus()


    def __start_wait_process_check(self):
        thread = threading.Thread(target=self.__wait_process_check, args=())
        thread.start()


    def __start_cpus(self):
        for cpu in self.__cpus:
            cpu.start()


    def __stop_cpus(self):
        for cpu in self.__cpus:
            cpu.stop()


    def __wait_process_check(self):
        while self.__running:
            self.__scheduler.wait_process_check()
            time.sleep(self.__clock_rate)


    def get_clock_rate(self) -> int:
        return self.__clock_rate
    
    def is_running(self) -> bool:
        return self.__running
