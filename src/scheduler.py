import queue

import threading
import time

from core import core
from prioritized_item import PrioritizedItem
from process import process
from process_info import process_info

class scheduler:
    
    """
    construtor da classe scheduler
    parâmetro quantum representa o quantum que cada processo recebe no momento que ele é escalonado
    parâmetro n_cores define o número de cores (núcleos) que serão executados
    parâmtro clock define o tempo em segundos do intervalo de uma execução e outra (time.sleep(self.__clock))
    """
    def __init__(self, quantum = 5, n_cores = 4, clock = 1):
        self.__next_id = 0
        self.__system_processes = queue.Queue()
        self.__interactive_processes = queue.PriorityQueue()
        self.__batch_processes = queue.Queue()
        self.__wait_processes = []
        self.__cores = []
        self.__dead_processes = []
        self.__clock = clock
        for i in range (n_cores):
            self.__cores.append(core(self, i, quantum, clock))
        self.__quantum = quantum
        self.__started = False

    """
    inicia todas as threads que simulam os cores (núcleos) da CPU
    inicia a thread responsável pela contagem de espera e wake up dos processos
    para que o programa pare é necessário utilizar a função end()
    tentar iniciar um scheduler que já iniciou gera um erro
    """
    def start(self):
        if self.__started:
            raise RuntimeError("scheduler already started")
        self.__started = True
        thread = threading.Thread(target=self.__wake_up, args=())
        thread.start()
        for core in self.__cores:
            core.start()

    """
    termina todas as threads inicializadas pelo método start
    tentar terminar um scheduler não iniciou gera um erro
    """
    def end(self):
        if not self.__started:
            raise RuntimeError("scheduler is not running")
        self.__started = False
        for core in self.__cores:
            core.end()
        

    # cria um novo processo e o associa com a fila correspondente
    def add_process(self, process: process):
        new_process_info = process_info(process, self.__next_id)
        self.__next_id += 1
        self.new_ready(new_process_info)

    """
    coloca um novo processo na fila de pronto
    os processos interativos são encapsulados em uma classe para funcionar com a fila de prioridades.
    """
    def new_ready(self, process_info):
        type = process_info.process.get_type()
        if type == process.SYSTEM_PROCESS:
            self.__system_processes.put(process_info)
        elif type == process.INTERACTIVE_PROCESS:
            wrapper = PrioritizedItem(process_info.get_priority(), process_info)
            self.__interactive_processes.put(wrapper)
        else:
            self.__batch_processes.put(process_info)

    # método que executa em paralelo para fazer contagem de espera e acordar processos que terminaram a espera.
    def __wake_up(self):
        while self.__started:
            time.sleep(self.__clock)
            new_ready = []
            for process_info in self.__wait_processes:
                is_ready = process_info.process.wait()
                if is_ready:
                    new_ready.append(process_info)
                else:
                    process_info.ellapsed_wait_time += 1

            for process_info in new_ready:
                self.__wait_processes.remove(process_info)
                self.new_ready(process_info) 
    
    # retorna verdadeiro ou falso para caso a CPU terminou (não há processos prontos e nem em espera)
    def is_over(self) -> bool:
        for core in self.__cores:
            if not core.get_running() is None:
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
        output = []
        for core in self.__cores:
            output.extend(["Core ", str(core.get_core_id()), ":"])
            if not core.get_running() is None:
                output.extend([" p", str(core.get_running().pid), " (", core.get_running().process.get_type_str(), ") ", "quantum: ", str(core.get_current_quantum())])
            output.append("\n")

        output.extend(["\n\nSystem processes: [ "])

        for process_info in system_list:
            output.extend(["p", str(process_info.pid), " "])
            
        output.extend(["]\nInteractive processes: [ "])

        for wrapper in interactive_list:
            output.extend(["p", str(wrapper.item.pid), " "])

        output.extend(["]\nBatch processes: [ "])

        for process_info in batch_list:
            output.extend(["p", str(process_info.pid), " "])

        output.extend(["]\n\nWait processes: [ "])

        for process_info in self.__wait_processes:
            output.extend(["p", str(process_info.pid), " "])

        output.append("]\nDead processes: [ ")

        for process_info in self.__dead_processes:
            output.extend(["p", str(process_info.pid), " "])

        output.append("]\n")

        return "".join(output)
    
    def started(self) -> bool:
        return self.__started
    
    # getters para que a classe core acesse os atributos necessários
    def get_quantum(self) -> int:
        return self.__quantum
    
    def get_clock(self) -> int:
        return self.__clock
    
    def get_system_processes(self) -> queue.Queue:
        return self.__system_processes
    
    def get_interactive_processes(self) -> queue.Queue:
        return self.__interactive_processes
    
    def get_batch_processes(self) -> queue.Queue:
        return self.__batch_processes
    
    def get_wait_processes(self) -> list:
        return self.__wait_processes  
    
    def get_dead_processes(self) -> list:
        return self.__dead_processes