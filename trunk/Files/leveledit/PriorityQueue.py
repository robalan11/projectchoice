import pygame

class PriorityQueue():
    def __init__(self):
        self.queue=[]
    def put(self, item):
        data, priority = item
        self._insort_right((priority, data))
        
    def get(self):
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)[1]
    def empty(self):
        while(len(self.queue)>0):
            self.queue.pop()

    def _insort_right(self, x):
        """Insert item x in list, and keep it sorted assuming a is sorted.
        
        If x is already in list, insert it to the right of the rightmost x.       
        """
        lo = 0        
        hi = len(self.queue)
        
        while lo < hi:
            mid = (lo+hi)/2
            if x[0] < self.queue[mid][0]: hi = mid
            else: lo = mid+1
        self.queue.insert(lo, x)