"""
Start from this module & follow this order: asynco.py > producer.py (printer_producer.py) > yieldo.py > aio_producer.py
"""
import time
import heapq
from collections import deque


class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.sleeping = list()
        self.order = 0

    def call_soon(self, func):
        self.ready.append(func)

    def call_later(self, delay, func):
        self.order += 1
        deadline = time.time() + delay
        heapq.heappush(self.sleeping, (deadline, self.order, func))  # instead of self.sleeping.sort()

    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                deadline, _, func = heapq.heappop(self.sleeping)  # self.sleeping.pop(0)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(func)

            while self.ready:
                func = self.ready.popleft()
                func()


scheduler = Scheduler()


def count_down(n):
    if n > 0:
        print('Down', n)
        scheduler.call_later(4, lambda: count_down(n-1))  # lambda is for making zero-argument function


def count_up(stop):
    def _run(x):  # instead of carrying x and having a default x=0
        if x < stop:
            print('Up', x)
            scheduler.call_later(1, lambda: _run(x+1))  # instead of time.sleep(1) we use call_later
    _run(0)


# def count_up(stop, x=0):
#     if x < stop:
#         print('Up', x)
#         time.sleep(1)
#         scheduler.call_soon(lambda: count_up(stop, x+1))


scheduler.call_soon(lambda: count_down(5))
scheduler.call_soon(lambda: count_up(20))
scheduler.run()
