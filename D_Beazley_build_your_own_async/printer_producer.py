"""
Producer.py with additional prints
"""
import time
from collections import deque
import heapq


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
            print(f"ready: {self.ready}", f"sleeping: {self.sleeping}", sep="\n-----\n")  # print added
            if not self.ready:
                deadline, _, func = heapq.heappop(self.sleeping)  # self.sleeping.pop(0)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(func)

            while self.ready:
                func = self.ready.popleft()
                func()


class AsyncQueue:
    def __init__(self):
        self.items = deque()    # items being queued
        self.waiters = deque()  # all getters waiting for data

    def put(self, item):
        print(f"Calling 'put' for {item}")  # print added
        self.items.append(item)
        if self.waiters:
            func = self.waiters.popleft()
            scheduler.call_soon(func)

    def get(self, callback):  # suppose to wait until an item is available and then return it
        print(f"Calling 'get' for {callback}")  # print added
        if self.items:
            callback(self.items.popleft())
        else:
            self.waiters.append(lambda: self.get(callback))
            print(f"waiters: {self.waiters}")   # print added


def producer(q, count):
    def _produce(n):
        if n < count:
            print('Producing', n)
            q.put(n)
            scheduler.call_later(4, lambda: _produce(n+1))
        else:
            print('Producer done')
            q.put(None)
    _produce(0)


def consumer(q):
    def _consume(item):
        if item is None:
            print('Consumer done')
        else:
            print('Consuming', item)
            scheduler.call_soon(lambda: consumer(q))  # like recursive call
    q.get(callback=_consume)


scheduler = Scheduler()

q = AsyncQueue()

scheduler.call_soon(lambda: producer(q, 10))
scheduler.call_soon(lambda: consumer(q))
scheduler.run()
