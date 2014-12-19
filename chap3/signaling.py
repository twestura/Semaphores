"""
An example of using a Semaphore to signal.
"""

import sys
from threading import Semaphore, Thread


class ThreadA(object):
    """
    The first process of the example.
    """

    def __init__(self, a1done):
        """
        Initializes the thread to use a Semaphore.

        Parameters:
            a1done - The semaphore to signal.
        """
        self._a1done = a1done

    def run(self):
        """
        Prints 'statement a1'.
        """
        print 'statement a1'
        self._a1done.release()


class ThreadB(object):
    """
    The second process of the example.
    """

    def __init__(self, a1done):
        """
        Initializes the thread to use a Semaphore.

        Parameters:
            a1done - The semaphore on which to wait.
        """
        self._a1done = a1done

    def run(self):
        """
        Prints 'statement b1' after 'statement a1' has already printed.
        """
        self._a1done.acquire()
        print 'statement b1'


def main():
    """
    Prints 'statement a1' followed by 'statement b1'.
    """
    a1done = Semaphore(0)
    Thread(target=ThreadA(a1done).run).start()
    Thread(target=ThreadB(a1done).run).start()
    return 0


if __name__ == '__main__':
    sys.exit(main())


