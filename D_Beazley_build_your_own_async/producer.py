"""
Version with callbacks
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
            if not self.ready:
                deadline, _, func = heapq.heappop(self.sleeping)  # self.sleeping.pop(0)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(func)

            while self.ready:
                func = self.ready.popleft()
                func()


class Result:
    def __init__(self, value=None, exc=None):
        self.value = value
        self.exc = exc

    def check(self):
        if self.exc:
            raise self.exc
        else:
            return self.value


class AsyncQueue:
    def __init__(self):
        self.items = deque()    # items being queued
        self.waiters = deque()  # all getters waiting for data
        self._closed = False    # queue can't be used when is True

    def close(self):
        self._closed = True
        if self.waiters and not self.items:
            for func in self.waiters:
                scheduler.call_soon(func)

    def put(self, item):
        if self._closed:
            raise QueueClosed()
        self.items.append(item)
        if self.waiters:
            func = self.waiters.popleft()
            scheduler.call_soon(func)

    def get(self, callback):  # suppose to wait until an item is available and then return it
        if self.items:
            callback(Result(value=self.items.popleft()))
        else:
            if self._closed:
                callback(Result(exc=QueueClosed()))
            else:
                self.waiters.append(lambda: self.get(callback))


class QueueClosed(Exception):
    pass


def producer(q, count):
    def _produce(n):
        if n < count:
            print('Producing', n)
            q.put(n)
            scheduler.call_later(1, lambda: _produce(n+1))
        else:
            print('Producer done')
            q.close()  # means no more new items will be produced  - instead of: q.put(None)
    _produce(0)


def consumer(q):
    def _consume(result):
        try:
            item = result.check()
            print('Consuming', item)
            scheduler.call_soon(lambda: consumer(q))  # like recursive call
        except QueueClosed:
            print('Consumer done')
    q.get(callback=_consume)


scheduler = Scheduler()

q = AsyncQueue()

scheduler.call_soon(lambda: producer(q, 10))
# scheduler.call_soon(lambda: producer(q, 5))  #  need to change q.close() to keep it 'open' if other producer's running
scheduler.call_soon(lambda: consumer(q))  # can be more than one consumer
scheduler.run()
