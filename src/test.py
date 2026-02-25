import random
import time

from process.commom_process import CommomProcess
from process.interactive_process import InteractiveProcess
from process.process import Process
from scheduler.scheduler import Scheduler
from scheduler.scheduler_context import SchedulerContext


scheduler = Scheduler(clock=1)
sc = SchedulerContext(scheduler)


for i in range(5):
    scheduler.add_process(CommomProcess(Process.SYSTEM_PROCESS))


for i in range(5):
    scheduler.add_process(CommomProcess(Process.BATCH_PROCESS))

for i in range(5):
    behaviour = random.choice([Process.CPU_BOUND, Process.IO_BOUND])
    scheduler.add_process(InteractiveProcess(behaviour))

scheduler.start()



while not scheduler.is_over():
    ctx = sc.get()
    print(ctx)
    time.sleep(1)

final_ctx = sc.get()
print(final_ctx)


print("finished")