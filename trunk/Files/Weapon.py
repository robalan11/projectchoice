import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from math import *
import AI
import random

class Weapon(object):
    def __init__(self, nodepath, isplayer, offset):
        #Aiming collision: floor, walls, doors, and player bullet channels
        self.ftrav=CollisionTraverser("pfiretrav")
        self.fr=CollisionRay(0,0,0,0,1,0)
        self.frpath=nodepath.attachNewNode(CollisionNode('pcray'))
        self.frpath.node().addSolid(self.fr)
        self.frpath.setPos(offset)
        if isplayer==True:
            self.frpath.node().setFromCollideMask(BitMask32(0x07))
        else:
            self.frpath.node().setFromCollideMask(BitMask32(0x0f))
        self.isplayer=isplayer
        self.frpath.setCollideMask(BitMask32(0x00))
        self.sight=CollisionHandlerQueue()
        self.ftrav.addCollider(self.frpath, self.sight)
    
    def reload(self):
        if self.reloadsound.status() != 2 and self.shots != self.maxshots: 
            if self.ammo > self.maxshots - self.shots:
                self.reloadsound.play()
                self.ammo -= self.maxshots - self.shots
                self.shots = self.maxshots
            elif self.ammo > 0:
                self.reloadsound.play()
                self.shots += self.ammo
                self.ammo = 0

class Knife(Weapon):
    def __init__(self, base, isplayer, offset):
        super(Knife, self).__init__(base, isplayer, offset)
        
        self.crosshair = "Art/HUD/knifecrosshair.png"
        self.firesound = loader.loadSfx("Sound/Effects/knifemiss.wav")
        self.hitsound = loader.loadSfx("Sound/Effects/knifehit.wav")
        self.wallsound = loader.loadSfx("Sound/Effects/knifewall.wav")
        self.shots=1
        self.maxshots=1
        self.ammo = 1
        self.type = "knife"
    
    def shoot(self, player):
        if self.firesound.status() != 2:
            self.ftrav.traverse(render)
            self.sight.sortEntries()
            self.firesound.play()
            for i in range(self.sight.getNumEntries()):
                object=self.sight.getEntry(i)
                #~ if weapon hits an AI
                if (object.getIntoNodePath().getName()=="AItarget"):
                    targ = object.getSurfacePoint(render)
                    dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                    if dist < 4:
                        self.hitsound.play()
                        object.getIntoNodePath().getParent().removeNode()#Current hack
                        break
                if (object.getIntoNodePath().getName()=="wall" or object.getIntoNodePath().getName()=="floor"):
                    targ = object.getSurfacePoint(render)
                    dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                    print dist
                    if dist < 4:
                        self.wallsound.play()
                    break
                if (object.getIntoNodePath().getName().split(";")[0]=="AItarget") and object.getIntoNodePath().getParent().node()!=player.model.node(): #Not shooting yourself
                    targ = object.getSurfacePoint(render)
                    dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                    if dist < 5 or not self.isplayer and dist<8:
                        self.hitsound.play()
                        ID=object.getIntoNodePath().getName().split(";")[1]
                        target=AI.AI.AI_dict[int(ID)]
                        target.damage(player, 20)
                        if player==AI.AI.playerhandle:
                            player.broadcast_attack(target)
                        break
                if (object.getIntoNodePath().getName()=="ptarget"):
                    targ = object.getSurfacePoint(render)
                    dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                    if dist < 5 or not self.isplayer and dist<8:
                        self.hitsound.play()
                        AI.AI.playerhandle.damage(player, 20)
                        break
    
    def reload(self):
        pass

class Pipe(Weapon):
    def __init__(self, base, isplayer, offset):
        super(Pipe, self).__init__(base, isplayer, offset)
        
        self.crosshair = "Art/HUD/knifecrosshair.png"
        self.firesound = loader.loadSfx("Sound/Effects/knifemiss.wav")
        self.hitsound = loader.loadSfx("Sound/Effects/knifehit.wav")
        self.wallsound = loader.loadSfx("Sound/Effects/knifewall.wav")
        self.shots=1
        self.maxshots=1
        self.ammo = 1
        self.type = "pipe"
    
    def shoot(self, player):
        if self.firesound.status() != 2:
            self.ftrav.traverse(render)
            self.sight.sortEntries()
            self.firesound.play()
            for i in range(self.sight.getNumEntries()):
                object=self.sight.getEntry(i)
                #~ if weapon hits an AI
                if (object.getIntoNodePath().getName()=="AItarget"):
                    targ = object.getSurfacePoint(render)
                    dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                    if dist < 4:
                        self.hitsound.play()
                        object.getIntoNodePath().getParent().removeNode()#Current hack
                        break
                if (object.getIntoNodePath().getName()=="wall" or object.getIntoNodePath().getName()=="floor"):
                    targ = object.getSurfacePoint(render)
                    dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                    print dist
                    if dist < 4:
                        self.wallsound.play()
                    break
                if (object.getIntoNodePath().getName().split(";")[0]=="AItarget") and object.getIntoNodePath().getParent().node()!=player.model.node(): #Not shooting yourself
                    targ = object.getSurfacePoint(render)
                    dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                    if dist < 4 or not self.isplayer and dist<8:
                        self.hitsound.play()
                        ID=object.getIntoNodePath().getName().split(";")[1]
                        target=AI.AI.AI_dict[int(ID)]
                        target.damage(player, 20)
                        if player==AI.AI.playerhandle:
                            player.broadcast_attack(target)
                        break
                if (object.getIntoNodePath().getName()=="ptarget"):
                    targ = object.getSurfacePoint(render)
                    dist = sqrt(pow(player.model.getX()-targ[0],2) + pow(player.model.getY()-targ[1],2) + pow(player.model.getZ()-targ[2],2))
                    if dist < 4 or not self.isplayer and dist<8:
                        self.hitsound.play()
                        AI.AI.playerhandle.damage(player, 20)
                        break
    
    def reload(self):
        pass


class Pistol(Weapon):
    def __init__(self, base, isplayer, offset):
        super(Pistol, self).__init__(base, isplayer, offset)
        
        self.crosshair = "Art/HUD/pistolcrosshair.png"
        self.firesound = loader.loadSfx("Sound/Effects/pistol.wav")
        self.reloadsound = loader.loadSfx("Sound/Effects/pistolreload.wav")
        self.emptysound = loader.loadSfx("Sound/Effects/empty.wav")
        self.shots = 12
        self.maxshots = 12
        self.ammo = 48
        self.maxammo = 120
        self.type = "pistol"
    
    def shoot(self, player):
        if self.reloadsound.status() != 2 and self.firesound.status() != 2:
            if self.shots > 0:
                self.ftrav.traverse(render)
                self.sight.sortEntries()
                self.firesound.play()
                self.shots -= 1
                for i in range(self.sight.getNumEntries()):
                    object=self.sight.getEntry(i)
                    #~ if weapon hits an AI
                    if (object.getIntoNodePath().getName()=="AItarget"):
                        object.getIntoNodePath().getParent().removeNode()#Current hack
                        break
                    if (object.getIntoNodePath().getName()=="wall" or object.getIntoNodePath().getName()=="floor"):
                        break
                    if (object.getIntoNodePath().getName().split(";")[0]=="AItarget") and object.getIntoNodePath().getParent().node()!=player.model.node(): #Not shooting yourself
                        ID=object.getIntoNodePath().getName().split(";")[1]
                        target=AI.AI.AI_dict[int(ID)]
                        target.damage(player, 15)
                        if player==AI.AI.playerhandle:
                            player.broadcast_attack(target)
                        break
                    if (object.getIntoNodePath().getName()=="ptarget"):
                        AI.AI.playerhandle.damage(player, 15)
                        break
            else:
                if self.emptysound.status() != 2:
                    self.emptysound.play()

class Shotgun(Weapon):
    def __init__(self, base, isplayer, offset):
        super(Shotgun, self).__init__(base, isplayer, offset)
        
        self.frays = [None]*20
        
        self.crosshair = "Art/HUD/shotguncrosshair.png"
        self.firesound = loader.loadSfx("Sound/Effects/shotgun.wav")
        self.reloadsound = loader.loadSfx("Sound/Effects/shotgunreload.wav")
        self.emptysound = loader.loadSfx("Sound/Effects/empty.wav")
        self.shots = 6
        self.maxshots = 6
        self.ammo = 24
        self.maxammo = 60
        self.type = "shotgun"
    
    def shoot(self, player):
        if self.reloadsound.status() != 2 and self.firesound.status() != 2:
            if self.shots > 0:
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
                self.firesound.play()
                self.shots -= 1
                hit_targets=[]
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
                    if (object.getIntoNodePath().getName().split(";")[0]=="AItarget") and object.getIntoNodePath().getParent().node()!=player.model.node() and hit_targets.count(object.getIntoNodePath().getName())==0: #Not shooting yourself or the same person twise
                        hit_targets.append(object.getIntoNodePath().getName())
                        ID=object.getIntoNodePath().getName().split(";")[1]
                        target=AI.AI.AI_dict[int(ID)]
                        distance = player.model.getPos()-target.model.getPos()
                        target.damage(player, int(100/distance.length())+1)
                        if player==AI.AI.playerhandle:
                            player.broadcast_attack(target)
                        continue
                    if (object.getIntoNodePath().getName()=="ptarget"):
                        distance = player.model.getPos()-AI.AI.playerhandle.model.getPos()
                        AI.AI.playerhandle.damage(player, int(100/distance.length()+1))
                        continue
                    
                for i in xrange(6):
                    self.frpath.node().removeSolid(0)
            else:
                if self.emptysound.status() != 2:
                    self.emptysound.play()

class Rifle(Weapon):
    def __init__(self, base, isplayer, offset):
        super(Rifle, self).__init__(base, isplayer, offset)
        
        self.crosshair = "Art/HUD/pistolcrosshair.png"
        self.firesound = loader.loadSfx("Sound/Effects/rifle.wav")
        self.reloadsound = loader.loadSfx("Sound/Effects/pistolreload.wav")
        self.emptysound = loader.loadSfx("Sound/Effects/empty.wav")
        self.shots = 50
        self.maxshots = 50
        self.ammo = 100
        self.maxammo = 300
        self.type = "rifle"
    
    def shoot(self, player):
        if self.reloadsound.status() != 2 and self.firesound.status() != 2:
            if self.shots > 0:
                self.ftrav.traverse(render)
                self.sight.sortEntries()
                self.firesound.play()
                self.shots -= 1
                for i in range(self.sight.getNumEntries()):
                    object=self.sight.getEntry(i)
                    #~ if weapon hits an AI
                    if (object.getIntoNodePath().getName()=="AItarget"):
                        object.getIntoNodePath().getParent().removeNode()#Current hack
                        break
                    if (object.getIntoNodePath().getName()=="wall" or object.getIntoNodePath().getName()=="floor"):
                        break
                    if (object.getIntoNodePath().getName().split(";")[0]=="AItarget") and object.getIntoNodePath().getParent().node()!=player.model.node(): #Not shooting yourself
                        ID=object.getIntoNodePath().getName().split(";")[1]
                        target=AI.AI.AI_dict[int(ID)]
                        target.damage(player, 10)
                        if player==AI.AI.playerhandle:
                            player.broadcast_attack(target)
                        break
                    if (object.getIntoNodePath().getName()=="ptarget"):
                        AI.AI.playerhandle.damage(player, 10)
                        break
            else:
                if self.emptysound.status() != 2:
                    self.emptysound.play()
