import random
class process:

    SYSTEM_PROCESS = 0
    INTERACTIVE_PROCESS = 1
    BATCH_PROCESS = 2

    CPU_BOUND = 0
    IO_BOUND = 1

    #se o processo é do sistema ou batch, ele será CPU bound e nunca fará I/O
    #se o processo é interativo, pode ser CPU bound ou I/O bound
    def __init__(self, type, num_instructions = 10, wait_time_range = (5, 20)):
        self.__type = type
        if type == self.SYSTEM_PROCESS or type == self.BATCH_PROCESS:
            self.__behaviour = self.CPU_BOUND
        elif type == self.INTERACTIVE_PROCESS:
            random_number = random.randint(1,3)
            if random_number >= 2:
                self.__behaviour = self.IO_BOUND
            else:
                self.__behaviour = self.CPU_BOUND
        else:
            raise ValueError("invalid process type")
        self.__num_instructions = num_instructions
        self.__wait_time = 0
        self.__wait_time_range = wait_time_range

    def get_type(self):
        return self.__type

    #retorna True se quer executar CPU
    #retora False se quer fazer I/O
    #se for um processo CPU bound tem 1 chance em 20 de fazer I/O
    #se for um processo I/O bound tem 5 chances em 20 de fazer I/O 
    def execute(self) -> bool:
        if self.__wait_time > 0:
            return
        
        self.__num_instructions -= 1
        if self.__type == self.INTERACTIVE_PROCESS:
            random_number = random.randint(1,20)
            if self.__behaviour == self.CPU_BOUND:
                if random_number < 20:
                    self.__wait_time = random.randint(self.__wait_time_range[0], self.__wait_time_range[1])
                    return True
                return False
            else:
                if random_number <= 15:
                    self.__wait_time = random.randint(self.__wait_time_range[0], self.__wait_time_range[1])
                    return True
                return False
        
        return True
    
    def wait(self) -> bool:
        self.__wait_time -= 1
        if self.__wait_time == 0:
            return True
        return False
    
    def is_over(self):
        return self.__num_instructions == 0