import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.task.Task import Task
from direct.task.Task import TaskManager
from Player import Player
import Level
import sys

class World(DirectObject):
    def __init__(self):
        base.cTrav=CollisionTraverser()
        self.player = Player("Art/Models/box.egg") #Add the dummy model
        #Execute level construction code
        #Create dummy targets with a collision hull attached to them. No collision handler.
        
        #Set up input
        
        self.keyMap={}
        
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
        
        taskMgr.add(self.player.tick, "player_tick")
        taskMgr.add(self.player.get_input, "player_input", extraArgs=[self.keyMap["forward"], self.keyMap["backward"], self.keyMap["left"], self.keyMap["right"], self.keyMap["shoot"]])
        
    def setKey(self, key, value):
        self.keyMap[key] = value

w = World()
run()