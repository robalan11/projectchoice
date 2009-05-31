from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", """fullscreen 1
win-size 1024 768""")
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.task.Task import Task
from direct.task.Task import TaskManager
from Player import Player
from Level import Level
from mainmenu import MainMenu
from AI import AI
from AI import AIsight
from GUI import GUI
from pandac.PandaModules import WindowProperties
from direct.gui.OnscreenImage import OnscreenImage
import sys

class World(DirectObject):
    def __init__(self):
        self.mainmenu = MainMenu(self)
    
    def initMainGame(self):
        self.mainmenu.__del__()
        base.cTrav=CollisionTraverser()
        self.player = Player("Art/Models/humanplayer-model.egg", self) #Add the dummy model
        self.player.model.setH(180)
        self.gui = GUI(self)
        #temp=AI(1, False, 0, Vec3(0,0,0), 0, 2) #Just to instantiate all AI global variables
        #temp2=AI(2, False, 1, Vec3(20,-40,0), 270, 1)
        AI.playerhandle=self.player
        
        #Execute level construction code
        

        self.level=Level("leveledit/LevelOne.txt",self.player,"G")
        self.player.setLevel(self.level)
        
        #Create dummy targets with a collision hull attached to them. No collision handler.
        
        #Set up input
        
        self.setKey("forward",0)
        self.setKey("backward",0)
        self.setKey("left",0)
        self.setKey("right",0)
        
        self.setKey("knife",0)
        self.setKey("pistol",0)
        self.setKey("shotgun",0)
        self.setKey("rifle",0)
        
        self.setKey("shoot",0)
        self.setKey("reload",0)
        self.setKey("use",0)
        self.setKey("run",0)
        
        
        self.accept("escape", sys.exit)
        self.accept("a", self.setKey, ["left",1])
        self.accept("d", self.setKey, ["right",1])
        self.accept("w", self.setKey, ["forward",1])
        self.accept("s", self.setKey, ["backward",1])
        self.accept("a-up", self.setKey, ["left",0])
        self.accept("d-up", self.setKey, ["right",0])
        self.accept("w-up", self.setKey, ["forward",0])
        self.accept("s-up", self.setKey, ["backward",0])
        
        self.accept("shift", self.setKey, ["run",1])
        self.accept("shift-up", self.setKey, ["run",0])
        
        self.accept("e", self.setKey, ["use",1])
        self.accept("e-up", self.setKey, ["use",0])
        
        self.accept("0", self.setKey, ["knife",1])
        self.accept("1", self.setKey, ["pistol",1])
        self.accept("2", self.setKey, ["shotgun",1])
        self.accept("3", self.setKey, ["rifle",1])
        self.accept("0-up", self.setKey, ["knife",0])
        self.accept("1-up", self.setKey, ["pistol",0])
        self.accept("2-up", self.setKey, ["shotgun",0])
        self.accept("3-up", self.setKey, ["rifle",0])
        
        self.accept("mouse1", self.setKey, ["shoot", 1])
        self.accept("mouse1-up", self.setKey, ["shoot", 0])
        self.accept("r", self.setKey, ["reload", 1])
        self.accept("r-up", self.setKey, ["reload", 0])
        
        #Set up tasks to get the world running
        
        taskMgr.add(self.player.tick, "player_tick")
        taskMgr.add(self.player.get_input, "player_input")
        taskMgr.add(AIsight, "AI sight check")
        
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setFullscreen(True)
        base.win.requestProperties(props)
        
        
    def setKey(self, key, value):
        self.player.setKey(key, value)

w = World()
run()
