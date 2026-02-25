from process.process import Process


class CommomProcess(Process):

    def __init__(self, type, num_instructions=10, ends=True):
        super().__init__(num_instructions, ends)
        self.__set_type(type)

    def __set_type(self, type: int):

        if type != Process.SYSTEM_PROCESS and type != Process.BATCH_PROCESS:
            raise RuntimeError("commom process type must be either system or batch")
        
        self.__type = type

    def get_behaviour(self) -> int:
        return Process.CPU_BOUND

    def get_type(self) -> int:
        return self.__type

    def execute(self):
        if self.can_execute():
            self._decrement_num_instructions()
            self._increment_execution_time()
        else:
            raise RuntimeError("process is over and can't execute")

    def can_execute(self) -> bool:
        return not self.is_over()