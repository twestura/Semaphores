"""
Barrier - n threads wait until they have all reached the same point,
          then they proceed.
"""


import random
import sys
import time
import threading
from threading import Semaphore, Thread


class Barrier(object):
    """
    Threads wait at the barrier until n have called passThrough.

    After n have passed through the barrier, another round
    can be started by using passThrough again.
    """

    def __init__(self, n):
        """
        Initializes a new Barrier for n threads.

        Parameters:
            n - The number of threads needed to pass the barrier.
                A positive int.
        """
        self._totalThreads = int(n)
        self._waitingPhase = 0  # The index on which to wait
        self._currentThreads = 0  # 0 <= _currentThreads < _totalThreads
        self._threadsWaiting = (Semaphore(0), Semaphore(0))
        self._barrierMutex = Semaphore(1)

    def passThrough(self):
        """
        Attempt to pass through the barrier, blocking until all threads arrive.
        """
        self._barrierMutex.acquire()
        self._currentThreads += 1
        if self._currentThreads == self._totalThreads:
            # _currentThreads - 1 threads are waiting
            while self._currentThreads != 1:
                self._threadsWaiting[self._waitingPhase].release()
                self._currentThreads -= 1
            self._currentThreads -= 1 # adjust for the current thread
            self._waitingPhase = (self._waitingPhase + 1) % 2
            self._barrierMutex.release()
        else:
            self._barrierMutex.release()
            self._threadsWaiting[self._waitingPhase].acquire()


def _delay():
    """Sleep for a random interval."""
    time.sleep(random.randint(0, 2))


count = 0  # pylint: disable=invalid-name
COUNT_MUTEX = Semaphore(1)
DEFAULT_ITERATIONS = 5
class Worker(object):
    """
    A thread to increment and decrement a shared count variable.
    """

    def __init__(self, barrier, idnum):
        """
        Initializes a new worker that uses a barrier.

        Parameters:
            barrier - The barrier to use.
            idnum - The id number of this Worker, an int.
        """
        self._barrier = barrier
        self._id = int(idnum)
        self._numIterations = DEFAULT_ITERATIONS

    def run(self):  # pylint: disable=no-self-use
        """
        Increments count.
        """
        global count  # pylint: disable=global-statement,invalid-name
        for _ in xrange(self._numIterations):
            _delay()
            COUNT_MUTEX.acquire()
            count += 1
            COUNT_MUTEX.release()
            self._barrier.passThrough()

            # don't print until every thread has incremented the count
            COUNT_MUTEX.acquire()
            print '{}, count is {}'.format(threading.current_thread().name,
                                           count)
            COUNT_MUTEX.release()
            self._barrier.passThrough()

            # don't decrement until every thread has printed the count
            _delay()
            COUNT_MUTEX.acquire()
            count -= 1
            COUNT_MUTEX.release()
            self._barrier.passThrough()

            # don't print until every thread has decremented the count
            COUNT_MUTEX.acquire()
            print '{}, count is {}'.format(threading.current_thread().name,
                                           count)
            COUNT_MUTEX.release()
            self._barrier.passThrough()


def main():
    """
    Runs a Barrier test.
    """
    num_threads = 25
    barrier = Barrier(num_threads)
    for k in xrange(num_threads):
        Thread(target=Worker(barrier, k).run,
               name='Thread {}'.format(k)).start()
    return 0


if __name__ == '__main__':
    sys.exit(main())

