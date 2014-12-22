"""
Rendezvou - An example in which two Threads must both
make progress an then wait for the other to catch up.
"""

import sys
from threading import Semaphore, Thread


class ThreadA(object):
    """
    The first thread from the example.
    """

    def __init__(self, a1printed, b1printed):
        """
        Initializes ThreadA from the example.

        Parameters:
            a1printed - Semaphore to control the a1 print statement.
            b1printed - Semaphore to control the b1 print statement.
        """
        self._a1printed = a1printed
        self._b1printed = b1printed

    def run(self):
        """
        Prints 'statement a1' followed by 'statement a2'.

        Waits until 'statement b1' is printed before
        printing 'statement a2'.
        """
        print 'statement a1'
        self._a1printed.release()  # V
        self._b1printed.acquire()  # P
        print 'statement a2'


class ThreadB(object):
    """
    The second thread from the example.
    """

    def __init__(self, a1printed, b1printed):
        """
        Initializes ThreadB from the example.

        Parameters:
            a1printed - Semaphore to control the a1 print statement.
            b1printed - Semaphore to control the b1 print statement.
        """
        self._a1printed = a1printed
        self._b1printed = b1printed

    def run(self):
        """
        Prints 'statement b1' followed by 'statement b2'.

        Waits until 'statement a1' is printed before
        printing 'statement b2'.
        """
        print 'statement b1'
        self._b1printed.release()  # V
        self._a1printed.acquire()  # P
        print 'statement b2'


def main():
    """
    Executes the rendezvou problem.
    """
    a1printed = Semaphore(0)
    b1printed = Semaphore(0)
    Thread(target=ThreadA(a1printed, b1printed).run).start()
    Thread(target=ThreadB(a1printed, b1printed).run).start()
    return 0


if __name__ == '__main__':
    sys.exit(main())
