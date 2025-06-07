import queue
import process

#essa classe define como o processo é visto pelo escalonador
#o escalonador não deve acessar o atributo de comportamento do processo
#o escalonador deve ser capaz de identificar o comportamento do processo baseado em sua execução
#o processo é tratado como CPU bound no início
class process_info:

    def __init__(self, process: process, pid: int):
        self.pid = pid
        self.process = process
        self.quantum = 0
        self.ellapsed_cpu_time = 0
        self.ellapsed_wait_time = 0

    #quanto menor o valor da prioridade, maior ela é, é assim que funciona a fila de prioridades do Python, não me culpe
    #nesse caso quanto mais tempo o processo ficar esperando, menor vai ser o valor da prioridade e portanto ela se torna maior
    #quanto maior o tempo de processamento maior o valor da prioridade e menor ela é.
    def get_priority(self) -> int:
        self.ellapsed_cpu_time - self.ellapsed_wait_time

class scheduler:
    
    def __init__(self, quantum = 5):
        self.__last_id = 0
        self.__system_processes = queue.Queue()
        self.__interactive_processes = queue.PriorityQueue()
        self.__batch_processes = queue.Queue()
        self.__wait_processes = []
        self.__executing = None
        self.__quantum = quantum
        

    #cria um novo processo e o associa com a fila correspondente
    def add_process(self, process: process):
        new_process_info = process_info(process, self.__last_id)
        self.__last_id += 1
        self.__new_ready(new_process_info)

    #realiza a execução do processo ocupando a CPU e faz as validações necessárias
    #se o processo fizer I/O, vai para a fila de espera
    #se o quantum acabar, vai para a fila de pronto correspondente
    #se o processo executar todas suas instruções, é finalizado
    def execute(self):
        if self.__executing is None:
            self.__context_switch(False)
        
        cpu_execution = self.__executing.process.execute()
        self.__executing.ellapsed_cpu_time += 1
        if not cpu_execution:
            self.__context_switch(False)
        elif self.__executing.process.is_over():
            self.__context_switch(True)
        else:
            self.__executing.quantum -= 1
            if self.__executing.quantum == 0:
                self.__new_ready(self.__executing)
                self.__context_switch(False)
        
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

        
    def __new_ready(self, process_info):
        type = process_info.process.get_type()
        if type == process.SYSTEM_PROCESS:
            self.__system_processes.put(process_info)
        elif type == process.INTERACTIVE_PROCESS:
            self.__interactive_processes.put((process_info.get_priority(), process_info))
        else:
            self.__batch_processes.put(process_info)

    def __context_switch(self, end_process: bool):
        next_exe = None
        if not end_process:
            self.__new_ready(self.__executing)

        if not self.__system_processes.empty():
            next_exe = self.__system_processes.get()
            self.__executing = next_exe
        elif not self.__interactive_processes.empty():
            next_exe = self.__interactive_processes.get()
            self.__executing = next_exe
        elif not self.__batch_processes.empty():
            next_exe = self.__batch_processes.get()
            self.__executing = next_exe
        