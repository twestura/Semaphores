"""
Mutex - An example of a mutex.
Protects a shared variable.
"""

import sys
from threading import Thread, Semaphore


INITIAL_COUNT = 0
count = INITIAL_COUNT  # pylint: disable=invalid-name
                       # count is global but not constant


class ThreadA(object):
    """
    Example thread A.
    """

    def __init__(self, mutex):
        """
        Initializes a new ThreadA to increment the count variable.

        Parameters:
            mutex - A semaphore to lock access to count.
        """
        self._mutex = mutex

    def run(self):
        """
        Increments count.
        """
        global count  # pylint: disable=global-statement,invalid-name
        self._mutex.acquire()
        count = count + 1
        self._mutex.release()
        print count


class ThreadB(object):
    """
    Example thread B.
    """

    def __init__(self, mutex):
        """
        Initializes a new ThreadB to increment the count variable.

        Parameters:
            mutex - A semaphore to lock access to count.
        """
        self._mutex = mutex

    def run(self):
        """
        Increments count.
        """
        global count  # pylint: disable=global-statement,invalid-name
        self._mutex.acquire()
        count = count + 1
        print count
        self._mutex.release()


def main():
    """
    Increments the shared variable twice.
    """
    count_mutex = Semaphore(1)
    Thread(target=ThreadA(count_mutex).run).start()
    Thread(target=ThreadB(count_mutex).run).start()
    return 0


if __name__ == '__main__':
    sys.exit(main())
