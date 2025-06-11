import random
import time
from scheduler import scheduler
from process import process

"""
múltiplos núcleos
fila de menor prioridade não precisa executar só quando a fila de maior prioridade estiver vazia.
há processos de sistema que nunca acabam
"""

s = scheduler()

for i in range(15):
    s.add_process(process(random.randint(0,2)))

print("INÍCIO\n")
while not s.is_over():
    s.execute()
    print(s.get_context(), "\n")
    time.sleep(1)

print("FIM")