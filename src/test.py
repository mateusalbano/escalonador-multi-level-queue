import random
import time

from process.commom_process import CommomProcess
from process.interactive_process import InteractiveProcess
from process.process import Process, ProcessBehaviour, ProcessType
from scheduler.scheduler_simulation import SchedulerSimulation

clock =  0.5
scheduler_sim = SchedulerSimulation(clock=clock)


for i in range(5):
    scheduler_sim.add_process(CommomProcess(ProcessType.SYSTEM_PROCESS))


for i in range(5):
    scheduler_sim.add_process(CommomProcess(ProcessType.BATCH_PROCESS))

for i in range(5):
    behaviour = random.choice([ProcessBehaviour.CPU_BOUND, ProcessBehaviour.IO_BOUND])
    scheduler_sim.add_process(InteractiveProcess(behaviour))

scheduler_sim.start()

elapsed_time = 0
while not scheduler_sim.is_over():
    ctx = scheduler_sim.get_context()
    print(ctx)
    time.sleep(clock)
    elapsed_time += 1
    if elapsed_time % 10 == 0:
        scheduler_sim.add_process(CommomProcess(ProcessType.SYSTEM_PROCESS))

final_ctx = scheduler_sim.get_context()
scheduler_sim.stop()

print(final_ctx)
print("finished")