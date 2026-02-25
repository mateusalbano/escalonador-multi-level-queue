import random
import threading
import time
import tkinter as tk
import tkinter.messagebox as mb
from process.process import Process
from scheduler.scheduler import Scheduler
from process.commom_process import CommomProcess
from process.interactive_process import InteractiveProcess
from scheduler.scheduler_context import SchedulerContext

root = tk.Tk()
root.title("Escalonador de múltiplas filas")
root.geometry("1000x750")
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

# lista de labels
labels = ["processos de sistema:", "processos interativos:", "processos batch:", "processos permanentes:", "clock:", "cpus:"]

# lista de spins
spins = []

for i, label in enumerate(labels):
    tk.Label(frame_top, text=label).grid(row=0, column=i*2, padx=5)
    spinbox = tk.Spinbox(frame_top, justify='center', from_=0, width=5, to=15, textvariable=tk.StringVar(value=5))
    spinbox.grid(row=0, column=i*2+1, padx=5)
    spins.append(spinbox)

# altera configurações de alguns spinboxes específicos
spins[3].config(from_=0, to=45, textvariable=tk.StringVar(value=1))
spins[4].config(from_=0.2, to=3, increment=0.2, textvariable=tk.StringVar(value=1.0))
spins[5].config(from_=1, to=20, textvariable=tk.StringVar(value=4))

frame_exec = tk.Frame(root, bd=2, padx=10, pady=10)
frame_exec.pack(padx=20, pady=10, fill="both", expand=True)

tk.Label(frame_exec, text="Execução:").pack(anchor="w")

text_exec = tk.Text(frame_exec, height=12, wrap="word", state="disabled", font=("Consolas", 16))
text_exec.pack(fill="both", expand=True)

scroll = tk.Scrollbar(text_exec, command=text_exec.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

text_exec.config(yscrollcommand=scroll.set)

#variáveis globais
escalonador = None
contexto = None
executando = False

# função que escreve no campo de texto, mantendo-o inalterável pelo usuário.
def escrever(texto: str):
    text_exec.config(state="normal")
    text_exec.replace('1.0', tk.END, texto)
    text_exec.config(state="disabled")

# valida se o usuário escolheu pelo menos 1 processo e se o número de processos permanentes é válido.
def entrada_valida() -> bool:
    sum = int(spins[0].get()) + int(spins[1].get()) + int(spins[2].get())
    if not sum > 0:
        mb.showwarning(message="Deve haver no mínimo um processo.", title="Aviso")
        return False
    
    if int(spins[3].get()) > sum:
        mb.showwarning(message="Número de processos permanentes deve ser menor ou igual ao número de processos.", title="Aviso")
        return False

    return True

# função executada em paralelo para atualizar o campo de texto.
def run():
    global executando
    global escalonador
    global contexto
    while executando and not escalonador.is_over():
        escrever(contexto.get())
        time.sleep(escalonador.get_clock())

    escrever(contexto.get())
    text_exec.config(state="normal")
    text_exec.insert(tk.END, "\nEND")
    text_exec.config(state="disabled")
    if escalonador.started():
        escalonador.stop()
    btn.config(text="iniciar")
    btn["state"] = "normal"
    mb.showinfo(title="Mensagem", message="Fim da execução!")
    executando = False
    
# função associada ao botão de iniciar ou parar
def iniciar_parar():
    global executando
    global escalonador
    global contexto
    executando = not executando

    if executando:
        if not entrada_valida():
            executando = False
            return

        btn.config(text="parar")
        text_exec.delete('1.0', tk.END)
    else:
        btn.config(text="iniciar")
        escalonador.stop()
        btn["state"] = "disabled"
        return

    n_sistemas = int(spins[0].get())
    n_interativos = int(spins[1].get())
    n_batchs = int(spins[2].get())
    n_permanentes = int(spins[3].get())
    total = n_sistemas + n_interativos + n_batchs
    processos_permanentes = [False for _ in range(n_permanentes)]
    processos_permanentes.extend([True for _ in range(total - n_permanentes)])
    random.shuffle(processos_permanentes)
    clock = float(spins[4].get())
    n_cpus = int(spins[5].get())
    escalonador = Scheduler(clock=clock, n_cpus=n_cpus)
    contexto = SchedulerContext(escalonador)

    for _ in range(n_sistemas):
        escalonador.add_process(CommomProcess(type=Process.SYSTEM_PROCESS, num_instructions=random.randint(7, 15), ends=processos_permanentes.pop()))

    for _ in range(n_interativos):
        escalonador.add_process(InteractiveProcess(behaviour=random.choice([Process.IO_BOUND, Process.CPU_BOUND]), num_instructions=random.randint(7, 15), ends=processos_permanentes.pop()))

    for _ in range(n_batchs):
        escalonador.add_process(CommomProcess(type=Process.BATCH_PROCESS, num_instructions=random.randint(7, 15), ends=processos_permanentes.pop()))

    escalonador.start()
    thread = threading.Thread(target=run)
    thread.start()

btn = tk.Button(root, text="iniciar", width=15, command=iniciar_parar)
btn.pack(side="right", padx=20, pady=10)

root.mainloop()