from scheduler.scheduler import Scheduler
from process.process import Process, ProcessType
from cpu import Cpu

class SchedulerContext:
    def __init__(self, scheduler: Scheduler, cpus: list[Cpu]):
        self.__scheduler = scheduler
        self.__cpus = cpus
        self.__res = None


    def get(self) -> str:
        self.__res = []
        self.__add_cpus_to_res()
        self.__add_scheduler_to_res()

        return "\n".join(self.__res)
    
    
    def __add_cpus_to_res(self):
        self.__res.append("CPUs:")
        for cpu in self.__cpus:
            self.__res.append(f"  {self.__cpu_to_str(cpu)}")

    def __add_scheduler_to_res(self):

        system_procs = self.__scheduler.get_system_processes()
        interactive_procs = self.__scheduler.get_interactive_processes()
        batch_procs = self.__scheduler.get_batch_processes()

        self.__res.append("Ready:")
        self.__res.append(f"  System: {self.__processes_to_str(system_procs)}")
        self.__res.append(f"  Interactive: {self.__processes_to_str(interactive_procs)}")
        self.__res.append(f"  Batch: {self.__processes_to_str(batch_procs)}")

        wait_procs = self.__scheduler.get_waiting_processes()
        dead_procs = self.__scheduler.get_dead_processes()

        self.__res.append(f"Waiting: {self.__processes_to_str(wait_procs)}")
        self.__res.append(f"Dead: {self.__processes_to_str(dead_procs)}")


    def __processes_to_str(self, processes: list[Process]):
        return ", ".join([self.__process_to_str(p) for p in processes])
    
    
    def __cpu_to_str(self, cpu: Cpu) -> str:
        cpu_str = f"CPU{cpu.get_id()}"

        if cpu.is_idle():
            return cpu_str + ": idle"
        
        proc = cpu.get_current_process()
        proc_str = self.__process_to_str(proc)
        type_str = self.__process_type_to_str(proc.get_type())

        return f"{cpu_str}: {proc_str} ({type_str}) (time_slice={cpu.get_time_slice()})"
    
    
    def __process_to_str(self, process: Process) -> str:
        return f"p{process.get_pid()}"
    
    def __process_type_to_str(self, process_type: ProcessType) -> str:
        types = {
            ProcessType.SYSTEM_PROCESS: "system",
            ProcessType.INTERACTIVE_PROCESS: "interactive",
            ProcessType.BATCH_PROCESS: "batch"
        }

        return types[process_type]


    