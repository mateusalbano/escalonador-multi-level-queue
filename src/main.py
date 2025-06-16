import threading
import time
import tkinter as tk
import tkinter.messagebox
from process import process
from scheduler import scheduler

# função de validação para aceitar apenas números
def validar_numero(valor):
    return valor.isdigit() or valor == ""

root = tk.Tk()
root.title("Escalonador de múltiplas filas")
root.geometry("700x500")

vcmd = (root.register(validar_numero), "%P")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

labels = ["processos de sistema:", "processos interativos:", "processos batch:", "clock:"]
entries = []

entry = None
for i, label in enumerate(labels):
    tk.Label(frame_top, text=label).grid(row=0, column=i*2, padx=5)
    entry = tk.Entry(frame_top, width=5, justify='center',
                     validate="key", validatecommand=vcmd)
    entry.insert(tk.END, "5")
    entry.grid(row=0, column=i*2+1, padx=5)
    entries.append(entry)
entry.delete('0', tk.END)
entry.insert(tk.END, "1")

frame_exec = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
frame_exec.pack(padx=20, pady=10, fill="both", expand=True)

tk.Label(frame_exec, text="Execução:").pack(anchor="w")

text_exec = tk.Text(frame_exec, height=12, wrap="word", state="disabled", font=("Consolas", 16))
text_exec.pack(fill="both", expand=True)

#variáveis globais
escalonador = None
executando = False

def escrever(texto: str):
    text_exec.config(state="normal")
    text_exec.insert(tk.END, texto)
    text_exec.config(state="disabled")

def run():
    global executando
    global escalonador
    while executando and not escalonador.is_over():
        text_exec.config(state="normal")
        text_exec.delete('1.0', tk.END)
        escrever(escalonador.get_context())
        time.sleep(escalonador.get_clock())

    escrever("\nFIM")
    if escalonador.started():
        escalonador.end()
    btn.config(text="iniciar")
    btn["state"] = "normal"
    tkinter.messagebox.showinfo(message="Fim da execução!")
    executando = False

def input_valido() -> bool:
    val1 = int(entries[0].get()) if entries[0].get() else 0
    val2 = int(entries[1].get()) if entries[0].get() else 0
    val3 = int(entries[2].get()) if entries[0].get() else 0
    total = val1 + val2 + val3
    
    if total < 1 or total > 50:
        tkinter.messagebox.showwarning(message="Número de processos deve estar entre 1 e 50.")
        return False
    
    val4 = int(entries[3].get()) if entries[0].get() else 0
    if val4 < 1 or val4 > 10:
        tkinter.messagebox.showwarning(message="Tempo de clock deve estar entre 1 e 10.")
    return True
    

def iniciar_parar():
    global executando
    global escalonador
    executando = not executando

    if executando:
        if not input_valido():
            executando = False
            return
        btn.config(text="parar")
        text_exec.delete('1.0', tk.END)
    else:
        btn.config(text="iniciar")
        escalonador.end()
        btn["state"] = "disabled"
        return

    n_sistemas = int(entries[0].get()) if entries[0].get() else 0
    n_interativos = int(entries[1].get()) if entries[1].get() else 0
    n_batchs = int(entries[2].get()) if entries[2].get() else 0
    clock = int(entries[3].get()) if entries[2].get() else 0
    escalonador = scheduler(clock=clock)


    for _ in range(int(n_sistemas / 2)):
        escalonador.add_process(process(process.SYSTEM_PROCESS))

    n_sistemas_inf = int(n_sistemas / 2) if n_sistemas % 2 == 0 else int(n_sistemas / 2) + 1

    for _ in range(n_sistemas_inf):
        escalonador.add_process(process(process.SYSTEM_PROCESS, ends=False))

    for _ in range(n_interativos):
        escalonador.add_process(process(process.INTERACTIVE_PROCESS))

    for _ in range(n_batchs):
        escalonador.add_process(process(process.BATCH_PROCESS))

    escalonador.start()
    thread = threading.Thread(target=run)
    thread.start()


btn = tk.Button(root, text="iniciar", width=15, command=iniciar_parar)
btn.pack(side="right", padx=20, pady=10)

root.mainloop()
