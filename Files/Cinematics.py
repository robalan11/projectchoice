#import base libraries
import time
import sys

#import Panda libraries
import direct.directbase.DirectStart
from direct.task import Task

class Event(object):
    def __init__(self, time, type, remainder):
        self.time = float(time)
        self.type = type
        self.duration = float(remainder[0])
        if self.type == 'm':
            self.function = self.waiter
        elif self.type == 'q':
            self.function = self.quit
    
    def waiter(self, title):
        elapsed = time.clock()-self.time
        if elapsed < self.duration:
            print title, elapsed
            return Task.cont
        return Task.done
    
    def quit(self, title):
        sys.exit(12345)

class Cinematic(object):
    def __init__(self, cinefile):
        self.events = []
        self.loadCinefile(cinefile)
        self.nextevent = 0
        self.start = time.clock()
        taskMgr.add(self.runCin, 'cinematic')

    def loadCinefile(self, cinefile):
        events = open(cinefile, 'r').readlines()
        for event in events:
            parts = event.split()
            self.events.append(Event(parts[0], parts[1], parts[2:]))
    
    def runCin(self, title):
        elapsed = time.clock()-self.start
        while self.events[self.nextevent].time <= elapsed:
            taskMgr.add(self.events[self.nextevent].function, str(self.events[self.nextevent]))
            self.nextevent += 1
            if self.nextevent >= len(self.events):
                return Task.done
        return Task.cont

Cinematic("Cinematics/test.cin")
run()
