import random
from process.process import Process, ProcessType, ProcessBehaviour


class InteractiveProcess(Process):

    def __init__(self, behaviour: int, num_instructions=10, is_permanent=True):
        super().__init__(num_instructions, is_permanent)
        self.__set_behaviour(behaviour)
        self.__current_wait_time = 0
        self.__elapsed_wait_time = 0

    def __set_behaviour(self, behaviour: ProcessBehaviour):
        if behaviour != ProcessBehaviour.CPU_BOUND and behaviour != ProcessBehaviour.IO_BOUND:
            raise RuntimeError("interactive process behaviour must be either CPU bound or I/O bound")
        
        self.__behaviour = behaviour

    def get_behaviour(self) -> ProcessBehaviour:
        return self.__behaviour
    
    def get_type(self) -> ProcessType:
        return ProcessType.INTERACTIVE_PROCESS
    
    """
    The lower this values gets higher the priority is, that implies:
    higher execution time -> smaller priority
    higher wait time -> higher priority
    """
    def get_priority(self) -> int:
        return self._elapsed_execution_time - self.__elapsed_wait_time

    def execute(self):
        if self.can_execute():
            if self.__behaviour == ProcessBehaviour.CPU_BOUND:
                self.__try_io_operation(10)
            elif self.__behaviour == ProcessBehaviour.IO_BOUND:
                self.__try_io_operation(20)

            self._decrement_num_instructions()
            self._increment_execution_time()
        else:
            raise RuntimeError("process is over and can't execute")

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