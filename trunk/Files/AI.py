import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.fsm import FSM
import math

    #5th collision bit is AI vision
    
def AIsight(task_object): 
        #Results in a list with the first target being the active target, followed by a distance-sorted set of alternatives
        #Does not check for occlusion by other objects in the way. That's done in the tick function
        #Reset, keeping track of only the first target
        for index,NPC in AI.AI_dict.items():
            if NPC.targetlist: #If the list isn't empty
                NPC.targetlist=NPC.targetlist[0]
            NPC.seeplayer=False
        AI.sight.sortEntries()
        for i in range(AI.sight.getNumEntries()):
            entry=AI.sight.getEntry(i)
            name=entry.getFromNodePath().getName().split(";")
            Looker=entry.getFromNodePath()
            look_angles = Vec3(entry.getIntoNodePath().getPos()) - Vec3(Looker.getPos())
            look_angles = look_angles.getStandardizedHpr()
            fromAI=AI.AI_dict[int(name[1])]
            if (abs(look_angles[1])< 60 and abs(look_angles[2])<60): #if in front of me
                if (entry.getIntoNodePath().getName()=="pspher"):
                    pass
                    #~ player.add_AI(AI_dict[name[1]])
                    #~ #Make sure vision isn't through walls
                    #~ #Redirect ray so that it's the right direction
                    #~ self.frpath.setHpr(look_angles-self.model.getHpr())
                    #~ self.ftrav.traverse(render)
                    #~ self.fire.sortEntries()
                    #~ self.frpath.setHpr(Point3(0,0,0))
                    #~ if self.fire.getEntry(0).getIntoNodePath().getName()=="pspher":
                        #~ #You can still see your primary target
                        #~ fromAI.seeplayer=True
                    #~ if not (player in fromAI.targetlist) and player.loyalty[fromAI.team]<45:
                        #~ fromAI.targetlist.append(player)
                        #~ fromAI.targetpos = player.model.getPos()
                else:
                    #print entry.getIntoNodePath().getName()
                    Lookedname=entry.getIntoNodePath().getName()
                    if Lookedname.split(";")[0]=="AIspher": #Sometimes this hiccups
                        Lookedname=Lookedname.split(";")[-1]
                        #print Lookedname[0]
                        #print Lookedname[1]
                        intoAI=AI.AI_dict[int(Lookedname)]
                        if not (intoAI in fromAI.targetlist) and intoAI.team!=fromAI.team:
                            fromAI.targetlist.append(AI)
        return Task.cont

class AI():
    
    AI_dict={}
    sight=CollisionHandlerQueue()
    ID=0
    
    def __init__(self, model,incell,team):
        #~ initialize the actor and FSM
        self.model=Actor(model)
        self.model.reparentTo(render)
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
        self.cspath.setCollideMask(BitMask32(0x16))
        
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
        self.fr=CollisionRay(0,0,1,0,1,1)
        self.frpath=self.model.attachNewNode(CollisionNode('AIcray;' +  str(AI.ID)))
        self.frpath.node().addSolid(self.fr)
        self.frpath.node().setFromCollideMask(BitMask32(0x15))
        self.frpath.setCollideMask(BitMask32(0x00))
        self.fire=CollisionHandlerQueue()
        self.ftrav.addCollider(self.frpath, self.fire)
        
        #Sight collision
        self.AIs=CollisionSphere(0,0,-1.25,20)
        self.AIspath=self.model.attachNewNode(CollisionNode('AIsight;' +  str(AI.ID)))
        self.AIspath.node().addSolid(self.AIs)
        self.AIspath.node().setFromCollideMask(BitMask32(0x016))
        self.AIspath.setCollideMask(BitMask32(0x00))
        base.cTrav.addCollider(self.AIspath, AI.sight)
        
        AI.ID += 1
        
        #~ self.weapon = whatever the starting weapon is
        
        #Variables
        self.dx=0
        self.dy=0
        self.dz=0
        self.dh=0
        self.health=50
        self.incell=incell
        self.targetlist=[]
        self.targetpos=(0,0,0)
        self.team=team   
        self.seeplayer=False
        
    def nodepath(self):
        return self.model
    
    def tick(self):
        #Brain choices stuff
        
        #Select the first target that isn't hidden by something else
        for target in self.targetlist:
            if target==player and AI.seeplayer == True:
                self.seetarget=True
                self.targetpos=target.model.getPos()
                break
            look_angles = Vec3(target.model.getPos())-Vec3(self.model.getPos())
            look_angles = look_angles.getStandardizedHpr()
            self.frpath.setHpr(look_angles-self.model.getHpr())
            self.ftrav.traverse(render)
            self.fire.sortEntries()
            self.frpath.setHpr(Point3(0,0,0))
            if self.fire.getEntry(0).getIntoNodePath().getName()==target.target.cspath.getName():
                    #Vision is not occluded
                    self.seetarget=True
                    self.targetpos = target.model.getPos()
                    break
        if self.seetarget==False:
            pass
            #If following player, turn to player
            #If facing player, run if you're >10 feet from them
            #Move to the target's last position
            #If already there, idle
        else:
            if health<10: #Health is at 1/5th strength
                pass
                #Turn away from target
                #If turned away from target, run
            pass    
            #Turn to face target
            #If facing target, fire at them
        
        #FSM stuff
        #Movement
        angle = math.radians(self.model.getH())
        sa = math.sin(angle)
        ca = math.cos(angle)
        time_tick = globalClock.getDt()*6
        self.model.setX(self.model.getX()-ca*self.dx*time_tick-sa*self.dy*time_tick)
        self.model.setY(self.model.getY()+ca*self.dy*time_tick-sa*self.dx*time_tick)
        self.model.setH(self.model.getH()+self.dh*time_tick)
    
class AI_manifest(FSM.FSM):
    def init(self, model):
        self.model=model
    