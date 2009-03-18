import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.fsm import FSM
import Weapon
import math

    #5th collision bit is AI vision
def calculateHpr(v):
    temp=Vec3(0,0,0)
    if v.length()!=0:
        temp.setX(-math.atan2(v.getX(), v.getY()))
        temp.setY(math.asin(v.getZ()/v.length()))
    temp= temp*180/math.pi
    return temp
    
def AIsight(task_object): 
        #Results in a list with the first target being the active target, followed by a distance-sorted set of alternatives
        #Does not check for occlusion by other objects in the way. That's done in the tick function
        #Reset, keeping track of only the first target
        player=AI.playerhandle
        for index,NPC in AI.AI_dict.items():
            if NPC.targetlist: #If the list isn't empty
                NPC.targetlist=NPC.targetlist[0]
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
                    fromAI.look_angles = calculateHpr(player.model.getPos()-fromAI.model.getPos())
                else:
                    continue
            else:
                fromAI=AI.AI_dict[int(name[1])]
                #print entry.getIntoNodePath().getParent().getPos()-Looker.getParent().getPos()
                fromAI.look_angles = calculateHpr(entry.getIntoNodePath().getParent().getPos()-Looker.getParent().getPos())
            #print fromAI.look_angles
            if (abs(fromAI.look_angles.getX()-fromAI.model.getH())< 60 and abs(fromAI.look_angles.getY()-fromAI.model.getP())<60): #if in front of me
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
                        if not (player in fromAI.targetlist) and player.loyalty[fromAI.team]<45:
                            fromAI.targetlist.append(player)
                            fromAI.targetpos = player.model.getPos()
                else:
                    #print entry.getIntoNodePath().getName()
                    Lookedname=entry.getIntoNodePath().getName()
                    if Lookedname.split(";")[0]=="AIspher": #Sometimes this hiccups
                        Lookedname=Lookedname.split(";")[-1]
                        #print Lookedname[0]
                        #print Lookedname[1]
                        intoAI=AI.AI_dict[int(Lookedname)]
                        if not (intoAI in fromAI.targetlist) and intoAI.team!=fromAI.team and fromAI!=intoAI:
                            fromAI.targetlist.append(AI)
        return Task.cont

class AI():
    
    AI_dict={}
    sight=CollisionHandlerQueue()
    ID=0
    playerhandle=0
    turnspeed=10
    runspeed=2
    followradius=10
    
    def __init__(self, model,incell,team, startpos):
        #~ initialize the actor and FSM
        self.model=Actor(model)
        self.model.reparentTo(render)
        self.model.setPos(startpos)
        self.manifest=AI_manifest(self.model)
        
        #~Add to AI_list
        
        AI.AI_dict[AI.ID] = self
        
        #~ Initialize collision ~#
        
        #World collision
        #Bit channels are only walls and floors!
    
        self.cs=CollisionSphere(0,0,-1.25,1.25)
        self.cspath=self.model.attachNewNode(CollisionNode('AIspher;' +  str(AI.ID)))
        self.cspath.node().addSolid(self.cs)
        self.cspath.node().setFromCollideMask(BitMask32(0x01))
        self.cspath.setCollideMask(BitMask32(0x11))
        
        self.cr=CollisionRay(0,0,0,0,0,-1)
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
        self.mhandle_floor.setOffset(2)
        
        base.cTrav.addCollider(self.cspath, self.mhandle_wall)
        base.cTrav.addCollider(self.crpath, self.mhandle_floor)
        
        #Firing collision (Passive/Into object only, bullets are active)
        #Bit channel is only bullets
        self.ct=CollisionTube(0,0,1,0,0,-1,0.5)
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
        self.AIs=CollisionSphere(0,0,-1.25,20)
        self.AIspath=self.model.attachNewNode(CollisionNode('AIsight;' +  str(AI.ID)))
        self.AIspath.node().addSolid(self.AIs)
        self.AIspath.node().setFromCollideMask(BitMask32(0x10))
        self.AIspath.setCollideMask(BitMask32(0x00))
        base.cTrav.addCollider(self.AIspath, AI.sight)
        
        self.weapon = Weapon.Pistol()
        
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
        self.follow=True
        self.collisionoverride=False
        
        #Tasks
        taskMgr.add(self.tick, "AI tick;"+str(AI.ID))
        AI.ID += 1
        
    def nodepath(self):
        return self.model
    
    def tick(self,task_object):
        #Brain choices stuff
        self.dx=0
        self.dy=0
        self.dz=0
        self.dh=0
        self.seetarget=False
        #Check for uninterruptable states
        #Select the first target that isn't hidden by something else
        for target in self.targetlist:
            if target==AI.playerhandle and self.seeplayer == True:
                self.seetarget=True
                self.targetpos=target.model.getPos()
                break
            self.look_angles = Vec3(target.model.getPos())-Vec3(self.model.getPos())
            self.look_angles = calculateHpr(self.look_angles)
            self.frpath.setHpr(self.look_angles-self.model.getHpr())
            self.ftrav.traverse(render)
            self.fire.sortEntries()
            self.frpath.setHpr(Point3(0,0,0))
            if self.fire.getEntry(0).getIntoNodePath().getName()==target.target.cspath.getName():
                    #Vision is not occluded, use this target
                    self.seetarget=True
                    self.targetpos = target.model.getPos()
                    break
        if self.seetarget==False:
            if self.seeplayer and self.follow:
                self.targetpos=AI.playerhandle.model.getPos()
                self.look_angles = self.targetpos-Vec3(self.model.getPos())
                self.look_angles = calculateHpr(self.look_angles)
                #If following player, turn to player
                self.dh=min(AI.turnspeed, max(self.look_angles.getX()-self.model.getH(), -AI.turnspeed))
                #print self.look_angles.getX()-self.model.getH()
                #print self.dh
                if abs(self.dh)<0.01:
                    distance = Vec3(self.targetpos)-Vec3(self.model.getPos())
                    distance.setZ(0)
                    #If facing player, run if you're >10 feet from them
                    if distance.length() >AI.followradius:
                        self.dy=min(AI.runspeed, distance.length())
            else:
            #Move to the target's last position                
                self.look_angles = self.targetpos-Vec3(self.model.getPos())
                self.look_angles = calculateHpr(self.look_angles)
                self.dh=min(AI.turnspeed, max(self.look_angles.getX()-self.model.getH(), -AI.turnspeed))
                if abs(self.dh)<0.01:
                    distance = Vec3(self.targetpos)-Vec3(self.model.getPos())
                    distance.setZ(0)
                    if distance.length()>0:
                        self.dy=min(AI.runspeed, distance.length())
            #If already there, idle
        else:
            if health<10: #Health is at 1/5th strength
                #Turn away from target
                self.dh=min(AI.turnspeed, max((self.look_angles[0]+180)%360-self.model.getH(), -AI.turnspeed))
                #If turned away from target, run
                if abs(self.dh)<20:
                    self.dy=AI.runspeed
            else:
                #Turn to face target
                self.targetpos=AI.playerhandle.model.getPos()
                self.dh=min(AI.turnspeed, max(self.look_angles(1)-self.model.getH(), -AI.turnspeed))
                #If facing target, fire at them
                if abs(self.dh)<0.01:
                    self.weapon.shoot(self)
        
        #FSM stuff
        #Movement
        angle = math.radians(self.model.getH())
        sa = math.sin(angle)
        ca = math.cos(angle)
        time_tick = globalClock.getDt()*6
        self.model.setX(self.model.getX()-ca*self.dx*time_tick-sa*self.dy*time_tick)
        self.model.setY(self.model.getY()+ca*self.dy*time_tick-sa*self.dx*time_tick)
        self.model.setH(self.model.getH()+self.dh*time_tick)
        return Task.cont
    
class AI_manifest(FSM.FSM):
    def init(self, model):
        self.model=model
    