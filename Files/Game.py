import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
import Player
import sys


class World():
    def __init__(self):
        base.cTrav=CollisionTraverser()
        self.player = Player() #Add the dummy model
        #Execute level construction code
        #Create dummy targets with a collision hull attached to them. No collision handler.
        
        #Set up input
        
        self.setKey("forward",0)
        self.setKey("backward",0)
        self.setKey("left",0)
        self.setKey("right",0)
        self.setKey("shoot",0)
        
        self.accept("escape", sys.exit)
        self.accept("a", self.setKey, ["left",1])
        self.accept("d", self.setKey, ["right",1])
        self.accept("w", self.setKey, ["forward",1])
        self.accept("s", self.setKey, ["backward",1])
        self.accept("a-up", self.setKey, ["left",0])
        self.accept("d-up", self.setKey, ["right",0])
        self.accept("w-up", self.setKey, ["forward",0])
        self.accept("s-up", self.setKey, ["backward",0])
        
        self.accept("mouse1", self.setKey, ["shoot", 1])
        self.accept("mouse1-up", self.setKey, ["shoot", 0]) 
        
        #Set up tasks to get the world running
        
        TaskMgr.add(self.player.tick, "player_tick")
        TaskMgr.add(self.player.get_input, "player_input", extraArgs=self.keyMap)
        
    def setKey(self, key, value):
        self.keyMap[key] = value

w = World()
run()