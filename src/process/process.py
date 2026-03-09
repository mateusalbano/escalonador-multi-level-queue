from abc import ABC, abstractmethod
from enum import Enum

class ProcessBehaviour(Enum):
    CPU_BOUND = 0
    IO_BOUND = 1

class ProcessType(Enum):
    SYSTEM_PROCESS = 0
    INTERACTIVE_PROCESS = 1
    BATCH_PROCESS = 2

class Process(ABC):

    INFINITE_INSTRUCTIONS = -1

    def __init__(self, num_instructions = 10):
        self._elapsed_execution_time = 0
        self.__set_num_instructions(num_instructions)


    def __str__(self) -> str:
        return f"p{self._pid}"
    

    def __set_num_instructions(self, num_instructions: int):
        if num_instructions <= 0 and num_instructions != self.INFINITE_INSTRUCTIONS:
            raise ValueError("num_instructions must be greater than 0 or equal to INFINITE_INSTRUCTIONS")
        
        self._num_instructions = num_instructions


    def get_num_instructions(self) -> int:
        return self._num_instructions
    

    def set_pid(self, pid):
        if pid < 0:
            raise ValueError("pid must be greater than or equal to 0")
        
        self._pid = pid


    def get_pid(self) -> int:
        return self._pid


    def _update_counters(self):
        if self.is_over():
            raise RuntimeError("process is over and can't update counters")

        if not self.is_permanent():
            self._num_instructions -= 1
        
        self._elapsed_execution_time += 1


    def is_permanent(self) -> bool:
        return self._num_instructions == -1
    
    def is_over(self) -> bool:
        return self._num_instructions == 0
    
    @abstractmethod
    def can_execute(self) -> bool:
        ...

    @abstractmethod
    def execute(self):
        ...

    @abstractmethod
    def get_behaviour(self) -> ProcessBehaviour:
        ...

    @abstractmethod
    def get_type(self) -> ProcessType:
        ...
