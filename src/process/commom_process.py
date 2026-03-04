from process.process import Process, ProcessType, ProcessBehaviour


class CommomProcess(Process):

    def __init__(self, type: ProcessType, num_instructions=10, permanent=False):
        super().__init__(num_instructions, permanent)
        self.__type = type


    def get_behaviour(self) -> ProcessBehaviour:
        return ProcessBehaviour.CPU_BOUND

    def get_type(self) -> ProcessType:
        return self.__type

    def execute(self):
        if not self.can_execute():
            raise RuntimeError("process cannot execute")
        
        self._update_counters()

    def can_execute(self) -> bool:
        return not self.is_over()