from queue import Queue
import process

#essa classe define como  processo é visto pelo escalonador
#o escalonador não deve acessar o atributo de comportamento do processo
#o escalonador deve ser capaz de identificar o comportamento do processo baseado em sua execução
#o processo é tratado como CPU bound no início
class process_info:
    def __init__(self, process: process):
        self.process = process
        self.behaviour = process.__CPU_BOUND
        self.ready = True
        self.ellapsed_cpu_time = 0
        self.ellapsed_wait_time = 0


class scheduler:

    def __init__(self):
        self.__system_processes = Queue.queue()
        self.__interactive_processes = Queue.queue()
        self.__batch_processes = Queue.queue()
        self.__wait_processes = Queue.queue()
        self.__executing = None

    def new_process(self, process: process):
        pass

    def execute(self):
        if self.__executing is None:
            return
        if not self.__system_processes.empty():
            pass
        elif not self.__interactive_processes.empty():
            pass
        elif not self.__batch_processes.empty():
            pass
        

    def context_switch(self):
        pass
