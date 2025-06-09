from scheduler import scheduler
from process import process

s = scheduler()

p1 = process(process.SYSTEM_PROCESS)
p2 = process(process.INTERACTIVE_PROCESS)
p3 = process(process.BATCH_PROCESS)
p4 = process(process.SYSTEM_PROCESS)
p5 = process(process.INTERACTIVE_PROCESS)
p6 = process(process.BATCH_PROCESS)
'''
'''

s.add_process(p1)
s.add_process(p2)
s.add_process(p3)
s.add_process(p4)
s.add_process(p5)
s.add_process(p6)
'''
'''
print("INÍCIO")
while not s.is_over():
    s.execute()

print("FIM")