import random
class process:

    SYSTEM_PROCESS = 0
    INTERACTIVE_PROCESS = 1
    BATCH_PROCESS = 2

    CPU_BOUND = 0
    IO_BOUND = 1

    """
    se o processo é do sistema ou batch, ele será CPU bound e nunca fará I/O
    se o processo é interativo, pode ser CPU bound ou I/O bound
    """
    def __init__(self, type, num_instructions = 10, wait_time_range = (2, 10), ends = True):
        self.__type = type
        if type == self.SYSTEM_PROCESS or type == self.BATCH_PROCESS:
            self.__behaviour = self.CPU_BOUND
        elif type == self.INTERACTIVE_PROCESS:
            random_number = random.randint(1,4)
            if random_number >= 2:
                self.__behaviour = self.IO_BOUND
            else:
                self.__behaviour = self.CPU_BOUND
        else:
            raise ValueError("invalid process type")
        
        self.__last_exec_io = False
        self.__num_instructions = num_instructions
        if not ends:
            self.__num_instructions = -1
        self.__wait_time = 0
        self.__wait_time_range = wait_time_range

    def get_type(self) -> int:
        return self.__type
    
    #retorna uma string do tipo de processo
    def get_type_str(self) -> str:
        if self.__type == self.SYSTEM_PROCESS:
            return "SYSTEM"
        if self.__type == self.INTERACTIVE_PROCESS:
            return "INTERACTIVE"
        else:
            return "BATCH"
    
    """
    retorna True se quer executar CPU
    retora False se quer fazer I/O
    se for um processo CPU bound tem 1 chance em 20 de fazer I/O
    se for um processo I/O bound tem 5 chances em 20 de fazer I/O 
    """
    def execute(self) -> bool:
        if self.__wait_time > 0:
            raise RuntimeError("process is waiting")
        
        if self.__num_instructions == 1:
            self.__num_instructions = 0
            return True

        if self.__type == self.INTERACTIVE_PROCESS:
            random_number = random.randint(1,20)
            if self.__behaviour == self.CPU_BOUND and not self.__last_exec_io and random_number >= 20:
                self.__last_exec_io = True
                self.__wait_time = random.randint(self.__wait_time_range[0], self.__wait_time_range[1])
                return False
            
            elif self.__behaviour == self.IO_BOUND and not self.__last_exec_io and random_number >= 15:
                self.__last_exec_io = True
                self.__wait_time = random.randint(self.__wait_time_range[0], self.__wait_time_range[1])
                return False
            
            self.__last_exec_io = False
        if self.__num_instructions > 0:
            self.__num_instructions -= 1

        return True
    
    """
    função para contabilizar a espera do processo
    se a espera acabou, retorna True, do contrário, retorna False
    """
    def wait(self) -> bool:
        self.__wait_time -= 1
        if self.__wait_time == 0:
            return True
        return False
    
    # retorna True ou False para caso o programa terminou de executar
    def is_over(self):
        return self.__num_instructions == 0