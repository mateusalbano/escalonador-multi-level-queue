import random
from process.process import Process, ProcessType, ProcessBehaviour


class InteractiveProcess(Process):

    def __init__(self, behaviour: ProcessBehaviour, num_instructions=10, permanent=False):
        super().__init__(num_instructions, permanent)
        self.__behaviour = behaviour
        self.__current_wait_time = 0
        self.__elapsed_wait_time = 0


    def get_behaviour(self) -> ProcessBehaviour:
        return self.__behaviour
    
    def get_type(self) -> ProcessType:
        return ProcessType.INTERACTIVE_PROCESS
    
    """
    The lower this value gets higher the priority is.
    higher execution time -> smaller priority
    higher wait time -> higher priority
    """
    def get_priority(self) -> int:
        return self._elapsed_execution_time - self.__elapsed_wait_time

    def execute(self):
        if not self.can_execute():
            raise RuntimeError("process cannot execute")
        
        self._update_counters()
        
        if self.__behaviour == ProcessBehaviour.CPU_BOUND:
            self.__try_io_operation(10)
        elif self.__behaviour == ProcessBehaviour.IO_BOUND:
            self.__try_io_operation(20)


    def __try_io_operation(self, probability: float):
        if self._num_instructions == 1:
            return
        
        choice = random.randrange(1,100)
        if probability >= choice:
            self.__make_io_operation()
    
    def __make_io_operation(self):
        self.__current_wait_time = random.randint(1, 4)

    def is_idle(self) -> bool:
        return self.__current_wait_time > 0
    
    def can_execute(self) -> bool:
        return not self.is_over() and not self.is_idle()

    def wait(self):
        if not self.is_idle():
            raise RuntimeError("process is not idle to wait")
        
        self.__current_wait_time -= 1
        self.__elapsed_wait_time += 1