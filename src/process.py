import random

class process:

    __SYSTEM_PROCESS = 0
    __INTERACTIVE_PROCESS = 1
    __BATCH_PROCESS = 2
    __CPU_BOUND = 0
    __IO_BOUND = 1


    #se o processo é do sistema ou batch, ele será CPU bound e nunca fará I/O
    #se o processo é interativo, pode ser CPU bound ou I/O bound
    def __init__(self, type, num_instructions):
        self.__type = type
        if type == self.__SYSTEM_PROCESS or type == self.__BATCH_PROCESS:
            self.__behaviour = self.__CPU_BOUND
        elif type == self.__INTERACTIVE_PROCESS:
            random_number = random.randint(1,3)
            if random_number >= 2:
                self.__behaviour = self.__IO_BOUND
            else:
                self.__behaviour = self.__CPU_BOUND
        else:
            raise ValueError("invalid process type")
        self.__num_instructions = num_instructions


    #retorna True se quer executar CPU
    #retora False se quer fazer I/O
    #se for um processo CPU bound tem 1 chance em 20 de fazer I/O 
    #se for um processo I/O bound tem 5 chances em 20 de fazer I/O 
    def execute(self) -> bool:
        self.__num_instructions -= 1
        if self.__type == self.__INTERACTIVE_PROCESS:
            random_number = random.randint(1,20)
            if self.__behaviour == self.__CPU_BOUND:
                if random_number < 20:
                    return True
                return False
            else:
                if random_number <= 15:
                    return True
                return False
        
        return True

