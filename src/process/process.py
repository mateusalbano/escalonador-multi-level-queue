from abc import ABC, abstractmethod
class Process(ABC):

    SYSTEM_PROCESS = 0
    INTERACTIVE_PROCESS = 1
    BATCH_PROCESS = 2

    CPU_BOUND = 0
    IO_BOUND = 1

    def __init__(self, num_instructions = 10, ends = True):
        self._elapsed_execution_time = 0
        self._set_num_instructions(num_instructions, ends)

    def __str__(self) -> str:
        return f"p{self._pid}"

    def set_pid(self, pid):
        self._pid = pid

    def get_pid(self) -> int:
        return self._pid

    def _set_num_instructions(self, num_instructions, ends):
        if ends:
            self._num_instructions = num_instructions
        else:
            self._num_instructions = -1

    def _decrement_num_instructions(self):
        if self.ends() and not self.is_over():
            self._num_instructions -= 1

    def _increment_execution_time(self):
        if not self.is_over():
            self._elapsed_execution_time += 1

    def ends(self) -> bool:
        return self._num_instructions != -1
    
    def is_over(self) -> bool:
        return self._num_instructions == 0
    
    @staticmethod
    def type_to_str(type: int):
        type_names = {
            Process.SYSTEM_PROCESS: "system",
            Process.INTERACTIVE_PROCESS: "interactive",
            Process.BATCH_PROCESS: "batch",
        }
        return type_names[type]
    
    @abstractmethod
    def can_execute(self) -> bool:
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_type(self) -> int:
        pass

    @abstractmethod
    def get_behaviour(self) -> int:
        pass
