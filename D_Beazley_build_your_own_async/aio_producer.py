"""
Version with Callback_Scheduler and Coroutines pretending being Callbacks  (FINAL VERSION)
"""
import time
import socket
import heapq
from collections import deque
from select import select


# Callback scheduler with add-ons (from producer.py)
class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.sleeping = list()
        self._read_waiting = dict()
        self._write_waiting = dict()
        self.current = None
        self.order = 0

    def call_soon(self, func):
        self.ready.append(func)

    def call_later(self, delay, func):
        self.order += 1
        deadline = time.time() + delay
        heapq.heappush(self.sleeping, (deadline, self.order, func))  # instead of self.sleeping.sort()

    def read_wait(self, fileno, func):   # to trigger func() when fileno is readable
        self._read_waiting[fileno] = func

    def write_wait(self, fileno, func):  # to trigger func() when fileno is writeable
        self._write_waiting[fileno] = func

    def run(self):
        while self.ready or self.sleeping or self._read_waiting or self._write_waiting:
            if not self.ready:
                timeout = None

                if self.sleeping:
                    deadline = self.sleeping[0][0]  # self.sleeping.pop(0)
                    timeout = deadline - time.time()
                    if timeout < 0:
                        timeout = 0

                can_read, can_write, _ = select(self._read_waiting, self._write_waiting, [], timeout)  # waiting for I/O

                for fd in can_read:
                    self.ready.append(self._read_waiting.pop(fd))
                for fd in can_write:
                    self.ready.append(self._write_waiting.pop(fd))

                now = time.time()  # check for sleeping task
                while self.sleeping:
                    if now > self.sleeping[0][0]:
                        self.ready.append(heapq.heappop(self.sleeping)[2])
                    else:
                        break

            while self.ready:
                func = self.ready.popleft()
                func()

    def new_task(self, coro):
        self.ready.append(Task(coro))

    async def sleep(self, delay):
        self.call_later(delay, self.current)
        self.current = None
        await switch()

    async def recv(self, sock, maxbytes):
        self.read_wait(sock, self.current)
        self.current = None
        await switch()
        return sock.recv(maxbytes)

    async def send(self, sock, data):
        self.write_wait(sock, self.current)
        self.current = None
        await switch()
        return sock.send(data)

    async def accept(self, sock):
        self.read_wait(sock, self.current)
        self.current = None
        await switch()
        return sock.accept()


class Task:
    def __init__(self, coro):
        self.coro = coro  # wrapping a coroutine

    def __call__(self):   # to make coroutine look like a callback
        try:
            scheduler.current = self
            self.coro.send(None)
            if scheduler.current:
                scheduler.ready.append(self)
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

        # if self.waiters and not self.items:  # my fix in case of few producers and few consumers
        #     self._closed = True
        #     for waiter in self.waiters:
        #         scheduler.ready.append(waiter)

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
            await switch()            # Switch to another task

        return self.items.popleft()


async def producer(q, count):
    for n in range(count):
        print('Producing', n)
        await q.put(n)
        await scheduler.sleep(1)

    print('Producer is done')
    q.close()  # instead of await q.put(None)  # "Sentinel" to shut down


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
# scheduler.run()


# now we can also run callbacks
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


scheduler.call_soon(lambda: count_down(5))
scheduler.call_soon(lambda: count_up(20))
# scheduler.run()


# now we can also run I/O
async def tcp_server(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(2)
    while True:
        client, addr = await scheduler.accept(sock)
        print(f'Connection from {addr}')
        scheduler.new_task(echo_handler(client))


async def echo_handler(sock):
    while True:
        data = await scheduler.recv(sock, 10000)
        if not data:
            break
        await scheduler.send(sock, b'Got: ' + data)
    print(f'Connection closed {sock.getpeername()}')
    sock.close()


scheduler.new_task(tcp_server(('', 30000)))
scheduler.run()



"""
01:47:00  start
https://www.youtube.com/watch?v=Y4Gt3Xjd7G8
"""