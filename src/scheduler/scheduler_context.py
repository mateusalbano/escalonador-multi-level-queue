from scheduler.scheduler import Scheduler
from process.process import Process
from cpu import Cpu

class SchedulerContext:
    def __init__(self, scheduler: Scheduler, cpus: list[Cpu]):
        self.__scheduler = scheduler
        self.__cpus = cpus


    def get(self) -> str:
        """Return a snapshot of the scheduler's state as a string.

        Includes per-CPU assignments, ready queues by type, waiting list and
        dead processes. Processes are formatted as p{pid}.
        """
        lines = []

        # CPUs
        lines.append("CPUs:")
        # helper for converting process type constants to human-readable names

        for cpu in self.__cpus:
            if cpu.is_idle():
                lines.append(f"  CPU{cpu.get_core_id()}: idle")
            else:
                proc = cpu.get_current_process()
                ptype = self.__get_process_type_str(proc.get_type())
                lines.append(
                    f"  CPU{cpu.get_core_id()}: p{proc.get_pid()} ({ptype}) "
                    f"(time_slice={cpu.get_time_slice()})"
                )

        
        system_procs = self.__scheduler.get_system_processes()
        interactive_procs = self.__scheduler.get_interactive_processes()
        batch_procs = self.__scheduler.get_batch_processes()

        lines.append("Ready:")
        lines.append(f"  System: {self.__get_processes_str(system_procs)}")
        lines.append(f"  Interactive: {self.__get_processes_str(interactive_procs)}")
        lines.append(f"  Batch: {self.__get_processes_str(batch_procs)}")

        # waiting and dead

        wait_procs = self.__scheduler.get_wait_processes()
        dead_procs = self.__scheduler.get_dead_processes()

        lines.append(f"Waiting: {self.__get_processes_str(wait_procs)}")
        lines.append(f"Dead: {self.__get_processes_str(dead_procs)}")

        return "\n".join(lines)
    
    
    def __get_process_type_str(self, type: int):
        type_names = {
            Process.SYSTEM_PROCESS: "system",
            Process.INTERACTIVE_PROCESS: "interactive",
            Process.BATCH_PROCESS: "batch",
        }
        return type_names[type]

    def __get_processes_str(self, processes: list):
        return ", ".join([str(p) for p in processes])
    
