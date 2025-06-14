from dataclasses import dataclass, field
from typing import Any

"""
classe utilizada pela fila de prioridades dos processos interativos do scheduler (escalonador)
o atributo priority guarda o valor da prioridade do atributo item
quanto menor o valor da prioridade, maior ela é, isso se deve ao comportamento da fila de prioridades do Python
"""

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)