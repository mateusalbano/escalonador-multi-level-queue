import queue
import random

from dataclasses import dataclass, field
from typing import Any

from process import process
from process_info import process_info

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

class scheduler:

    DISPATCH = 0
    WAIT = 1
    TIME_RUN_OUT = 2
    IDLE_CPU = 3
    
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

    """
    realiza a execução do processo ocupando a CPU e faz as validações necessárias
    se o processo fizer I/O, vai para a fila de espera
    se o quantum acabar, vai para a fila de pronto correspondente
    se o processo executar todas suas instruções, é finalizado
    """
    def execute(self):
        if self.is_over():
            raise RuntimeError("can't execute terminated cpu")

        self.__wake_up()

        if self.__executing is None:
            self.__context_switch(self.IDLE_CPU)

        if not self.__executing is None:
            cpu_execution = self.__executing.process.execute()
            if not cpu_execution:
                self.__context_switch(self.WAIT)
            elif self.__executing.process.is_over():
                self.__executing.ellapsed_cpu_time += 1
                self.__context_switch(self.DISPATCH)
            else:
                self.__executing.ellapsed_cpu_time += 1
                self.__executing.quantum -= 1
                if self.__executing.quantum <= 0:
                    self.__context_switch(self.TIME_RUN_OUT)
        

    """
    coloca um novo processo na fila de pronto
    os processos interativos são encapsulados em uma classe para funcionar com a fila de prioridades.
    """
    def __new_ready(self, process_info):
        type = process_info.process.get_type()
        if type == process.SYSTEM_PROCESS:
            self.__system_processes.put(process_info)
        elif type == process.INTERACTIVE_PROCESS:
            wrapper = PrioritizedItem(process_info.get_priority(), process_info)
            self.__interactive_processes.put(wrapper)
        else:
            self.__batch_processes.put(process_info)

    # método utilizado pelo execute para fazer contagem de espera e acordar processos que terminaram a espera.
    def __wake_up(self):
        new_ready = []
        for process_info in self.__wait_processes:
            is_ready = process_info.process.wait()
            if is_ready:
                new_ready.append(process_info)
            else:
                process_info.ellapsed_wait_time += 1

        for process_info in new_ready:
            self.__wait_processes.remove(process_info)
            self.__new_ready(process_info)

    """
    roleta para escolher qual fila será executada
    considerando que nenhuma das filas estejam vazias, as chances de uma fila ser escolhida:
    fila de processos de sistema: 50%
    fila de processos interativos: 33.3%
    fila de processos batch: 16.6%
    se uma fila estiver vazia as chances são distribuídas para as demais filas
    se todas as filas estiverem vazias, significa que não há processos prontos para serem escalonados
    """
    def __next_executing(self) -> int:
        wheel = []
        if not self.__system_processes.empty():
            wheel.extend([process.SYSTEM_PROCESS, process.SYSTEM_PROCESS, process.SYSTEM_PROCESS])
        if not self.__interactive_processes.empty():
            wheel.extend([process.INTERACTIVE_PROCESS, process.INTERACTIVE_PROCESS])
        if not self.__batch_processes.empty():
            wheel.append(process.BATCH_PROCESS)

        if len(wheel) == 0:
            return -1
        
        return wheel[random.randint(0, len(wheel) - 1)] 

    """
    troca o contexto da cpu
    end_process define se o processo deve ser finalizado ou não
    processo finalizado é retirado de execução e perde sua referência
    processo não finalizado é retirado da execução e colocado em sua fila correspondente
    a fila escolhida depende da execução da roleta (__next_executing())
    """
    def __context_switch(self, action: int):

        if action == self.WAIT:
            self.__wait_processes.append(self.__executing)
            self.__executing = None
        elif action == self.TIME_RUN_OUT:
            self.__new_ready(self.__executing)

        next = self.__next_executing()

        if next == process.SYSTEM_PROCESS:
            self.__executing = self.__system_processes.get()
        elif next == process.INTERACTIVE_PROCESS:
            self.__executing = self.__interactive_processes.get().item
        elif next == process.BATCH_PROCESS:
            self.__executing = self.__batch_processes.get()
        else:
            if action == self.DISPATCH:
                self.__executing = None
            return
        
        self.__executing.quantum = self.__quantum


    # retorna verdadeiro ou falso para caso a CPU terminou (não há processos prontos e nem em espera)
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
    
    """
    retorna uma string mostrando o contexto da última execução
    o uso de listas se deve ao fato de que as strings em Python são imutáveis, listas não, o que otimiza o programa.
    """
    def get_context(self) -> str:
        system_list = list(self.__system_processes.queue)
        interactive_list = list(self.__interactive_processes.queue)
        batch_list = list(self.__batch_processes.queue)
        output = list("Executing: ")
        if not self.__executing is None:
            output.extend(["p", str(self.__executing.pid), " (", self.__executing.process.get_type_str(), ") ", "quantum: ", str(self.__executing.quantum)])

        output.extend(list("\n\nSystem processes: [ "))

        for process_info in system_list:
            output.extend(["p", str(process_info.pid), " "])
            
        output.extend(list("]\nInteractive processes: [ "))

        for wrapper in interactive_list:
            output.extend(["p", str(wrapper.item.pid), " "])

        output.extend(list("]\nBatch processes: [ "))

        for process_info in batch_list:
            output.extend(["p", str(process_info.pid), " "])

        output.extend(list("]\n\nWait processes: [ "))

        for process_info in self.__wait_processes:
            output.extend(["p", str(process_info.pid), " "])

        output.append("]\n")

        return "".join(output)