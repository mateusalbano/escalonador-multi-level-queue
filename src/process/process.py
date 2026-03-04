from abc import ABC, abstractmethod
from enum import Enum

class ProcessType(Enum):
    SYSTEM_PROCESS = 0
    INTERACTIVE_PROCESS = 1
    BATCH_PROCESS = 2

class ProcessBehaviour(Enum):
    CPU_BOUND = 0
    IO_BOUND = 1

class Process(ABC):

    def __init__(self, num_instructions = 10, permanent = False):
        self._elapsed_execution_time = 0
        self._set_num_instructions(num_instructions, permanent)

    def __str__(self) -> str:
        return f"p{self._pid}"

    def set_pid(self, pid):
        self._pid = pid

    def get_pid(self) -> int:
        return self._pid

    def _set_num_instructions(self, num_instructions, permanent):
        if permanent:
            self._num_instructions = -1
        else:
            self._num_instructions = num_instructions

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
    def get_type(self) -> ProcessType:
        ...

    @abstractmethod
    def get_behaviour(self) -> ProcessBehaviour:
        ...