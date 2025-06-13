from scheduler import scheduler
class core:

    def __init__(self, scheduler: scheduler, quantum = 5):
        self.__process_info = None
        self.__scheduler = scheduler
        self.__quantum = quantum
        self.__current_quantum = 0


    