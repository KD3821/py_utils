"""
Version with coroutines
"""
import time
from collections import deque
import heapq


class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.sleeping = list()
        self.current = None    # currently executing generator
        self.order = 0

    async def sleep(self, delay):
        deadline = time.time() + delay
        self.order += 1
        heapq.heappush(self.sleeping, (deadline, self.order, self.current))
        self.current = None  # "Disappear"
        await switch()

    def new_task(self, coro):
        self.ready.append(coro)  # rename gen to coro

    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                deadline, _, coro = heapq.heappop(self.sleeping)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(coro)

            self.current = self.ready.popleft()

            try:
                self.current.send(None)  # instead of next(self.current)
                if self.current:
                    self.ready.append(self.current)
            except StopIteration:
                pass


class Awaitable:
    def __await__(self):
        yield


def switch():
    return Awaitable()


class QueueClosed(Exception):
    pass


class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.waiters = deque()
        self._closed = False

    def close(self):
        self._closed = True

        if self.waiters and not self.items:
            scheduler.ready.append(self.waiters.popleft())  # Rescheduling waiting tasks

    async def put(self, item):
        if self._closed:
            raise QueueClosed()

        self.items.append(item)

        if self.waiters:
            scheduler.ready.append(self.waiters.popleft())

    async def get(self):
        while not self.items:
            if self._closed:
                raise QueueClosed()

            self.waiters.append(scheduler.current)  # Put myself to sleep
            scheduler.current = None  # "Disappear"
            await switch()           # Switch to another task

        return self.items.popleft()


async def producer(q, count):
    for n in range(count):
        print('Producing', n)
        await q.put(n)
        await scheduler.sleep(1)

    print('Producer is done')
    q.close()  # instead await q.put(None)  # "Sentinel" to shut down


async def consumer(q):
    try:
        while True:
            item = await q.get()
            print('Consuming', item)
    except QueueClosed:
        print('Consumer is done')


scheduler = Scheduler()

aq = AsyncQueue()
scheduler.new_task(producer(aq, 10))
scheduler.new_task(consumer(aq))
scheduler.run()


# ---------------------


async def count_down(n):
    while n > 0:
        print('Down', n)
        await scheduler.sleep(1)  # instead time.sleep(1)
        # await switch()  # instead of yield (later: no need because handled in scheduler.sleep())
        n -= 1


async def count_up(stop):
    x = 0
    while x < stop:
        print('Up', x)
        await scheduler.sleep(1)  # instead time.sleep(1)
        # await switch()  # instead of yield (later: no need because handled in scheduler.sleep())
        x += 1

# scheduler.new_task(count_down(5))
# scheduler.new_task(count_up(5))
# scheduler.run()


"""
1:11:00 - starts
https://www.youtube.com/watch?v=Y4Gt3Xjd7G8
"""
