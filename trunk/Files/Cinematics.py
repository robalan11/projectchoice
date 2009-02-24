#import base libraries
import time
import sys

#import Panda libraries
import direct.directbase.DirectStart
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode

class Event(object):
    def __init__(self, time, type, duration, remainder):
        self.time = float(time)
        self.type = type
        self.duration = float(duration)
        
        if self.type == 'm':
            self.function = self.move
            self.target = int(remainder[0])
            self.points = []
            for point in remainder[1:]:
                nums = point.split(',')
                self.points.append((float(nums[0]), float(nums[1]), float(nums[2])))
        
        elif self.type == 't':
            self.function = self.turn
            self.target = int(remainder[0])
            self.rotation = float(remainder[1])
            #self.startrot = self.target.getH()
            self.startrot = 0
        
        elif self.type == 's':
            self.function = self.speak
            self.first = True
            self.target = int(remainder[0])
            self.file = remainder[1]
        
        elif self.type == 'q':
            self.function = self.quit
    
    def move(self, title):
        elapsed = time.clock()-self.time
        if elapsed < self.duration:
            point = self.bezier(self.points[:], elapsed/self.duration)
            #target.setPos(point)
            print point
            return Task.cont
        return Task.cont
    
    def turn(self, title):
        elapsed = time.clock()-self.time
        if elapsed < self.duration:
            rot = self.startrot + self.rotation * (elapsed/self.duration)
            #self.target.setH(rot)
            print rot
            return Task.cont
        return Task.done
    
    def speak(self, title):
        elapsed = time.clock()-self.time
        if self.first:
            text = open(self.file, 'r').readlines()
            #put text on the screen
            pos = 1
            self.textlines = []
            for line in text:
                pos -= 0.06
                self.textlines.append(OnscreenText(text=line, style=1, fg=(1,1,1,1), pos=(0, pos), align=TextNode.ACenter, scale = .06))
            self.first = False
        if elapsed < self.duration:
            return Task.cont
        for line in self.textlines:
            pass
            #line.clearText()
        return Task.done
    
    def quit(self, title):
        sys.exit(12345)
    
    def bezier(self, points, t):
        if len(points) == 1:
            return points[0]
        next_itr = []
        for i in xrange(len(points) - 1):
            pt_a = [points[i][0],   points[i][1],   points[i][2]]
            pt_b = [points[i+1][0], points[i+1][1], points[i+1][2]]
            next_itr.append((pt_a[0] + float(pt_b[0] - pt_a[0]) * t,
                             pt_a[1] + float(pt_b[1] - pt_a[1]) * t,
                             pt_a[2] + float(pt_b[2] - pt_a[2]) * t))
        return self.bezier(next_itr, t)

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
            self.events.append(Event(parts[0], parts[1], parts[2], parts[3:]))
    
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
