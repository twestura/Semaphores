"""
Multiplex - Up to n threads can share a resource.
"""


from threading import Semaphore


class Multiplex(object):
    """
    A lock that allows up to n threads to access a critical section.
    """

    def __init__(self, n):
        """
        Initializes a new Multiplex that allows n threads.

        Parameters:
            n - The number of threads that can access a critical section.
        """
        self._multiplex_sem = Semaphore(n)

    def acquire(self):
        """
        Enter the multiplex and block until space is available.
        """
        self._multiplex_sem.acquire()

    def release(self):
        """
        Leave the multiplex.
        """
        self._multiplex_sem.release()

