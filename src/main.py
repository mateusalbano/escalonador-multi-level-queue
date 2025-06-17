import random
import threading
import time
import tkinter as tk
import tkinter.messagebox
from process import process
from scheduler import scheduler

root = tk.Tk()
root.title("Escalonador de múltiplas filas")
root.geometry("900x675")
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

# lista de labels
labels = ["processos de sistema:", "processos interativos:", "processos batch:", "clock:", "cores:"]

# lista de spins
spins = []

for i, label in enumerate(labels):
    tk.Label(frame_top, text=label).grid(row=0, column=i*2, padx=5)
    spinbox = tk.Spinbox(frame_top, justify='center', from_=0, width=5, to=15, textvariable=tk.StringVar(value=5))
    spinbox.grid(row=0, column=i*2+1, padx=5)
    spins.append(spinbox)

# altera as configurações do último spinbox adicionado (clock)
spins[3].config(from_=0.2, to=3, increment=0.2, textvariable=tk.StringVar(value=1.0))
spins[4].config(from_=1, to=20, textvariable=tk.StringVar(value=4))

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
executando = False

# função que escreve no campo de texto, mantendo-o inalterável pelo usuário.
def escrever(texto: str):
    text_exec.config(state="normal")
    text_exec.replace('1.0', tk.END, texto)
    text_exec.config(state="disabled")

# valida se o usuário escolheu pelo menos 1 processo.
def entrada_valida() -> bool:
    return int(spins[0].get()) + int(spins[1].get()) + int(spins[2].get()) > 0

# função executada em paralelo para atualizar o campo de texto.
def run():
    global executando
    global escalonador
    while executando and not escalonador.is_over():
        escrever(escalonador.get_context())
        time.sleep(escalonador.get_clock())

    text_exec.config(state="normal")
    text_exec.insert(tk.END, "\nEND")
    text_exec.config(state="disabled")
    if escalonador.started():
        escalonador.end()
    btn.config(text="iniciar")
    btn["state"] = "normal"
    tkinter.messagebox.showinfo(title="Mensagem", message="Fim da execução!")
    executando = False
    
# função associada ao botão de iniciar ou parar
def iniciar_parar():
    global executando
    global escalonador
    executando = not executando

    if executando:
        if not entrada_valida():
            executando = False
            tkinter.messagebox.showwarning(message="Deve haver no mínimo um processo.", title="Aviso")
            return

        btn.config(text="parar")
        text_exec.delete('1.0', tk.END)
    else:
        btn.config(text="iniciar")
        escalonador.end()
        btn["state"] = "disabled"
        return

    n_sistemas = int(spins[0].get())
    n_interativos = int(spins[1].get())
    n_batchs = int(spins[2].get())
    clock = float(spins[3].get())
    n_cores = int(spins[4].get())
    escalonador = scheduler(clock=clock, n_cores=n_cores)

    for _ in range(int(n_sistemas / 2)):
        escalonador.add_process(process(process.SYSTEM_PROCESS, num_instructions= random.randint(7, 15)))

    n_sistemas_inf = int(n_sistemas / 2) if n_sistemas % 2 == 0 else int(n_sistemas / 2) + 1

    for _ in range(n_sistemas_inf):
        escalonador.add_process(process(process.SYSTEM_PROCESS, ends=False))

    for _ in range(n_interativos):
        escalonador.add_process(process(process.INTERACTIVE_PROCESS, num_instructions= random.randint(7, 15)))

    for _ in range(n_batchs):
        escalonador.add_process(process(process.BATCH_PROCESS, num_instructions= random.randint(7, 15)))

    escalonador.start()
    thread = threading.Thread(target=run)
    thread.start()

btn = tk.Button(root, text="iniciar", width=15, command=iniciar_parar)
btn.pack(side="right", padx=20, pady=10)

root.mainloop()