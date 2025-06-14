import random
import time
from process import process
from scheduler import scheduler

"""
**Lista de afazeres:**

- múltiplos núcleos (feito)
- fila de menor prioridade não precisa executar só quando a fila de maior prioridade estiver vazia (feito)
- há processos de sistema que nunca acabam (não feito)
- desenvolver uma interface de linha de comando para utilizar o programa (não feito)

Adicional:

- plotar um gráfico com o tempo de execução de cada processo ou fila (não feito)
"""

s = scheduler(clock=1)

for i in range(15):
    s.add_process(process(random.randint(0, 2)))

print("START\n")
s.start()
while not s.is_over():
    print(s.get_context(), "\n")
    time.sleep(s.get_clock())

s.end()
print(s.get_context(), "\n")
print("END")