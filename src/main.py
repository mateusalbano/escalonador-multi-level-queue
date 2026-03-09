import random
import threading
import time
import tkinter as tk
import tkinter.messagebox as mb
from typing import Optional

from process.process import Process, ProcessBehaviour, ProcessType
from process.commom_process import CommomProcess
from process.interactive_process import InteractiveProcess
from scheduler.scheduler_simulation import SchedulerSimulation


class UIConfig:
    WINDOW_TITLE = "escalonador de múltiplas filas"
    WINDOW_SIZE = "1000x750"
    TEXT_FONT = ("Consolas", 16)
    PADDING_Y = 10
    PADDING_X = 20
    SPINBOX_WIDTH = 5
    BUTTON_WIDTH = 15
    TEXT_HEIGHT = 12


class SpinboxConfig:
    LABELS = [
        "processos de sistema:",
        "processos interativos:",
        "processos batch:",
        "processos permanentes:",
        "clock:",
        "cpus:",
    ]
    
    CONFIGS = [
        {"from_": 0, "to": 15, "value": 5},      # system processes
        {"from_": 0, "to": 15, "value": 5},      # interactive processes
        {"from_": 0, "to": 15, "value": 5},      # batch processes
        {"from_": 0, "to": 45, "value": 1},      # permanent processes
        {"from_": 0.2, "to": 3, "increment": 0.2, "value": 1.0},  # clock_rate
        {"from_": 1, "to": 20, "value": 4},      # cpus
    ]

class ProcessConfig:
    MIN_INSTRUCTIONS = 7
    MAX_INSTRUCTIONS = 15


class SchedulerApp:
    
    def __init__(self, root: tk.Tk):
        self.__root = root
        self.__simulator: Optional[SchedulerSimulation] = None
        self.__running = False
        self.__spinboxes = []
        self.__text_output = None
        self.__start_button = None
        
        self.__setup_ui()
    
    def __setup_ui(self):
        self.__root.title(UIConfig.WINDOW_TITLE)
        self.__root.geometry(UIConfig.WINDOW_SIZE)
        
        self.__create_input_frame()
        self.__create_output_frame()
        self.__create_button()

    
    def __create_input_frame(self):
        frame = tk.Frame(self.__root)
        frame.pack(pady=UIConfig.PADDING_Y)
        
        for i, label_text in enumerate(SpinboxConfig.LABELS):
            tk.Label(frame, text=label_text).grid(row=0, column=i * 2, padx=5)
            
            config = SpinboxConfig.CONFIGS[i]
            spinbox = tk.Spinbox(
                frame,
                justify='center',
                width=UIConfig.SPINBOX_WIDTH,
                textvariable=tk.StringVar(value=str(config["value"])),
                **{k: v for k, v in config.items() if k != "value"}
            )
            spinbox.grid(row=0, column=i * 2 + 1, padx=5)
            self.__spinboxes.append(spinbox)
    
    def __create_output_frame(self):
        frame = tk.Frame(self.__root, bd=2, padx=10, pady=10)
        frame.pack(padx=UIConfig.PADDING_X, pady=UIConfig.PADDING_Y, fill="both", expand=True)
        
        tk.Label(frame, text="Execução:").pack(anchor="w")
        
        self.__text_output = tk.Text(
            frame,
            height=UIConfig.TEXT_HEIGHT,
            wrap="word",
            state="disabled",
            font=UIConfig.TEXT_FONT
        )
        self.__text_output.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(self.__text_output, command=self.__text_output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__text_output.config(yscrollcommand=scrollbar.set)

    
    """Create the start/stop button"""
    def __create_button(self):
        self.__start_button = tk.Button(
            self.__root,
            text="iniciar",
            width=UIConfig.BUTTON_WIDTH,
            command=self.__on_start_stop_clicked
        )
        self.__start_button.pack(side="right", padx=UIConfig.PADDING_X, pady=UIConfig.PADDING_Y)

    
    def __get_input_values(self) -> dict:
        return {
            "system": int(self.__spinboxes[0].get()),
            "interactive": int(self.__spinboxes[1].get()),
            "batch": int(self.__spinboxes[2].get()),
            "permanent": int(self.__spinboxes[3].get()),
            "clock_rate": float(self.__spinboxes[4].get()),
            "cpus": int(self.__spinboxes[5].get()),
        }
    
    def __is_valid_input(self) -> bool:
        values = self.__get_input_values()
        total_processes = values["system"] + values["interactive"] + values["batch"]
        
        if total_processes == 0:
            mb.showwarning(
                message="Deve haver no mínimo um processo.",
                title="Aviso"
            )
            return False
        
        if values["permanent"] > total_processes:
            mb.showwarning(
                message="Número de processos permanentes deve ser menor ou igual ao número de processos.",
                title="Aviso"
            )
            return False
        
        return True
    
    def __clear_output(self):
        self.__update_output("")


    def __update_output(self, text: str):
        self.__text_output.config(state="normal")
        self.__text_output.replace('1.0', tk.END, text)
        self.__text_output.config(state="disabled")

    
    def __create_permanent_flags(self, total: int, permanent_count: int) -> list[bool]:
        flags = [True] * permanent_count + [False] * (total - permanent_count)
        random.shuffle(flags)
        return flags
    

    def __populate_processes(self, values: dict, permanent_flags: list[bool]):

        def get_num_instructions():
            if permanent_flags.pop():
                return Process.INFINITE_INSTRUCTIONS
            
            return random.randint(ProcessConfig.MIN_INSTRUCTIONS, ProcessConfig.MAX_INSTRUCTIONS)

        for _ in range(values["system"]):
            num_instruc = get_num_instructions()

            proc = CommomProcess(type=ProcessType.SYSTEM_PROCESS, num_instructions=num_instruc)
            self.__simulator.add_process(proc)
        
        for _ in range(values["interactive"]):
            behaviour = random.choice([ProcessBehaviour.IO_BOUND, ProcessBehaviour.CPU_BOUND])
            num_instruc = get_num_instructions()

            proc = InteractiveProcess(behaviour=behaviour, num_instructions=num_instruc)
            self.__simulator.add_process(proc)
        
        for _ in range(values["batch"]):
            num_instruc = get_num_instructions()
            proc = CommomProcess(type=ProcessType.BATCH_PROCESS, num_instructions=num_instruc)
            self.__simulator.add_process(proc)
    

    def __run_simulator(self):
        while self.__running and not self.__simulator.is_over():
            self.__update_output(self.__simulator.get_context())
            time.sleep(self.__simulator.get_clock_rate())
        
        # Final update
        self.__update_output(self.__simulator.get_context() + "\nEND")
        
        if self.__simulator.is_running():
            self.__simulator.stop()
        
        self.__start_button.config(text="iniciar")
        self.__start_button["state"] = "normal"
        mb.showinfo(title="Mensagem", message="Fim da execução!")
        self.__running = False
    
    def __start_simulation(self):
        if not self.__is_valid_input():
            self.__running = False
            return
        
        self.__start_button.config(text="parar")
        self.__clear_output()
        
        values = self.__get_input_values()
        total = values["system"] + values["interactive"] + values["batch"]
        permanent_flags = self.__create_permanent_flags(total, values["permanent"])
        
        self.__simulator = SchedulerSimulation(clock_rate=values["clock_rate"], n_cpus=values["cpus"])
        self.__populate_processes(values, permanent_flags)
        
        self.__simulator.start()
        thread = threading.Thread(target=self.__run_simulator, daemon=True)
        thread.start()
    
    def __stop_simulation(self):
        self.__start_button.config(text="iniciar")
        self.__simulator.stop()
        self.__start_button["state"] = "disabled"

    
    """Handle start/stop button click"""
    def __on_start_stop_clicked(self):
        self.__running = not self.__running
        
        if self.__running:
            self.__start_simulation()
        else:
            self.__stop_simulation()


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()