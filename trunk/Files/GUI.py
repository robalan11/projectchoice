from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode
from direct.task import Task

class GUI(DirectObject):
    def __init__(self, world):
        self.worldref = world
        self.font = loader.loadFont("Art/Fonts/Soviet2.ttf")
        self.hp = OnscreenText(text="100", style=1, fg=(0.9,0.6,0,1), shadow=(0,0,0,0.7), pos=(-1.0, -0.85), align=TextNode.ARight, scale = .2, mayChange = 1, font = self.font)
        self.hpnote = OnscreenText(text="Health", style=1, fg=(0.9,0.6,0,1), shadow=(0,0,0,0.7), pos=(-1.01, -0.95), align=TextNode.ARight, scale = .08, font = self.font)
        self.armor = OnscreenText(text="100", style=1, fg=(0.9,0.6,0,1), shadow=(0,0,0,0.7), pos=(-0.65, -0.85), align=TextNode.ARight, scale = .2, mayChange = 1, font = self.font)
        self.armornote = OnscreenText(text="Armor", style=1, fg=(0.9,0.6,0,1), shadow=(0,0,0,0.7), pos=(-0.68, -0.95), align=TextNode.ARight, scale = .08, font = self.font)
        self.ammo = OnscreenText(text="12/48", style = 1, fg=(0.9,0.6,0,1), shadow=(0,0,0,0.7), pos=(1.225, -0.85), align=TextNode.ARight, scale = .2, mayChange = 1, font = self.font)
        self.ammonote = OnscreenText(text="Ammo", style=1, fg=(0.9,0.6,0,1), shadow=(0,0,0,0.7), pos=(1.05, -0.95), align=TextNode.ARight, scale = .08, font = self.font)
        taskMgr.add(self.refresh, 'refreshgui')
    
    def refresh(self, title):
        self.hp['text'] = str(self.worldref.player.health)
        self.armor['text'] = str(self.worldref.player.armor)
        self.ammo['text'] = str(self.worldref.player.weapon.shots) + "/" + str(self.worldref.player.weapon.ammo)
        if self.worldref.player.weapon == self.worldref.player.knife:
            self.ammo.hide()
        else:
            self.ammo.show()
        return Task.cont