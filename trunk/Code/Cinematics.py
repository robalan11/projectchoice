import time

class Event(object):
    def __init__(time, type, remainder):
        self.time = time
        self.type = type

class Cinematic(object):
    def __init__(cinefile):
        self.events = []
        self.loadCinefile(cinefile)
        self.nextevent = 0
        self.start = time.clock()
        self.run()

    def loadCinefile(cinefile):
        events = open(cinefile, 'r').readlines()
        for event in events:
            parts = event.split()
            self.events.append(Event(parts[0], parts[1], parts[2:]))
    
    def run():
        elapsed = time.clock()-self.start
        while self.events[self.nextevent].time <= elapsed:
            self.events[self.nextevent].function()
            self.nextevent += 1
