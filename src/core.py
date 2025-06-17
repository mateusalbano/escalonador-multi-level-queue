import random
import threading
import time
from process import process
from process_info import process_info
import scheduler

class core:

    DISPATCH = 0
    WAIT = 1
    TIME_RUN_OUT = 2
    IDLE = 3

    def __init__(self, scheduler: scheduler, core_id, quantum = 5, clock = 1):
        self.__core_id = core_id
        self.__scheduler = scheduler
        self.__quantum = quantum
        self.__current_quantum = 0
        self.__running = None
        self.__clock = clock
        self.__started = False
        
    """
    inicia a thread que executa o método execute
    este método é chamado pelo start() do scheduler (escalonador)
    tentar iniciar um core (núcleo) que já iniciou gera um erro
    """
    def start(self):
        if self.__started:
            raise RuntimeError("core scheduling already started")
        self.__started = True
        thread = threading.Thread(target=self.__execute, args=())
        thread.start()

    """
    interrompe a thread que executa o método execute
    este método é chamado pelo end() do scheduler (escalonador)
    tentar interromper um core (núcleo) que já iniciou gera um erro
    """
    def end(self):
        if not self.__started:
            raise RuntimeError("core is not running")
        self.__started = False

    """
    realiza a execução do processo ocupando a CPU e faz as validações necessárias
    se o processo fizer I/O, vai para a fila de espera
    se o quantum acabar, vai para a fila de pronto correspondente
    se o processo executar todas suas instruções, é finalizado
    este método é executado em paralelo
    """
    def __execute(self):
        while self.__started:
            time.sleep(self.__clock)
            if self.__running is None:
                self.__context_switch(self.IDLE)
                continue

            cpu_execution = self.__running.process.execute()
            if not cpu_execution:
                self.__context_switch(self.WAIT)
            elif self.__running.process.is_over():
                self.__running.ellapsed_cpu_time += 1
                self.__context_switch(self.DISPATCH)
            else:
                self.__running.ellapsed_cpu_time += 1
                self.__current_quantum -= 1
                if self.__current_quantum <= 0:
                    self.__context_switch(self.TIME_RUN_OUT)

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
        if not self.__scheduler.get_system_processes().empty():
            wheel.extend([process.SYSTEM_PROCESS, process.SYSTEM_PROCESS, process.SYSTEM_PROCESS])
        if not self.__scheduler.get_interactive_processes().empty():
            wheel.extend([process.INTERACTIVE_PROCESS, process.INTERACTIVE_PROCESS])
        if not self.__scheduler.get_batch_processes().empty():
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
            self.__scheduler.get_wait_processes().append(self.__running)
            self.__running = None
        elif action == self.TIME_RUN_OUT:
            self.__scheduler.new_ready(self.__running)

        next = self.__next_executing()

        if next == process.SYSTEM_PROCESS:
            self.__running = self.__scheduler.get_system_processes().get()
        elif next == process.INTERACTIVE_PROCESS:
            self.__running = self.__scheduler.get_interactive_processes().get().item
        elif next == process.BATCH_PROCESS:
            self.__running = self.__scheduler.get_batch_processes().get()
        else:
            if action == self.DISPATCH:
                self.__running = None
            return
        
        self.__current_quantum = self.__quantum


    def get_running(self) -> process_info:
        return self.__running
    
    def get_core_id(self) -> int:
        return self.__core_id
    
    def get_quantum(self) -> int:
        return self.__quantum
    
    def get_current_quantum(self) -> int:
        return self.__current_quantum