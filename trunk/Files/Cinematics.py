#import base libraries
import time
import sys

#import Panda libraries
import direct.directbase.DirectStart
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode
from pandac.PandaModules import VBase3

from Level import Level

class Event(object):
    def __init__(self, world, time, type, duration, target, remainder, starttime, cinematic):
        self.worldref = world
        self.time = float(time) + starttime
        self.type = type
        self.duration = float(duration)
        self.target = target
        self.cinematic = cinematic
        
        if self.type == 'm':
            self.function = self.move
            self.points = []
            for point in remainder:
                nums = point.split(',')
                self.points.append((float(nums[0]), float(nums[1]), float(nums[2])))
        
        elif self.type == 't':
            self.function = self.turn
            self.rotation = float(remainder[0])
            self.startrot = self.target.model.getH()
        
        elif self.type == 's':
            self.function = self.speak
            self.first = True
            self.target = target
            self.file = remainder[0]
            self.start = int(remainder[1])
            self.end = int(remainder[2])
            #self.font = loader.loadFont("Art/Fonts/Soviet2.ttf")
        
        elif self.type == 'c':
            self.function = self.camera
            self.rotation = float(remainder[0])
            self.pitch = float(remainder[1])
            self.first = True
            self.points = []
            for point in remainder[2:]:
                nums = point.split(',')
                self.points.append((float(nums[0]), float(nums[1]), float(nums[2])))
        
        elif self.type == 'n':
            self.function = self.nextlevel
            self.levelfile = remainder[0]
            self.entrance = remainder[1]
        
        elif self.type == 'g':
            self.function = self.give
            self.wepnum = int(remainder[0])
        
        elif self.type == 'q':
            self.target = target
            self.function = self.quit
    
    def move(self, title):
        elapsed = time.clock()-self.time
        if elapsed < self.duration:
            pos = self.bezier(self.points[:], elapsed/self.duration)
            self.target.model.x = pos[0]
            self.target.model.y = pos[1]
            self.target.model.z = pos[2]
            return Task.cont
        return Task.done
    
    def turn(self, title):
        elapsed = time.clock()-self.time
        if elapsed < self.duration:
            rot = self.startrot + self.rotation * (elapsed/self.duration)
            self.target.model.setH(self.startrot + rot)
            return Task.cont
        return Task.done
    
    def speak(self, title):
        if self.worldref.player.keyMap["shoot"] == 1:
            for line in self.textlines:
                line.hide()
            timediff = self.cinematic.events[self.cinematic.nextevent].time - time.clock()
            for event in self.cinematic.events:
                event.time -= timediff
            return Task.done
        elapsed = time.clock()-self.time
        if self.first:
            text = open(self.file, 'r').readlines()
            #put text on the screen
            pos = 1
            self.textlines = []
            for line in text[self.start:self.end]:
                pos -= 0.09
                self.textlines.append(OnscreenText(text=line, style=1, fg=(0.9,0.8,0.6,1), shadow=(0,0,0,0.7), pos=(0, pos), align=TextNode.ACenter, scale = .09))#, font = self.font))
            self.first = False
        if elapsed < self.duration:
            return Task.cont
        for line in self.textlines:
            line.hide()
        return Task.done
    
    def camera(self, title):
        if self.first:
            self.startrot = base.camera.getH()
            self.startpitch = base.camera.getP()
            self.first = False
        elapsed = time.clock()-self.time
        if elapsed < self.duration:
            pos = self.bezier(self.points[:], elapsed/self.duration)
            posv = VBase3(pos[0], pos[1], pos[2])
            base.camera.setPos(posv)
            rot = self.startrot + self.rotation * (elapsed/self.duration)
            base.camera.setH(rot)
            pit = self.startpitch + self.pitch * (elapsed/self.duration)
            base.camera.setP(pit)
            return Task.cont
        return Task.done
    
    def nextlevel(self, title):
        self.worldref.player.model.reparentTo(render)
        self.worldref.player.dx = 0
        self.worldref.player.dy = 0
        self.worldref.level.rootnode.removeNode()
        self.worldref.level = Level(self.levelfile, self.worldref.player, self.entrance)
        self.worldref.player.setLevel(self.worldref.level)

    def give(self, title):
        if self.wepnum == 10:
            self.worldref.player.armor = 100
        else:
            self.worldref.player.haveweapon[self.wepnum] = 1
    
    def quit(self, title):
        self.target.runningcinematic = False
        base.camera.reparentTo(self.target.model)
        base.camera.setH(0)
        base.camera.setPos(VBase3(0,0,5.0))
        self.worldref.player.arms.show()
        for ai in self.worldref.level.ais:
            ai.cinematic = False
    
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
    def __init__(self, cinefile, actors, world):
        self.worldref = world;
        self.start = time.clock()
        self.events = []
        self.actors = actors
        self.loadCinefile(cinefile)
        base.camera.setH(float(self.camstart[0]))
        base.camera.setP(float(self.camstart[1]))
        pos = self.camstart[2].split(',')
        base.camera.setPos(VBase3(float(pos[0]), float(pos[1]), float(pos[2])))
        self.nextevent = 0
        taskMgr.add(self.runCin, cinefile)

    def loadCinefile(self, cinefile):
        events = open(cinefile, 'r').readlines()
        self.camstart = events[0].split()
        for event in events[1:]:
            parts = event.split()
            self.events.append(Event(self.worldref, parts[0], parts[1], parts[2], self.actors[parts[3]], parts[4:], self.start, self))
    
    def runCin(self, title):
        currtime = time.clock()
        while self.events[self.nextevent].time <= currtime:
            taskMgr.add(self.events[self.nextevent].function, str(title) + str(self.events[self.nextevent]))
            self.nextevent += 1
            if self.nextevent >= len(self.events):
                return Task.done
        return Task.cont

if __name__ == "__main__":
    import Player
    player = Player.Player("Art/Models/box.egg")
    actors = {"player": player}
    Cinematic("Cinematics/test.cin")
    run()
