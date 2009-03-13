import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from math import *
import random

class Weapon(object):
    def __init__(self):
        #Aiming collision: floor, walls, doors, and player bullet channels
        self.ftrav=CollisionTraverser("pfiretrav")
        self.fr=CollisionRay(0,0,0,0,1,0)
        self.frpath=base.camera.attachNewNode(CollisionNode('pcray'))
        self.frpath.node().addSolid(self.fr)
        self.frpath.node().setFromCollideMask(BitMask32(0x07))
        self.frpath.setCollideMask(BitMask32(0x00))
        self.sight=CollisionHandlerQueue()
        self.ftrav.addCollider(self.frpath, self.sight)

class Knife(Weapon):
    def __init__(self):
        super(Knife, self).__init__()
        
        self.crosshair = "Art/HUD/knifecrosshair.png"
    
    def shoot(self, player):
        self.ftrav.traverse(render)
        self.sight.sortEntries()
        for i in range(self.sight.getNumEntries()):
            object=self.sight.getEntry(i)
            #~ if weapon hits an AI
            if (object.getIntoNodePath().getName()=="AItarget"):
                targ = object.getSurfacePoint(render)
                dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                if dist < 4:
                    object.getIntoNodePath().getParent().removeNode()#Current hack
                    break
            if (object.getIntoNodePath().getName()=="wall" or object.getIntoNodePath().getName()=="floor"):
                break
                #~ do damage and alert AI
                #~ broadcast_attack(AI_hit)

class Pistol(Weapon):
    def __init__(self):
        super(Pistol, self).__init__()
        
        self.crosshair = "Art/HUD/pistolcrosshair.png"
    
    def shoot(self, player):
        self.ftrav.traverse(render)
        self.sight.sortEntries()
        for i in range(self.sight.getNumEntries()):
            object=self.sight.getEntry(i)
            #~ if weapon hits an AI
            if (object.getIntoNodePath().getName()=="AItarget"):
                object.getIntoNodePath().getParent().removeNode()#Current hack
                break
            if (object.getIntoNodePath().getName()=="wall" or object.getIntoNodePath().getName()=="floor"):
                break
                #~ do damage and alert AI
                #~ broadcast_attack(AI_hit)

class Shotgun(Weapon):
    def __init__(self):
        super(Shotgun, self).__init__()
        
        self.frays = [None, None, None, None, None, None]
        
        self.crosshair = "Art/HUD/shotguncrosshair.png"
    
    def shoot(self, player):
        for i in xrange(6):
            self.frays[i] = CollisionRay(0,0,0,0,1,0)
            theta = random.randint(1,628318)/100000.0
            phi = 0.05 * random.randint(0,157079)/100000.0     # Tune the leading constant for spread
            newdir = Point3(cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi))
            perturb = Point3(0,0,1) - newdir
            self.frays[i].setDirection(self.frays[i].getDirection() + perturb)
            self.frpath.node().addSolid(self.frays[i])
        self.ftrav.traverse(render)
        self.sight.sortEntries()
        for i in range(self.sight.getNumEntries()):
            object=self.sight.getEntry(i)
            #~ if weapon hits an AI
            if (object.getIntoNodePath().getName()=="AItarget"):
                targ = object.getSurfacePoint(render)
                dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                object.getIntoNodePath().getParent().removeNode()#Current hack
                break
            if (object.getIntoNodePath().getName()=="wall" or object.getIntoNodePath().getName()=="floor"):
                break
                #~ do damage and alert AI
                #~ broadcast_attack(AI_hit)
            
        for i in xrange(6):
            self.frpath.node().removeSolid(0)