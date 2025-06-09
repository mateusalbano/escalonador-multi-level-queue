import queue
from process import process
from dataclasses import dataclass, field
from typing import Any


class process_info:
    """
    essa classe define como o processo é visto pelo escalonador
    o escalonador não deve acessar o atributo de comportamento do processo
    o escalonador deve ser capaz de identificar o comportamento do processo baseado em sua execução
    o processo é tratado como CPU bound no início
    """
    def __init__(self, process: process, pid: int):
        self.pid = pid
        self.process = process
        self.quantum = 0
        self.ellapsed_cpu_time = 0
        self.ellapsed_wait_time = 0

    # quanto menor o valor da prioridade, maior ela é, é assim que funciona a fila de prioridades do Python, não me culpe
    # nesse caso quanto mais tempo o processo ficar esperando, menor vai ser o valor da prioridade e portanto ela se torna maior
    # quanto maior o tempo de processamento maior o valor da prioridade e menor ela é.
    def get_priority(self) -> int:
        self.ellapsed_cpu_time - self.ellapsed_wait_time

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

class scheduler:

    DISPATCH = 0
    WAIT = 1
    TIME_RUN_OUT = 2
    # WAKE_UP = 3
    
    def __init__(self, quantum = 5):
        self.__last_id = 0
        self.__system_processes = queue.Queue()
        self.__interactive_processes = queue.PriorityQueue()
        self.__batch_processes = queue.Queue()
        self.__wait_processes = []
        self.__executing = None
        self.__quantum = quantum
        

    # cria um novo processo e o associa com a fila correspondente
    def add_process(self, process: process):
        new_process_info = process_info(process, self.__last_id)
        self.__last_id += 1
        self.__new_ready(new_process_info)

    # realiza a execução do processo ocupando a CPU e faz as validações necessárias
    # se o processo fizer I/O, vai para a fila de espera
    # se o quantum acabar, vai para a fila de pronto correspondente
    # se o processo executar todas suas instruções, é finalizado
    def execute(self):
        if self.is_over():
            raise RuntimeError("can't execute idle cpu")

        if self.__executing is None:
            self.__context_switch(self.DISPATCH)
        
        if not self.__executing is None:
            cpu_execution = self.__executing.process.execute()
            self.__executing.ellapsed_cpu_time += 1
            if not cpu_execution:
                self.__context_switch(self.WAIT)
            elif self.__executing.process.is_over():
                self.__context_switch(self.DISPATCH)
            else:
                self.__executing.quantum -= 1
                if self.__executing.quantum <= 0:
                    self.__context_switch(self.TIME_RUN_OUT)
        
        new_ready = []
        i = 0
        for process_info in self.__wait_processes:
            is_ready = process_info.process.wait()
            if is_ready:
                new_ready.append(i)
            else:
                process_info.ellapsed_wait_time += 1
            i += 1

        for i in new_ready:
            self.__new_ready(self.__wait_processes.pop(i))

    # coloca um novo processo na fila de pronto
    # os processos interativos são encapsulados em uma classe para funcionar com a fila de prioridades.
    def __new_ready(self, process_info):
        type = process_info.process.get_type()
        if type == process.SYSTEM_PROCESS:
            self.__system_processes.put(process_info)
        elif type == process.INTERACTIVE_PROCESS:
            wrapper = PrioritizedItem(process_info.get_priority(), process_info)
            self.__interactive_processes.put(wrapper)
        else:
            self.__batch_processes.put(process_info)

    # troca o contexto da cpu
    # end_process define se o processo deve ser finalizado ou não
    # processo finalizado é retirado de execução e perde sua referência
    # processo não finalizado é retirado da execução e colocado em sua fila correspondente
    def __context_switch(self, action: int):
        if action == self.WAIT:
            self.__wait_processes.append(self.__executing)
            self.__executing = None
        elif action == self.TIME_RUN_OUT:
            self.__new_ready(self.__executing)
            
        if not self.__system_processes.empty():
            self.__executing = self.__system_processes.get()
        elif not self.__interactive_processes.empty():
            self.__executing = self.__interactive_processes.get().item
        elif not self.__batch_processes.empty():
            self.__executing = self.__batch_processes.get()
        elif action != self.DISPATCH:
            return
        else:
            self.__executing = None
            return 
           
        
        self.__executing.quantum = self.__quantum


    # retorna verdadeiro ou falso para caso a CPU terminou
    def is_over(self) -> bool:
        if self.__executing != None:
            return False
        
        if not self.__system_processes.empty():
            return False
        
        if not self.__interactive_processes.empty():
            return False
        
        if not self.__batch_processes.empty():
            return False
        
        if len(self.__wait_processes) != 0:
            return False
        
        return True