import time
import random
import threading
from process import process
from scheduler import scheduler
from pyfiglet import Figlet
from pyfiglet import Figlet
from rich.live import Live
from rich.console import Console


"""
**Lista de afazeres:**

- múltiplos núcleos (feito)
- fila de menor prioridade não precisa executar só quando a fila de maior prioridade estiver vazia (feito)
- há processos de sistema que nunca acabam (feito)
- desenvolver uma CLI ou GUI para utilizar o programa (em andamento)

Adicional:

- melhorar a lógica de atribuição de id (não feito)
- plotar um gráfico com o tempo de execução de cada processo ou fila (não feito)
"""

f = Figlet(font='standard')
print(f.renderText('MLQ Scheduler'))

s = scheduler(clock=1)

s.add_process(process(0, ends=True))
s.add_process(process(0, ends=True))
s.add_process(process(0, ends=False))
s.add_process(process(0, ends=False))
s.add_process(process(0, ends=False))
for i in range(10):
    s.add_process(process(random.randint(1, 2)))

stop = False
console = Console()

def run():
    live = Live(console=console, refresh_per_second=1)
    live.update(s.get_context())
    with live:
        while not s.is_over() and not stop:
            live.update(s.get_context())
            time.sleep(s.get_clock())
    s.end()

s.start()

thread = threading.Thread(target=run)
thread.start()
time.sleep(1)
while True:
    if input() == "":
        stop = True
        break