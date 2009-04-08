import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.fsm import FSM
import Weapon
import math

    #5th collision bit is AI vision
def calculateHpr(v, norm_angles):
    temp=Vec3(0,0,0)
    if v.length()!=0:
        temp.setX(-math.atan2(v.getX(), v.getY()))
        temp.setY(math.asin(v.getZ()/v.length()))
    temp= temp*180/math.pi
    if temp.getX()-norm_angles.getX()>180:
        temp.setX(temp.getX() - 360)
    if temp.getX()-norm_angles.getX()<-180:
        temp.setX(temp.getX()+360)
    if temp.getY()-norm_angles.getY()>180:
        temp.setY(temp.getY() - 360)
    if temp.getY()-norm_angles.getY()<-180:
        temp.setY(temp.getY() + 360)
    return temp
    
def AIsight(task_object): 
        #Results in a list with the first target being the active target, followed by a distance-sorted set of alternatives
        #Does not check for occlusion by other objects in the way. That's done in the tick function
        #Reset, keeping track of only the first target
        player=AI.playerhandle
        for index,NPC in AI.AI_dict.items():
            #if NPC.targetlist: #If the list isn't empty
                #NPC.targetlist=[NPC.targetlist[0]]
            NPC.seeplayer=False
        AI.sight.sortEntries()
        for i in range(AI.sight.getNumEntries()):
            entry=AI.sight.getEntry(i)
            name=entry.getFromNodePath().getName().split(";")
            Looker=entry.getFromNodePath()
            fromAI=0
            if name==["pspher"]:
                if "AIspher" in entry.getIntoNodePath().getName():
                    name = entry.getIntoNodePath().getName().split(";")
                    fromAI=AI.AI_dict[int(name[1])]
                    fromAI.look_angles = calculateHpr(player.model.getPos()-fromAI.model.getPos(), fromAI.model.getHpr())
                else:
                    continue
            else:
                fromAI=AI.AI_dict[int(name[1])]
                #print entry.getIntoNodePath().getParent().getPos()-Looker.getParent().getPos()
                fromAI.look_angles = calculateHpr(entry.getIntoNodePath().getParent().getPos()-Looker.getParent().getPos(), Looker.getParent().getHpr())
            if fromAI.forceturn:
                continue
            if (abs(fromAI.look_angles.getX()-fromAI.model.getH())< AI.FOV and abs(fromAI.look_angles.getY()-fromAI.model.getP())<AI.FOV): #if in front of me
                if (entry.getIntoNodePath().getName()=="pspher" or entry.getFromNodePath().getName()=="pshper"):
                    #print look_angles
                    #Make sure vision isn't through walls
                    #Redirect ray so that it's the right direction
                    fromAI.frpath.setHpr(fromAI.look_angles-fromAI.model.getHpr())
                    fromAI.cspath.setCollideMask(BitMask32(0x00))
                    fromAI.ctpath.setCollideMask(BitMask32(0x00))
                    fromAI.ftrav.traverse(render)
                    fromAI.fire.sortEntries()
                    fromAI.cspath.setCollideMask(BitMask32(0x11))
                    fromAI.ctpath.setCollideMask(BitMask32(0x08))
                    fromAI.frpath.setHpr(Vec3(0,0,0))
                    #print fromAI.fire.getEntry(0).getIntoNodePath().getParent()
                    #print player.model.getGeomNode()
                    if fromAI.fire.getNumEntries()>0 and fromAI.fire.getEntry(0).getIntoNodePath().getParent()==player.model.getGeomNode():
                        #View is not obfuscated
                        fromAI.seeplayer=True
                        player.add_AI(fromAI)
                        if fromAI.targetlist.count(player)==0 and (player.loyalty[fromAI.team]<45 or fromAI.forcedenemy==True):
                            fromAI.targetlist.append(player)
                            fromAI.targetpos = player.model.getPos()
                else:
                    #print entry.getIntoNodePath().getName()
                    Lookedname=entry.getIntoNodePath().getName()
                    if Lookedname.split(";")[0]=="AIspher": #Sometimes this hiccups
                        Lookedname=Lookedname.split(";")[-1]
                        intoAI=AI.AI_dict[int(Lookedname)]
                        if fromAI.targetlist.count(intoAI)==0 and intoAI.team!=fromAI.team and fromAI!=intoAI:
                            fromAI.targetlist.append(intoAI)
            elif fromAI.awareof==0: #Check for hearing if haven't already heard something
                temp = entry.getIntoNodePath().getParent().getPos()-entry.getFromNodePath().getParent().getPos()
                if (entry.getIntoNodePath().getName()=="pspher" or entry.getFromNodePath().getName()=="pshper"):
                    if temp.length() < player.loud:
                        fromAI.awareof=player
                else:
                    Lookedname=entry.getIntoNodePath().getName()
                    if Lookedname.split(";")[0]=="AIspher": #Sometimes this hiccups
                        Lookedname=Lookedname.split(";")[-1]
                        intoAI=AI.AI_dict[int(Lookedname)]
                        if temp.length()<intoAI.loud:
                            fromAI.awareof=intoAI
        return Task.cont

class AI():
    
    AI_dict={}
    sight=CollisionHandlerQueue()
    ID=0
    playerhandle=0
    turnspeed=50
    runspeed=2
    followradius=10
    FOV=87
    runanim=1.5
    turnanim=5
    walkanim=1
    scale=0.53
    
    def __init__(self, model, incell,team, startpos, starth, weapon):
        #Model = Number of model body type. Just use 0 for default body
        # incell = Are you in a cell (This may not be used)
        #Team = 0 for guards, 1 for prisoner
        # startpos = vector starting position in the world
        # starth = start heading
        # weapon = int indication weapon
        #~ initialize the actor and FSM
        #Load the appropriate team model and specified model type
        self.model=Actor("Art/Models/human1-model.egg")
        self.model.reparentTo(render)
        self.model.setPos(startpos)
        self.model.setH(starth)
        self.model.setScale(AI.scale,AI.scale,AI.scale)
        self.manifest=AI_manifest(self.model)
        
        #~Add to AI_list
        
        AI.AI_dict[AI.ID] = self
        
        #~ Initialize collision ~#
        
        #World collision
        #Bit channels are only walls and floors!
    
        self.cs=CollisionSphere(0,0,-1.25/AI.scale,1.25/AI.scale)
        self.cspath=self.model.attachNewNode(CollisionNode('AIspher;' +  str(AI.ID)))
        self.cspath.node().addSolid(self.cs)
        self.cspath.node().setFromCollideMask(BitMask32(0x01))
        self.cspath.setCollideMask(BitMask32(0x11))
        
        self.cr=CollisionRay(0,0,0.1/AI.scale,0,0,-1/AI.scale)
        self.crpath=self.model.attachNewNode(CollisionNode('AIray;' +  str(AI.ID)))
        self.crpath.node().addSolid(self.cr)
        self.crpath.node().setFromCollideMask(BitMask32(0x02))
        self.crpath.setCollideMask(BitMask32(0x00))
    
        self.mhandle_wall=CollisionHandlerPusher()
        self.mhandle_wall.addCollider(self.cspath, self.model)
        self.mhandle_floor=CollisionHandlerGravity()
        self.mhandle_floor.addCollider(self.crpath, self.model)
        self.mhandle_floor.setGravity(0.5)
        self.mhandle_floor.setMaxVelocity(2)
        self.mhandle_floor.setOffset(0.1/AI.scale)
        
        base.cTrav.addCollider(self.cspath, self.mhandle_wall)
        base.cTrav.addCollider(self.crpath, self.mhandle_floor)
        
        #Firing collision (Passive/Into object only, bullets are active)
        #Bit channel is only bullets
        self.ct=CollisionTube(0,0,1/AI.scale,0,0,-1/AI.scale,0.5/AI.scale)
        self.ctpath=self.model.attachNewNode(CollisionNode('AItarget;' +  str(AI.ID)))
        self.ctpath.node().addSolid(self.ct)
        self.ctpath.node().setFromCollideMask(BitMask32(0x00))
        self.ctpath.setCollideMask(BitMask32(0x08))
        
        #Aiming collision: floor, walls, doors, and Player, and AI bullet channels
        self.ftrav=CollisionTraverser("AIfiretrav")
        self.fr=CollisionRay(0,0,0,0,1,0)
        self.frpath=self.model.attachNewNode(CollisionNode('AIcray;' +  str(AI.ID)))
        self.frpath.node().addSolid(self.fr)
        self.frpath.node().setFromCollideMask(BitMask32(0x0f))
        self.frpath.setCollideMask(BitMask32(0x00))
        self.fire=CollisionHandlerQueue()
        self.ftrav.addCollider(self.frpath, self.fire)
        #self.frpath.show()
        
        #Sight collision
        self.AIs=CollisionSphere(0,0,-1.25,60)
        self.AIspath=self.model.attachNewNode(CollisionNode('AIsight;' +  str(AI.ID)))
        self.AIspath.node().addSolid(self.AIs)
        self.AIspath.node().setFromCollideMask(BitMask32(0x10))
        self.AIspath.setCollideMask(BitMask32(0x00))
        base.cTrav.addCollider(self.AIspath, AI.sight)
        #self.AIspath.show()
        
        #Set weapon, weapon model, and load animations based on weapon
        
        temp=self.model.exposeJoint(None, "modelRoot", "right_hand_manip")
        if (weapon == 1):
            self.drop = "Pistol"
            self.weapon = Weapon.Pistol(self.model)
            self.killzone=15
            self.model.loadAnims({"Crouch": "Art/animations/human1-crouchingpistol.egg"})
            self.model.loadAnims({"Run": "Art/animations/human1-runningpistol.egg"})
            self.model.loadAnims({"Walk": "Art/animations/human1-walkingpistol.egg"})
            #Load idling
            #Load firing
            w=loader.loadModel("Art/Models/pistol.egg")
            w.setScale(0.05,0.05,0.05)
            w.setPos(-0.1, 0.6, 0.2)
            w.setHpr(90,70,135)
            w.reparentTo(temp)
        elif (weapon ==2):
            self.drop = "Shotgun"
            self.weapon = Weapon.Shotgun(self.model)
            self.killzone=10
            self.model.loadAnims({"Crouch": "Art/animations/human1-crouchingbiggun.egg"})
            self.model.loadAnims({"Run": "Art/animations/human1-runningbiggun.egg"})
            self.model.loadAnims({"Walk": "Art/animations/human1-walkingbiggun.egg"})
            #Load idling
            #Load firing
            w=loader.loadModel("Art/Models/shotgun.egg")
            w.setScale(0.1, 0.1,0.1)
            w.setPos(-0.56, 0.23, 0.3)
            w.setHpr(175,90,10)
            w.reparentTo(temp)
        #elif (weapon ==3):
            #self.weapon = Weapon.Rifle(self.model)
            #self.model.loadAnims({"Crouch": "Art/animations/human1-crouchingbiggun.egg"})
            #self.model.loadAnims({"Run": "Art/animations/human1-runningbiggun.egg"})
            #self.model.loadAnims({"Walk": "Art/animations/human1-walkingbiggun.egg"})
            #Load idling
            #Load firing
            #w=loader.loadModel("Art/Models/shotgun.egg")
            #w.setScale(0.1,0.1,0.1)
            #w.reparentTo(temp)
        else:
            # Change later to different melee weaps for different AI
            self.drop = "Medkit"
            self.weapon = Weapon.Knife(self.model)
            self.killzone = 3
            self.model.loadAnims({"Crouch": "Art/animations/human1-crouching.egg"})
            self.model.loadAnims({"Run": "Art/animations/human1-running.egg"})
            self.model.loadAnims({"Walk": "Art/animations/human1-walking.egg"})
            #Load idling
            #Load firing
            #w=loader.loadModel("Art/Models/shotgun.egg")
            #w.setScale(0.1,0.1,0.1)
            #w.reparentTo(temp)
        #Variables
        self.dx=0
        self.dy=0
        self.dz=0
        self.dh=0
        self.health=50
        self.incell=incell
        self.targetlist=[]
        self.targetpos=startpos
        self.seetarget=False
        self.team=team   
        self.seeplayer=False
        self.follow=False
        self.collisionoverride=False
        self.forceturn=False
        self.shooting=False
        self.awareof=0
        self.forcedenemy=False
        self.loud=0
        self.ID = AI.ID
        
        #Tasks
        taskMgr.add(self.tick, "AI tick;"+str(AI.ID))
        AI.ID += 1
        
    def nodepath(self):
        return self.model
        
    def count(self, object):
        if object==self:
            return 1
        else:
            return 0
    
    def damage(self, attacker, damage):
        #attacker is the attacking player/AI which is passed to the weapon
        self.health -= damage
        self.look_angles = attacker.model.getPos()-self.model.getPos()
        self.look_angles = calculateHpr(self.look_angles, self.model.getHpr())
        if abs(self.look_angles.getX()-self.model.getH())>AI.FOV and self.targetlist.len()==0:
            self.forceturn = True
            self.target = attacker
            self.targetpos = attacker.model.getPos()
    
    def tick(self,task_object):
       
        self.dx=0
        self.dy=0
        self.dz=0
        self.dh=0
        self.seetarget=False
        self.shooting=False
        
        #------------------------
        #Brain choices stuff
        #------------------------
        
        #Check for uninterruptable states
        #if self.model.getAnimControl("Fire").isPlaying() and self.model.getCurrentFrame("Fire")<self.model.getNumFrames("Fire"):
            #return
        #if self.health<0:
            #if self.model.getAnimControl("Dying").isPlaying() and self.model.getCurrentFrame("Dying")<self.model.getNumFrames("Dying")":
                #Spawn your drop
                #AI.AI_dict.remove(self)
                #self.model.remove()
                #self.remove()
            #return
        if self.targetlist==[] and self.awareof!=0: #If see nothing and hear something, turn to it
            self.targetpos=self.awareof.model.getPos()
            self.forceturn=True #Trips the next statement
            self.awareof=0
        if self.forceturn==True:
            self.look_angles = self.targetpos-Vec3(self.model.getPos())
            self.look_angles = calculateHpr(self.look_angles, self.model.getHpr())
            self.dh=min(AI.turnspeed, max(self.look_angles.getX()-self.model.getH(), -AI.turnspeed))
            if abs(self.dh)<1:
                self.forceturn=False
                self.dh=0
                self.targetpos=self.model.getPos()
        else:
            #Select the first target that isn't hidden by something else
            for target in self.targetlist:
                if target==AI.playerhandle and self.seeplayer == True:
                    self.seetarget=True
                    self.targetpos=target.model.getPos()
                    self.look_angles = self.targetpos-Vec3(self.model.getPos())
                    self.look_angles = calculateHpr(self.look_angles, self.model.getHpr())
                    break
                self.look_angles = Vec3(target.model.getPos())-Vec3(self.model.getPos())
                self.look_angles = calculateHpr(self.look_angles, self.model.getHpr())
                self.frpath.setHpr(self.look_angles-self.model.getHpr())
                self.ftrav.traverse(render)
                self.fire.sortEntries()
                self.frpath.setHpr(Point3(0,0,0))
                if self.fire.getEntry(0).getIntoNodePath().getParent().getName()==target.model.getName():
                        #Vision is not occluded, use this target
                        self.seetarget=True
                        self.targetpos = target.model.getPos()
                        self.targetlist=[target]
                        break
            if self.seetarget==False:
                if self.seeplayer and self.follow:
                    self.targetpos=AI.playerhandle.model.getPos()
                    self.look_angles = self.targetpos-Vec3(self.model.getPos())
                    self.look_angles = calculateHpr(self.look_angles, self.model.getHpr())
                    #If following player, turn to player
                    self.dh=min(AI.turnspeed, max(self.look_angles.getX()-self.model.getH(), -AI.turnspeed))
                    if abs(self.dh)<1:
                        distance = Vec3(self.targetpos)-Vec3(self.model.getPos())
                        distance.setZ(0)
                        #If facing player, run if you're >10 feet from them
                        if distance.length() >AI.followradius:
                            self.dy=min(AI.runspeed, distance.length()-AI.followradius)
                else:
                    #Did your primary target move right behind you? Turn to face them first
                    #~ if self.targetlist.len()>0:
                        #~ temp=target[0].model.getPos()
                        #~ self.look_angles = temp -self.model.getPos()
                        #~ self.look_angles = calculateHpr(self.look_angles, self.model.getHpr())
                        #~ temp = self.targetpos - self.model.getPos()
                        #~ if abs(self.look_angles - self.getHpr())>AI.FOV and temp.length()<3:
                            #~ #Turn
                    #Move to the target's last position                
                    self.look_angles = self.targetpos-Vec3(self.model.getPos())
                    self.look_angles = calculateHpr(self.look_angles, self.model.getHpr())
                    self.dh=min(AI.turnspeed, max(self.look_angles.getX()-self.model.getH(), -AI.turnspeed))
                    if abs(self.dh)<1:
                        distance = Vec3(self.targetpos)-Vec3(self.model.getPos())
                        distance.setZ(0)
                        if distance.length()>0:
                            self.dy=min(AI.runspeed, distance.length())
                        else:
                            self.targetlist=[] #Lost your target
                #If already there, idle
            else:
                if self.health<10: #Health is at 1/5th strength
                    #Turn away from target
                    self.dh=min(AI.turnspeed, max((self.look_angles[0]+180)%360-self.model.getH(), -AI.turnspeed))
                    #If turned away from target, run
                    if abs(self.dh)<20:
                        self.dy=AI.runspeed
                else:
                    #Turn to face target
                    self.dh=min(AI.turnspeed, max(self.look_angles.getX()-self.model.getH(), -AI.turnspeed))
                    #If facing target, fire at them
                    if abs(self.dh)<5:
                        distance = Vec3(self.targetpos)-Vec3(self.model.getPos())
                        distance.setZ(0)
                        if distance.length()>self.killzone:
                            self.dy=min(AI.runspeed, distance.length())
                            if distance.length()<self.killzone*1.4:
                                self.shooting=True
                                self.weapon.shoot(self)
                                self.weapon.shots=self.weapon.maxshots
                        else:
                            self.weapon.shoot(self)
                            self.weapon.shots=self.weapon.maxshots # AI don't run out of ammo
                            self.shooting=True
        #------------------------
        #Animation Handling
        #------------------------
        
        #print self.ID
        #print self.dy
        #if self.shooting:
            #pass
            #if self.dy > 0
                #run shooting part on top half and moving part on bottom half
            #else:
                #self.model.play("Fire")
        if self.dy>AI.runanim:
            #print "Run"
            self.model.setPlayRate(self.dy/AI.runanim, "Run")
            if not self.model.getAnimControl("Run").isPlaying():
                self.model.loop("Run")
        elif self.dy>0:
            #print "Walk"
            self.model.setPlayRate(self.dy/AI.runanim, "Walk")
            if not self.model.getAnimControl("Walk").isPlaying():
                self.model.loop("Walk")
        else:
            #print "Still"
            self.model.stop()
        #elif not self.model.getAnimControl("Idle").isPlaying():
            #self.model.loop("Idle")
        #------------------------    
        #Movement
        #------------------------
        angle = math.radians(self.model.getH())
        sa = math.sin(angle)
        ca = math.cos(angle)
        time_tick = globalClock.getDt()*6
        self.model.setX(self.model.getX()-ca*self.dx*time_tick-sa*self.dy*time_tick)
        self.model.setY(self.model.getY()+ca*self.dy*time_tick-sa*self.dx*time_tick)
        #print "#"
        self.model.setH(self.model.getH()+self.dh*time_tick)
        self.model.setH((self.model.getH()+180)%360-180)
        self.loud=self.dy+(self.weapon.firesound.status()==2)*40
        return Task.cont
    
class AI_manifest(FSM.FSM):
    def init(self, model):
        self.model=model
    