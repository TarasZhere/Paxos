'''
    THREADING class modification
        This file defines a ThreadingReturn class that inherits the Thread class 
        and modifies the run and join methods to return on Join. I have been doing that because the join method does not return
        any value if the Threaded method has a return type.
        The solution has been taken from this stackoverflow post: https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread
'''

from threading import Thread

class ThreadReturn(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)    

    def join(self, *args):
        Thread.join(self, *args)
        return self._return