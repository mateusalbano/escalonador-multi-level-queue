import process

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
        self.ellapsed_cpu_time = 0
        self.ellapsed_wait_time = 0

    """
    quanto menor o valor da prioridade, maior ela é, é assim que funciona a fila de prioridades do Python, não me culpe
    nesse caso quanto mais tempo o processo ficar esperando, menor vai ser o valor da prioridade e portanto ela se torna maior
    quanto maior o tempo de processamento maior o valor da prioridade e menor ela é.
    """
    def get_priority(self) -> int:
        return self.ellapsed_cpu_time - self.ellapsed_wait_time