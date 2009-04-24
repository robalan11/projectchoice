import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenImage import OnscreenImage
from AI import AI
from AI import calculateHpr
import math
import Weapon
import Cinematics
from Level import Level

#This assumes that base.cTrav has been defined

# bit 0 is walls, bit 1 is floor, bit 3 is player bullets, bit 4 is AI bullets, bit 5 is AI vision, bit 6 is powerups and mission objectives

class Player ():
    def __init__(self, arm_model, world):
        self.worldref = world
        
        #~ initialize actor with the arm model
        self.keyMap = {}
        self.model=Actor(arm_model)
        self.model.reparentTo(render)
        
        #~ Initialize collision ~#
        
        #World collision
        #Bit channels are only walls and floors!
        base.camera.reparentTo(self.model)
        base.camera.setPos(0,0,4.0)
        base.camera.setHpr(0,0,0)
        base.camLens.setFov(60)
        base.disableMouse()
        
        if base.mouseWatcherNode.hasMouse():
            self.mouse_x = base.mouseWatcherNode.getMouseX()
            self.mouse_y = base.mouseWatcherNode.getMouseY()
        else:
            self.mouse_x = 0
            self.mouse_y = 0
    
        self.cs=CollisionSphere(0,0,0,1.25)
        self.cspath=self.model.attachNewNode(CollisionNode('pspher'))
        self.cspath.node().addSolid(self.cs)
        self.cspath.node().setFromCollideMask(BitMask32(0x01))
        self.cspath.setCollideMask(BitMask32.bit(0x11))
        #self.cspath.show()
        
        self.cr=CollisionRay(0,0,0,0,0,-1)
        self.crpath=self.model.attachNewNode(CollisionNode('pray'))
        self.crpath.node().addSolid(self.cr)
        self.crpath.node().setFromCollideMask(BitMask32(0x02))
        self.crpath.setCollideMask(BitMask32(0x00))
    
        self.mhandle_wall=CollisionHandlerPusher()
        self.mhandle_wall.addCollider(self.cspath, self.model)
        self.mhandle_floor=CollisionHandlerGravity()
        self.mhandle_floor.addCollider(self.crpath, self.model)
        self.mhandle_floor.setGravity(9.8)
        self.mhandle_floor.setMaxVelocity(2)
        self.mhandle_floor.setOffset(2)
        
        base.cTrav.addCollider(self.cspath, self.mhandle_wall)
        base.cTrav.addCollider(self.crpath, self.mhandle_floor)
        
        #Firing collision (Passive/Into object only, bullets are active)
        #Bit channel is only bullets
        self.ct=CollisionTube(0,0,4,0,0,-2,1)
        self.ctpath=self.model.attachNewNode(CollisionNode('ptarget'))
        self.ctpath.node().addSolid(self.ct)
        self.ctpath.node().setFromCollideMask(BitMask32(0x00))
        self.ctpath.setCollideMask(BitMask32(0x08))
        
        #Powerup pickup and mission objective handling and touching AI
        self.ps=CollisionSphere(0,0,0, 2.5)
        self.pspath=self.model.attachNewNode(CollisionNode('ppower'))
        self.pspath.node().addSolid(self.ps)
        self.pspath.node().setFromCollideMask(BitMask32(0x24))
        self.pspath.setCollideMask(BitMask32(0x00))
        self.phandle=CollisionHandlerQueue()
        base.cTrav.addCollider(self.pspath, self.phandle)
        
        #Set up weapons
        self.pistol = Weapon.Pistol(base.camera, True, Vec3(0,0,0))
        self.shotgun = Weapon.Shotgun(base.camera, True, Vec3(0,0,0))
        self.knife = Weapon.Knife(base.camera, True, Vec3(0,0,0))
        self.pipe = Weapon.Pipe(base.camera, True, Vec3(0,0,0))
        self.assaultrifle = Weapon.Rifle(base.camera, True, Vec3(0,0,0))
        self.weapon = self.knife
        self.crosshair=OnscreenImage(image = self.weapon.crosshair, pos = (0,0,0), scale =0.125)
        self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        
        #Set up weapon animations
        self.arms = Actor("Art/Models/arms-model") #, {"pistol":"Art/Models/fire_pistol"})
        self.arms.setScale(0.5)
        self.arms.reparentTo(self.model)
        self.arms.setPos(0,0,-1.8)
        
        self.AIs=CollisionSphere(0,0,-1.25,1.25)
        self.AIspath=self.model.attachNewNode(CollisionNode('pspher'))
        self.AIspath.node().addSolid(self.AIs)
        self.AIspath.node().setFromCollideMask(BitMask32(0x10))
        self.AIspath.setCollideMask(BitMask32(0x10))
        base.cTrav.addCollider(self.AIspath, AI.sight)        
        
        #~ self.weapon = whatever the starting weapon is
        #~ set up an empty list of enemies that see me
        self.enemies_watching=[]
        
        #Variables
        self.dx=0
        self.dy=0
        self.dz=0
        self.loud=0
        self.health=100
        self.armor=0
        self.use=False
        self.usecheck=True
        self.haveweapon=[1,1,0,0] #Knife, Pistol Shotgun Assault Rifle
        self.loyalty = [50, 50] # out of a minimum of 0 and a maximum of 100
        self.pobjective=[False, False]
        self.gobjective=[False, False]
        self.Respawning = False
        
        self.runningcinematic = False
        
        self.dead=False
        self.dying=False
        
    def nodepath(self):
        return self.model
    
    def setKey(self, key, value):
        self.keyMap[key] = value
    
    def setLevel(self, level):
        #~ It's a pointer to the level, nyah
        self.levelref = level
    
    def count(self, object):
        if object==self:
            return 1
        else:
            return 0
        
    def get_input (self, task_object):
        if self.runningcinematic:
            return Task.cont
        if self.dying or self.dead:
            return Task.cont
        #~ set player to running or stopped depending upon key input
        #Panda3D has built-in support for moving the camera?
        
        #print forward, backward, left, right
        
        
        self.mouse_oldx = self.mouse_x
        self.mouse_oldy = self.mouse_y
        
        #~ if base.mouseWatcherNode.hasMouse():
            #~ self.mouse_x = base.mouseWatcherNode.getMouseX()
            #~ self.mouse_y = base.mouseWatcherNode.getMouseY()
        
        #~ self.dH = self.mouse_x - self.mouse_oldx
        #~ self.dP = self.mouse_y - self.mouse_oldy
        
        #~ self.model.setHpr(self.model.getH()-self.dH*10, 0 , 0)
        #~ base.camera.setHpr(0, base.camera.getP()+self.dP*10, 0)
        
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2):
            self.model.setH(self.model.getH() -  (x - base.win.getXSize()/2)*0.1)
            base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2)*0.1)
            if base.camera.getP()>90:
                base.camera.setP(90)
            elif base.camera.getP()<-90:
                base.camera.setP(-90)
        
        if self.mhandle_floor.isOnGround(): #~ if not in the air
            self.dy = (self.keyMap["forward"]-self.keyMap["backward"])*0.75
            self.dx = (self.keyMap["left"]-self.keyMap["right"])*0.75
            
            #self.dz = key_mapping["jump"]
        #~ if player pressed use key
        #if (key_mapping["use"]==1):
            #~ open doors in front of player
            #~ if door is locked prisoner door and have key
                #~ release_prisoner
            #~ toggle follow flag of friendly AI in front of player
        #~ if animation playing is not the weapon firing/weapon is not reloading
            #~ if player pressed fire button
        if (self.keyMap["shoot"]==1):
            if self.weapon != self.assaultrifle:
                self.keyMap["shoot"]=0
            #self.arms.play(self.weapon.type)
            self.weapon.shoot(self)
        
        if (self.keyMap["reload"] == 1):
            self.weapon.reload()
            
        if (self.keyMap["use"]==1) and self.usecheck==True:
            self.use=True
            self.usecheck=False
        else:
            self.use=False
            if (self.keyMap["use"]==0):
                self.usecheck=True
        
        #~ if input requests changing the weapon and have that weapon, change to that weapon
        if (self.keyMap["knife"]==1 and self.weapon != self.knife and self.haveweapon[0]):
            self.weapon = self.knife
            self.crosshair.destroy()
            self.crosshair=OnscreenImage(image = self.knife.crosshair, pos = (0,0,0), scale =0.125)
            self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        if (self.keyMap["pistol"]==1 and self.weapon != self.pistol and self.haveweapon[1]):
            self.weapon = self.pistol
            self.crosshair.destroy()
            self.crosshair=OnscreenImage(image = self.pistol.crosshair, pos = (0,0,0), scale =0.05)
            self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        if (self.keyMap["shotgun"]==1 and self.weapon != self.shotgun and self.haveweapon[2]):
            self.weapon = self.shotgun
            self.crosshair.destroy()
            self.crosshair=OnscreenImage(image = self.shotgun.crosshair, pos = (0,0,0), scale =0.15)
            self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        if (self.keyMap["rifle"]==1 and self.weapon != self.assaultrifle and self.haveweapon[3]):
            self.weapon = self.assaultrifle
            self.crosshair.destroy()
            self.crosshair=OnscreenImage(image = self.assaultrifle.crosshair, pos = (0,0,0), scale =0.07)
            self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        
            
        return Task.cont
        
    def clear_sight(self):
        self.enemies_watching=[]
    
    def add_AI(self, AI):
        self.enemies_watching.append(AI)
        
    def damage(self, attacker, damage):
        #attacker is the attacking player/AI which is passed to the weapon
        if self.armor>0:
            if self.armor<damage:
                self.armor=0
                self.health-=damage-self.armor
            else:
                self.armor-=damage
        else:
            self.health -= damage
        if self.health<=0 and self.Respawning == False:
            self.health=0
            self.dying=True
            self.dead=True
            deathcam=LerpPosInterval(base.camera, 1, Vec3(0,0,0))
            restart=Func(self.restart)
            delay = Wait(2)
            interval=Sequence(deathcam, delay, restart)
            #interval.start()
            self.restart()
    
    def restart(self):
        print "Reload level"
        self.Respawning = True
        self.dx = 0
        self.dy = 0
        entrancetype = self.worldref.level.entrancetype
        filename=self.worldref.level.currentfilename
        self.worldref.level.rootnode.removeNode()
        self.worldref.level = Level(filename, self, entrancetype)
        self.worldref.player.setLevel(self.worldref.level)
        
        base.camera.setPos(0,0,4)
        self.dead=False
        self.dying=False
        self.health = 100
        self.Respawning = False
        
    
    def broadcast_attack(self, AI_hit):
        for enemy in self.enemies_watching:
            #~ if AI is not AI_hit
            if (enemy != AI_hit):
                #~ if AI_hit is ally
                if AI_hit.team==enemy.team:
                    #~ lower team loyalty
                    if (self.loyalty[enemy.team]>0):
                        self.loyalty[enemy.team]-=2
                    #~ enemy attacks player
                    enemy.forcedenemy=True
                else:
                    #~ raise team loyalty
                    if (self.loyalty[enemy.team]<100):
                        self.loyalty[enemy.team]+=2
            else:
                #~ AI_hit attacks player
                AI_hit.forcedenemy=True
    def tick(self,task_object):
        self.worldref.level.plnp.setPos(self.model.getPos().getX(), self.model.getPos().getY(), 5)
    
        if self.runningcinematic:
            return Task.cont
        if self.dying or self.dead:
            return Task.cont
        
        #~ check and set lights of current room to player
        #~ if under cinematic control
            #~ run cinema_tick(self) and nothing else
        if self.weapon != self.knife:
            self.loud=(self.weapon.firesound.status()==2)*40
        else:
            self.loud=0
        angle = math.radians(self.model.getH())
        sa = math.sin(angle)
        ca = math.cos(angle)
        time_tick = globalClock.getDt()*6
        self.model.setX(self.model.getX()-ca*self.dx-sa*self.dy)
        self.model.setY(self.model.getY()+ca*self.dy-sa*self.dx)
        #print self.model.getH()
        #~ if (self.m_handlefloor.isOnGround()):
            #~ self.m_handlefloor.setVelocity(self.dz)
            
        #~ set camera to player's position (anchored to player, so done automatically)
        #~Check for collision with powerups and mission objectives
        for i in range(self.phandle.getNumEntries()):
            #Check the node's name against all powerup types and change accordingly
            name = self.phandle.getEntry(i).getIntoNodePath().getName()
            remove=True
            if name == "health":
                self.health = min(100, self.health+25)
            elif name == "armor":
                self.armor = 100
            elif name == "pistol":
                self.haveweapon[1] = 1
                self.pistol.ammo = min(self.pistol.maxammo, self.pistol.ammo+self.pistol.maxshots)
            elif name == "shotgun":
                self.haveweapon[2] = 1
                self.shotgun.ammo = min(self.shotgun.maxammo, self.shotgun.ammo+self.shotgun.maxshots)
            elif name == "assault":
                self.haveweapon[3] = 1
                self.assaultrifle.ammo = min(self.assaultrifle.maxammo, self.assaultrifle.ammo+self.assaultrifle.maxshots)
            elif name == "pammo":
                self.pistol.ammo = min(self.pistol.maxammo, self.pistol.ammo+12)
            elif name == "pammolarge":
                self.pistol.ammo = min(self.pistol.maxammo, self.pistol.ammo+36)
            elif name == "sammo":
                self.shotgun.ammo = min(self.shotgun.maxammo, self.shotgun.ammo+4)
            elif name == "sammo":
                self.shotgun.ammo = min(self.shotgun.maxammo, self.shotgun.ammo+10)
            elif name == "aammo":
                self.assaultrifle.ammo = min(self.assaultrifle.maxammo, self.assaultrifle.ammo+24)
            elif name == "aammolarge":
                self.assaultrifle.ammo = min(self.assaultrifle.maxammo, self.assaultrifle.ammo+60)
            elif name == "prisonerobjective1":
                self.pobjective[0]=True
            elif name == "prisonerobjective2":
                self.pobjective[1]=True
            elif name == "guardobjective1":
                self.gobjective[0]=True
            elif name == "guardobjective2":
                self.gobjective[2]=True
            elif name.split(";")[0] == "AItarget" and name!="AItarget":
                remove=False
                temp = AI.AI_dict[int(name.split(";")[-1])]
                v = temp.model.getPos() - self.model.getPos()
                Player_look = calculateHpr(v, self.model.getHpr())
                AI_look = calculateHpr(-v, temp.model.getHpr())
                if abs(AI_look[0]-temp.model.getH())>AI.FOV and temp.targetlist==[]: #turn to face what bumped me
                    temp.forceturn = True
                    temp.targetpos = self.model.getPos()
                elif self.use==True and abs(Player_look[0]-self.model.getH())<5 and self.loyalty[temp.team]>65: #facing and you want me to follow
                    temp.follow=not temp.follow
                    self.use=False
                    print temp.follow
            if remove==True:
                self.phandle.getEntry(i).getIntoNodePath().getParent().remove()
        
        gridpos = (-1*int((self.model.getY()-5)/10), int((self.model.getX()+5)/10))
        if gridpos[0] >= 0 and gridpos[1] >= 0 and self.levelref.cines[gridpos] != '.':
            cinenumber = self.levelref.cines[gridpos]
            
            if self.levelref.levelfilename == "LevelOne":
                if cinenumber == '1':
                    for ai in self.levelref.ais:
                        if ai.team == False and ai.dead:
                            return Task.cont
                if cinenumber == '2':
                    for ai in self.levelref.ais:
                        if ai.team == True and ai.dead:
                            return Task.cont
                if cinenumber == '3':
                    for ai in self.levelref.ais:
                        if ai.team == True and not ai.dead:
                            return Task.cont
                        if ai.team == False and ai.dead:
                            return Task.cont
                if cinenumber == '4':
                    for ai in self.levelref.ais:
                        if ai.team == False and not ai.dead:
                            return Task.cont
                        if ai.team == True and ai.dead:
                            return Task.cont
                if cinenumber == '5':
                    for ai in self.levelref.ais:
                        if ai.team == True and not ai.dead:
                            return Task.cont
            
            if self.levelref.levelfilename == "Level2":
                if cinenumber == '1':
                    if self.levelref.entrancetype == "G":
                        return Task.cont
                if cinenumber == '2':
                    if self.levelref.entrancetype == "P":
                        return Task.cont
                    for ai in self.levelref.ais:
                        if (self.levelref.ais.index(ai) == 2 or self.levelref.ais.index(ai) == 3) and ai.dead:
                            return Task.cont
                if cinenumber == '5':
                    for ai in self.levelref.ais:
                        if (self.levelref.ais.index(ai) == 5 or self.levelref.ais.index(ai) == 6) and ai.dead:
                            return Task.cont
                if cinenumber == '6':
                    for ai in self.levelref.ais:
                        if ai.team == False and not ai.dead:
                            return Task.cont
                if cinenumber == '7':
                    for ai in self.levelref.ais:
                        if ai.team == True and not ai.dead:
                            return Task.cont
                if cinenumber == '8':
                    for ai in self.levelref.ais:
                        if not ai.dead:
                            return Task.cont
            
            base.camera.reparentTo(render)
            actors = {"player": self}
            for ai in self.levelref.ais:
                index = "ai" + str(self.levelref.ais.index(ai))
                actors[index] = ai
            file = "Cinematics/" + self.levelref.levelfilename + "-" + self.levelref.cines[gridpos] + ".cin"
            Cinematics.Cinematic(file, actors, self.worldref)
            for key in self.levelref.cines.keys():
                if self.levelref.cines[key] == cinenumber:
                    self.levelref.cines[key] = '.'
            self.runningcinematic = True
            self.arms.hide()
        
        return Task.cont
    def collided(self):
        pass
        #~ if collided with weapon
            #~ pickup weapon and add weapon/ammo to inventory
        #~ if collided with health/powerup
            #~ change respective stats
        #~ else
            #~ return player to previous location
                #~ (could also configure collision parts as pusher)
    #~ add_to_list(AI)
        #~ Add AI to list of enemies that see me
    #~ remove_from_list(AI)
        #~ Remove AI from list of enemies that see me
    #~ release_prisoner
    #Unlock the prisoner's door
    #~ prisoner follows scripted procedure to get out
        #~ broadcast_attack(Dummy guard)
    def possess(self):
        pass
        #~ hand over control to the cinema code
    def relinquish(self):
        pass
        #~ return control to the player
