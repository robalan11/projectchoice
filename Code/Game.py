import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
import Player


class World():
    def __init__(self):
        base.cTrav=CollisionTraverser()
        self.player = Player() #Add the dummy model
        #Execute level construction code
        #Create dummy targets with a collision hull attached to them. No collision handler.
w = World()
run()