import random
import time
from process import process
from scheduler import scheduler

"""
múltiplos núcleos
fila de menor prioridade não precisa executar só quando a fila de maior prioridade estiver vazia
há processos de sistema que nunca acabam
"""

s = scheduler()

for i in range(15):
    s.add_process(process(random.randint(0, 2)))

print("START\n")

while not s.is_over():
    print(s.get_context(), "\n")
    s.execute()
    time.sleep(1)

print(s.get_context(), "\n")
print("END")