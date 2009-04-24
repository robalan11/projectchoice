import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.fsm import FSM
import Weapon
import math
import time

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
        player.clear_sight()
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
                    if fromAI.dying:
                        continue
                    fromAI.look_angles = calculateHpr(player.model.getPos()-fromAI.model.getPos(), fromAI.model.getHpr())
                else:
                    continue
            else:
                fromAI=AI.AI_dict[int(name[1])]
                if fromAI.dying or entry.getIntoNodePath().getParent().isEmpty() or Looker.getParent().isEmpty():
                    continue
                #print entry.getIntoNodePath().getParent().getPos()-Looker.getParent().getPos()
                fromAI.look_angles = calculateHpr(entry.getIntoNodePath().getParent().getPos()-Looker.getParent().getPos(), Looker.getParent().getHpr())
            if fromAI.forceturn:
                continue
            if abs(fromAI.look_angles.getX()-fromAI.model.getH())< AI.FOV: # and abs(fromAI.look_angles.getY()-fromAI.model.getP())<AI.FOV): #if in front of me
                if (entry.getIntoNodePath().getName()=="pspher" or entry.getFromNodePath().getName()=="pshper"):
                    #print look_angles
                    #Make sure vision isn't through walls
                    #Redirect ray so that it's the right direction
                    #fromAI.frpath.setHpr(fromAI.look_angles-fromAI.model.getHpr())
                    #temp =player.cspath.getPos()+player.model.getPos()-fromAI.frpath.getPos()-fromAI.model.getPos()
                    fromAI.frpath.lookAt(player.cspath)
                    fromAI.cspath.setCollideMask(BitMask32(0x00))
                    fromAI.ctpath.setCollideMask(BitMask32(0x00))
                    fromAI.ftrav.traverse(fromAI.level.collisionStuff)
                    fromAI.fire.sortEntries()
                    fromAI.cspath.setCollideMask(BitMask32(0x11))
                    fromAI.ctpath.setCollideMask(BitMask32(0x04))
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
    runspeed=0.65
    followradius=10
    FOV=87
    runanim=1.5/2*0.65
    turnanim=5
    walkanim=1
    scale=1.06#0.53
    movetweak=2
    accuracy1=12
    accuracy2=0
    follow=[loader.loadSfx("Sound/Guard/guardfollow.wav"), loader.loadSfx("Sound/Prisoner/inmatefollow.wav")]
    stay=[loader.loadSfx("Sound/Guard/guardstay.wav"), loader.loadSfx("Sound/Prisoner/inmatestay.wav")]
    nofollow=[loader.loadSfx("Sound/Guard/guardnofollow.wav"), loader.loadSfx("Sound/Prisoner/inmatenofollow.wav")]
    huh=[loader.loadSfx("Sound/Guard/guardhuh.wav"), loader.loadSfx("Sound/Prisoner/inmateshuh.wav")]
    hit=loader.loadSfx("Sound/Effects/hit.wav")
    
    def __init__(self, model, incell,team, startpos, starth, weapon,rootnode, level):
        #Model = Number of model body type. Just use 0 for default body
        # incell = Are you in a cell (This may not be used)
        #Team = 0 for guards, 1 for prisoner
        # startpos = vector starting position in the world
        # starth = start heading
        # weapon = int indication weapon
        #~ initialize the actor and FSM
        #Load the appropriate team model and specified model type
        if model!=1 and model !=2:
            model=1
        if team==2:
            self.model=Actor("Art/Models/warden.egg")
        elif team==1: #load prisoner garb if it's a prisoner
            self.model=Actor("Art/Models/human"+str(model)+"-modelp.egg")
        else:
            self.model=Actor("Art/Models/human"+str(model)+"-model.egg")
        self.model.loadAnims({"Dying": "Art/animations/human"+str(model)+"-death.egg"})
        self.model.reparentTo(rootnode)
        self.model.setPos(startpos)
        self.model.setH(starth)
        self.model.setScale(AI.scale,AI.scale,AI.scale)
        self.manifest=AI_manifest(self.model)
        
        
        self.level=level
        
        
        
        #~Add to AI_list
        
        AI.AI_dict[AI.ID] = self
        
        #~ Initialize collision ~#
        
        #World collision
        #Bit channels are only walls and floors!
    
        self.cs=CollisionSphere(0,0,0,1.0*AI.scale)
        self.cspath=self.model.attachNewNode(CollisionNode('AIspher;' +  str(AI.ID)))
        self.cspath.node().addSolid(self.cs)
        self.cspath.node().setFromCollideMask(BitMask32(0x01))
        self.cspath.setPos(0,0,2.5*AI.scale)
        self.cspath.setCollideMask(BitMask32(0x11))
        #self.cspath.show()
        
        self.cr=CollisionRay(0,0,0.1,0,0,-1)
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
        self.mhandle_floor.setOffset(0.1)
        
        base.cTrav.addCollider(self.cspath, self.mhandle_wall)
        base.cTrav.addCollider(self.crpath, self.mhandle_floor)
        
        #Firing collision (Passive/Into object only, bullets are active)
        #Bit channel is only bullets
        self.ct=CollisionTube(0,0,5*AI.scale,0,0,0/AI.scale,1*AI.scale)
        self.ctpath=self.model.attachNewNode(CollisionNode('AItarget;' +  str(AI.ID)))
        self.ctpath.node().addSolid(self.ct)
        self.ctpath.node().setFromCollideMask(BitMask32(0x00))
        self.ctpath.setCollideMask(BitMask32(0x04))
        #self.ctpath.show()
        
        #Aiming collision: floor, walls, doors, and Player, and AI bullet channels
        self.ftrav=CollisionTraverser("AIfiretrav")
        self.fr=CollisionRay(0,0,0,0,1,0)
        self.frpath=self.model.attachNewNode(CollisionNode('AIcray;' +  str(AI.ID)))
        self.frpath.node().addSolid(self.fr)
        self.frpath.node().setFromCollideMask(BitMask32(0x0f))
        self.frpath.setPos(0,0,5*AI.scale)
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
        
        #Root is joint69: on human2 it's human1crouching:joint69
        
        #Set weapon, weapon model, and load animations based on weapon
        temp=self.model.exposeJoint(None, "modelRoot", "right_hand")
        temp2=self.model.exposeJoint(None, "modelRoot", "joint20")
        self.model.makeSubpart("arms", ["joint18", "joint68"])
        self.blah=False
        if (weapon == 1):
            self.drop = "pistol"
            self.dropmodel = "Art/Models/pistol.egg"
            self.pscale=Vec3(0.05, 0.05, 0.05)
            self.weapon = Weapon.Pistol(self.model, False, Vec3(0,0,4))
            self.killzone=30*AI.scale
            self.model.loadAnims({"Crouch": "Art/animations/human"+str(model)+"-crouchingpistol.egg"})
            self.model.loadAnims({"Run": "Art/animations/human"+str(model)+"-runningpistol.egg"})
            self.model.loadAnims({"Walk": "Art/animations/human"+str(model)+"-runningpistol.egg"})
            self.model.loadAnims({"Idle": "Art/animations/human"+str(model)+"-idlepistol.egg"})
            self.model.loadAnims({"Fire": "Art/animations/human"+str(model)+"-firepistol.egg"})
            w=loader.loadModel("Art/Models/pistol.egg")
            self.anim_start={"Crouch":1, "Run":0, "Walk":0, "Idle":6, "Fire":6}
            self.anim_end={"Crouch":self.model.getNumFrames("Crouch")-1}
            self.anim_end["Run"]=self.model.getNumFrames("Run")-1
            self.anim_end["Walk"]=self.model.getNumFrames("Walk")-1
            self.anim_end["Idle"]=42
            self.anim_end["Fire"]=self.model.getNumFrames("Fire")-30
            w.setScale(0.05,0.05,0.05)
            w.setPos(0.55,0.0,-0.1)
            w.setHpr(160,90,0)
            w.reparentTo(temp)
        elif (weapon ==2):
            self.blah=True
            self.drop = "shotgun"
            self.dropmodel = "Art/Models/shotgun.egg"
            self.pscale=Vec3(0.1, 0.1, 0.1)
            self.weapon = Weapon.Shotgun(self.model, False, Vec3(0,0,4))
            self.killzone=20*AI.scale
            self.model.loadAnims({"Crouch": "Art/animations/human"+str(model)+"-crouchingbiggun.egg"})
            self.model.loadAnims({"Run": "Art/animations/human"+str(model)+"-runningbiggun.egg"})
            self.model.loadAnims({"Walk": "Art/animations/human"+str(model)+"-runningbiggun.egg"})
            self.model.loadAnims({"Idle": "Art/animations/human"+str(model)+"-idleshotgun.egg"})
            self.model.loadAnims({"Fire": "Art/animations/human"+str(model)+"-fireshotgun.egg"})
            w=loader.loadModel("Art/Models/shotgun.egg")
            self.anim_start={"Crouch":0, "Run":6, "Walk":6, "Idle":0, "Fire":6}
            self.anim_end={"Crouch":self.model.getNumFrames("Crouch")-1}
            self.anim_end["Run"]=self.model.getNumFrames("Run")-1
            self.anim_end["Walk"]=self.model.getNumFrames("Walk")-20
            self.anim_end["Idle"]=self.model.getNumFrames("Idle")-20
            self.anim_end["Fire"]=self.model.getNumFrames("Fire")-1
            w.setScale(0.1, 0.1,0.1)
            w.setPos(0.80, 0.0, -0.4)
            w.setHpr(180,0,-15)
            w.reparentTo(temp)
            self.w=w
        elif (weapon ==3):
            self.drop="assault"
            self.dropmodel = "Art/Models/assaultrifle.egg"
            self.pscale=Vec3(0.1, 0.1, 0.1)
            self.killzone=30*AI.scale
            self.weapon = Weapon.Rifle(self.model, False, Vec3(0,0,4))
            self.model.loadAnims({"Crouch": "Art/animations/human"+str(model)+"-crouchingbiggun.egg"})
            self.model.loadAnims({"Run": "Art/animations/human"+str(model)+"-runningbiggun.egg"})
            self.model.loadAnims({"Walk": "Art/animations/human"+str(model)+"-runningbiggun.egg"})
            self.model.loadAnims({"Idle": "Art/animations/human"+str(model)+"-idleassultrifle.egg"})
            self.model.loadAnims({"Fire": "Art/animations/human"+str(model)+"-fireassultrifle.egg"})
            w=loader.loadModel("Art/Models/assaultrifle.egg")
            self.anim_start={"Crouch":0, "Run":6, "Walk":6, "Idle":0, "Fire":2}
            self.anim_end={"Crouch":self.model.getNumFrames("Crouch")-1}
            self.anim_end["Run"]=self.model.getNumFrames("Run")-20
            print self.model.getNumFrames("Run")
            self.anim_end["Walk"]=self.model.getNumFrames("Walk")-20
            self.anim_end["Idle"]=self.model.getNumFrames("Idle")-1
            self.anim_end["Fire"]=4
            w.setScale(0.1, 0.1,0.1)
            w.setPos(0.70, 0.0, 0)
            w.setHpr(170,0,0)
            w.reparentTo(temp)
        elif (weapon==4):
            # Change later to different melee weaps for different AI
            self.drop = "health"
            self.dropmodel = "Art/Models/health.egg"
            self.pscale=Vec3(0.5, 0.5, 0.5)
            self.weapon = Weapon.Knife(self.model, False, Vec3(0,0,4))
            self.killzone = 2.75
            self.model.loadAnims({"Crouch": "Art/animations/human"+str(model)+"-crouching.egg"})
            self.model.loadAnims({"Run": "Art/animations/human"+str(model)+"-running.egg"})
            self.model.loadAnims({"Walk": "Art/animations/human"+str(model)+"-running.egg"})
            self.model.loadAnims({"Idle": "Art/animations/human"+str(model)+"-idlepistol.egg"})
            self.model.loadAnims({"Fire": "Art/animations/human"+str(model)+"-fireknife.egg"})
            if team:
                w=loader.loadModel("Art/Models/shiv.egg")
                w.setPos(0.3,-0.1,-0.1)
                w.setHpr(45,0,0)
            else:
                w=loader.loadModel("Art/Models/knife.egg")
                w.setPos(0.3,-0.1,-0.1)
                w.setHpr(45,0,0)
            self.anim_start={"Crouch":0, "Run":0, "Walk":6, "Idle":6, "Fire":6}
            self.anim_end={"Crouch":self.model.getNumFrames("Crouch")-1}
            self.anim_end["Run"]=self.model.getNumFrames("Run")-1
            self.anim_end["Walk"]=self.model.getNumFrames("Walk")-1
            self.anim_end["Idle"]=42
            self.anim_end["Fire"]=self.model.getNumFrames("Fire")-23
            w.reparentTo(temp)
        else:
            # Change later to different melee weaps for different AI
            self.drop = "health"
            self.dropmodel = "Art/Models/health.egg"
            self.pscale=Vec3(0.5, 0.5, 0.5)
            self.weapon = Weapon.Pipe(self.model, False, Vec3(0,0,4))
            self.killzone = 2.75
            self.model.loadAnims({"Crouch": "Art/animations/human"+str(model)+"-crouching.egg"})
            self.model.loadAnims({"Run": "Art/animations/human"+str(model)+"-running.egg"})
            self.model.loadAnims({"Walk": "Art/animations/human"+str(model)+"-running.egg"})
            self.model.loadAnims({"Idle": "Art/animations/human"+str(model)+"-idlepistol.egg"})
            self.model.loadAnims({"Fire": "Art/animations/human"+str(model)+"-firetonfa.egg"})
            if team:
                w=loader.loadModel("Art/Models/pipe.egg")
                w.setScale(0.4, 0.4, 0.4)
                w.setHpr(-135, 0, 0)
                w.setPos(0.6,-0.4,-0.6)
            else:
                w=loader.loadModel("Art/Models/tonfa.egg")
                w.setScale(0.4, 0.4, 0.4)
                w.setHpr(-135, 0, 0)
                w.setPos(1.4,-0.6,-0.1)
            self.anim_start={"Crouch":0, "Run":0, "Walk":6, "Idle":6, "Fire":29}
            self.anim_end={"Crouch":self.model.getNumFrames("Crouch")-1}
            self.anim_end["Run"]=self.model.getNumFrames("Run")-1
            self.anim_end["Walk"]=self.model.getNumFrames("Walk")-1
            self.anim_end["Idle"]=42
            self.anim_end["Fire"]=self.model.getNumFrames("Fire")-1
            w.reparentTo(temp)
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
        self.dying=False
        self.dropped=False
        self.dead=False
        self.rundistance=0
        self.idle=False
        self.cinematic = False
        
        self.model.play("Idle", fromFrame=self.anim_start["Idle"], toFrame=self.anim_end["Idle"])
        self.idle=True
        
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
        if self.health<0: #Already dying
            return
        AI.hit.play()
        self.health -= damage
        self.look_angles = attacker.model.getPos()-self.model.getPos()
        self.look_angles = calculateHpr(self.look_angles, self.model.getHpr())
        if abs(self.look_angles.getX()-self.model.getH())>AI.FOV and self.targetlist==[]:
            self.forceturn = True
            self.target = attacker
            self.targetpos = attacker.model.getPos()
        if self.health<=0:
            self.model.play("Dying", fromFrame=6)
            self.dying=True
            self.dead = True
        
    def destroy(self, task_object):
        print "DESTROY"
        self.model.node().removeAllChildren()
        self.model.remove()
        del AI.AI_dict[self.ID]
        self.dead=True
        print "Dead to me"
        
    
    def tick(self,task_object):
        
        #if self.dead:
            #del self
            #return
        
        if self.cinematic:
            return Task.cont
       
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
        
        #if self.blah:
            #self.w.setR(self.w.getR()+1)
        
        if self.dying==True:
            if self.model.getCurrentFrame("Dying")>=self.model.getNumFrames("Dying")-4 and self.dropped==False:
                self.model.node().removeAllChildren()
                self.cspath.node().clearSolids()
                self.AIspath.node().clearSolids()
                self.ctpath.node().clearSolids()
                base.cTrav.removeCollider(self.AIspath)
                powerup=loader.loadModel(self.dropmodel)
                powerup.setPos(self.model.getPos()+Vec3(0,0,0.5))
                powerup.setScale(self.pscale)
                powerup.reparentTo(self.level.rootnode)
                sphere=CollisionSphere(0,0,0,1)
                spherep=powerup.attachNewNode(CollisionNode(self.drop))
                spherep.node().addSolid(sphere)
                spherep.setCollideMask(BitMask32(0x20))
                #spherep.show()
                self.dropped=True
                #self.dead=True
                #del AI.AI_dict[self.ID]
                #taskMgr.doMethodLater(5, self.destroy, "Remove me")
            return Task.cont
            
        distance = Vec3(self.level.player.model.getPos())-Vec3(self.model.getPos())
        distance.setZ(0)
        #STOP AI over 50 from player! Does this help? It doesn't seem to help much...
        if distance.length() >120:
            return Task.cont
        else:
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
                    if target.dying: #Don't waste your time on a dying target
                        self.targetpos=self.model.getPos()
                        break
                    self.look_angles = Vec3(target.model.getPos())-Vec3(self.model.getPos())
                    self.look_angles = calculateHpr(self.look_angles, self.model.getHpr())
                    #self.frpath.setHpr(self.look_angles-self.model.getHpr())
                    self.frpath.lookAt(target.cspath)
                    #self.frpath.show()
                    self.cspath.setCollideMask(BitMask32(0x00))
                    self.ctpath.setCollideMask(BitMask32(0x00))
                    self.ftrav.traverse(self.level.collisionStuff)
                    self.fire.sortEntries()
                    self.cspath.setCollideMask(BitMask32(0x11))
                    self.ctpath.setCollideMask(BitMask32(0x04))
                    self.fire.sortEntries()
                    #self.frpath.setHpr(Point3(0,0,0))
                    if self.fire.getNumEntries()>0 and self.fire.getEntry(0).getIntoNodePath().getParent()==target.model.getGeomNode():
                            #Vision is not occluded, use this target
                            self.seetarget=True
                            self.targetpos = target.model.getPos()
                            self.targetlist=[target]
                            break
                if self.seetarget==False:
                    #print self.seeplayer
                    #print self.model.getH()
                    #~ if self.health<10: #Health is at 1/5th strength
                        #~ if self.rundistance<10:
                            #~ self.dy=AI.runspeed
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
                                self.dy=min(AI.runspeed, (distance.length()-AI.followradius)/AI.movetweak)
                    elif self.targetlist != [] : #If had a target you lost sight of
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
                        self.dh=min(AI.turnspeed, max(self.look_angles.getX()-self.model.getH()-AI.accuracy2, -AI.turnspeed))
                        if abs(self.dh)<1:
                            distance = Vec3(self.targetpos)-Vec3(self.model.getPos())
                            distance.setZ(0)
                            if distance.length()>0:
                                self.dy=min(AI.runspeed, distance.length()/AI.movetweak)
                            else:
                                self.targetlist=[] #Lost your target
                    #If already there, idle
                else:
                    #~ if self.health<10: #Health is at 1/5th strength
                        #~ #Turn away from target
                        #~ self.dh=min(AI.turnspeed, max((self.look_angles[0]+180)%360-self.model.getH(), -AI.turnspeed))
                        #~ #If turned away from target, run
                        #~ if abs(self.dh)<20:
                            #~ self.dy=AI.runspeed
                    #~ else:
                    #Turn to face target
                    self.dh=min(AI.turnspeed, max(self.look_angles.getX()-self.model.getH()-AI.accuracy2, -AI.turnspeed))
                    #If facing target, fire at them
                    if abs(self.dh)<AI.accuracy1:
                        distance = Vec3(self.targetpos)-Vec3(self.model.getPos())
                        distance.setZ(0)
                        if distance.length()>self.killzone:
                            self.dy=min(AI.runspeed, distance.length())
                            #if distance.length()<self.killzone*1.4:
                                #self.shooting=True
                        else:
                            self.shooting=True
        #------------------------
        #Animation Handling
        #------------------------
        
        #print self.ID
        #print self.dy
        if self.dy>AI.runanim:
            self.idle=False
            #print "Run"
            self.model.setPlayRate(self.dy/AI.runanim, "Run")
            if not self.model.getAnimControl("Run").isPlaying():
                self.model.loop("Run", restart=self.anim_start["Run"], fromFrame=self.anim_start["Run"], toFrame=self.anim_end["Run"])
        elif self.dy>0:
            #print "Walk"
            self.idle=False
            self.model.setPlayRate(self.dy/AI.runanim, "Walk")
            if not self.model.getAnimControl("Walk").isPlaying():
                self.model.loop("Walk", restart=self.anim_start["Walk"], fromFrame=self.anim_start["Walk"], toFrame=self.anim_end["Walk"])
        #elif self.dh>0:
            #self.model.pose("Fire", self.anim_start["Fire"], partName="arms")        
        else:
            if not self.model.getAnimControl("Idle").isPlaying() and self.idle==False:
                self.model.play("Idle", fromFrame=self.anim_start["Idle"], toFrame=self.anim_end["Idle"])
                self.idle=True
        if self.shooting:
            if not self.model.getAnimControl("Fire").isPlaying():
                self.model.play("Fire", fromFrame=self.anim_start["Fire"], toFrame=self.anim_end["Fire"])
                self.weapon.shoot(self)
                self.weapon.shots=self.weapon.maxshots
        #------------------------    
        #Movement
        #------------------------
        angle = math.radians(self.model.getH())
        sa = math.sin(angle)
        ca = math.cos(angle)
        time_tick = globalClock.getDt()*6
        self.model.setX(self.model.getX()-ca*self.dx-sa*self.dy)
        self.model.setY(self.model.getY()+ca*self.dy-sa*self.dx)
        self.model.setH(self.model.getH()+self.dh*time_tick)
        self.model.setH((self.model.getH()+180)%360-180)
        self.loud=(self.weapon.firesound.status()==2)*40
        
        return Task.cont
 
#~ class Powerup():
        #~ def __init__(self, AI):
            #~ self.powerup=loader.loadModel("Art/Models/box.egg")
            #~ #self.powerup=loader.loadModel(AI.dropmodel)
            #~ self.powerup.show()
            #~ self.powerup.reparentTo(render)
            #~ self.powerup.setPos(AI.model.getPos()+Vec3(0,0,1))
            #~ sphere=CollisionSphere(0,0,0,3)
            #~ self.spherep=self.powerup.attachNewNode(CollisionNode(AI.drop))
            #~ self.spherep.node().addSolid(sphere)
            #~ self.spherep.setCollideMask(BitMask32(0x20))
            #~ #self.spherep.show()
            #~ taskMgr.add(self.tick, "Powerup tick")
        #~ def tick(self, task):
            #~ distance=self.powerup.getPos()-AI.playerhandle.model.getPos()
            #~ print distance.length()
            #~ #print self.powerup.getPos()
            #~ #print self.spherep.getPos()
            #~ return Task.cont
            
class AI_manifest(FSM.FSM):
    def init(self, model):
        self.model=model
    
