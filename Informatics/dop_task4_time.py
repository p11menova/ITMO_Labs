import time
from main import main
from dop_task1 import task1
from dop_task2_re import task2


tic = time.perf_counter()
for _ in range(100):
     main()
toc = time.perf_counter()
print('my parser')
print(f"execution time: {toc - tic:0.9f} seconds" + '\n')


tic = time.perf_counter()
for _ in range(100):
     task1()
toc = time.perf_counter()
print('parser+libs')
print(f"execution time: {toc - tic:0.9f} seconds"+'\n')


tic = time.perf_counter()
for _ in range(100):
     task2()
toc = time.perf_counter()
print('parser+regex')
print(f"execution time: {toc - tic:0.9f} seconds" + '\n')
