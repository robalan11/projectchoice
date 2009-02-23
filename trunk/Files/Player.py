import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.actor.Actor import Actor
import math

#This assumes that base.cTrav has been defined

class Player (Actor):
    def __init__(self,arm_model):
        #~ initialize actor with the arm model
        Actor(arm_model)
        
        #~ Initialize collision ~#
        
        #World collision
        #Bit channels are only walls and floors!
        base.camera.reparentTo(self)
        base.camera.setPos(0,0,0.75)
        base.camera.setHpr(0,0,0)
        
        self.cs=CollisionSphere(0,0,-0.5,0.5)
        self.cspath=self.attachNewNode(CollisionNode('pspher'))
        self.cspath.node().addSolid(self.cs)
        
        self.cr=CollisionRay(0,0,0,0,0,-1)
        self.crpath=self.attachNewNode(CollisionNode('pray'))
        self.crpath.node().addSolid(self.cr)
        
        self.mhandle_wall=CollisionHandlerPusher()
        self.mhandle_floor=CollisionHandlerGravity()
        self.mhandle_floor.setGravity(0.5)
        self.mhandle_floor.setMaxVelocity(2)
        self.mhandle_floor.setOffset(1)
        
        base.cTrav.addCollider(self.cspath, self.mhandle_wall)
        base.cTrav.addCollider(self.crpath, self.mhandle_floor)
        
        #Firing collision (Passive/Into object only, bullets are active)
        #Bit channel is only bullets
        self.ct=CollisionSphere(0,0,1,0,0,-1,0.5)
        self.ctpath=self.attachNewNode(CollisionNode('ptarget'))
        self.ctpath.node().addSolid(self.ct)
        
        #Aiming collision: floor, walls, doors, and AI channels
        self.ftrav=CollisionTraverser("pfiretrav")
        self.fr=CollisionRay(0,0,0,1,0,0)
        self.frpath=base.camera.attachNewNode(CollisionNode('pcray'))
        self.frpath.node().addSolid(self.fr)
        self.sight=CollisionHandlerQueue()
        self.ftrav.addCollider(self.frpath, self.sight)
        
        #~ self.weapon = whatever the starting weapon is
        #~ set up an empty list of enemies that see me
        self.enemies_watching=[]
        
    def get_input (self, key_mapping):
        #~ set player to running or stopped depending upon key input
        #Panda3D has built-in support for moving the camera?
        if self.mhandle_floor.isOnGround(): #~ if not in the air
            self.dx = key_mapping["forward"] - key_mapping["backward"]
            self.dy = key_mapping["right"] - key_mapping["left"]
            #self.dz = key_mapping["jump"]
        #~ if player pressed use key
        if (key_mapping["use"]==1):
            pass
            #~ open doors in front of player
            #~ if door is locked prisoner door and have key
                #~ release_prisoner
            #~ toggle follow flag of friendly AI in front of player
        #~ if animation playing is not the weapon firing/weapon is not reloading
            #~ if player pressed fire button
        if (key_mapping["shoot"]==1):
            key_mapping["shoot"]=0 #hack for demo, remove once have anims
                #~ get properties of current weapon
                #~ start firing animation as self-managing interval
                #~ fire a ray with appropriate range and get collision detection
            self.ftrav.traverse()
            self.sight.sortEntries()
            for i in range(self.sight.getNumEntries()):
                object=self.sight.getEntry(i)
                #~ if weapon hits an AI
                if (object.getIntoPath().getName()=="AItarget"):
                    object.getIntoPath().getParent().Remove() #Current hack
                    break
                if (object.getIntoPath().getName()=="wall" or object.getIntoPath().getName()=="floor"):
                    break
                    #~ do damage and alert AI
                    #~ broadcast_attack(AI_hit)
            #~ else if input requests changing the weapon and have that weapon 
                #~ and ammo
            #~ Change to that weapon
    def broadcast_attack(self, AI_hit):
        for enemy in self.enemies_watching:
            #~ if AI is not AI_hit
            if (enemy != AI_hit):
                #~ if AI_hit is ally
                if AI_hit.team==enemy.team:
                    #~ lower team loyalty
                    if (self.loyalty[enemy.team]>0):
                        self.loyalty[enemy.team]-=1
                    #~ enemy attacks player
                    enemy.attack(self)
                else:
                    #~ raise team loyalty
                    if (self.loyalty[enemy.team]<100):
                        self.loyalty[enemy.team]+=1
            else:
                #~ AI_hit attacks player
                enemy.attack(self)
    def tick(self):
        #~ check and set lights of current room to player
        #~ if under cinematic control
            #~ run cinema_tick(self) and nothing else
        angle = math.radians(self.player.getH()) + math.pi
        dx = dist * math.sin(angle)
        dy = dist * -math.cos(angle)
        time_tick = globalClock.getDt()*6
        self.setPos(self.getPos()+Vec3(dx*self.dx*time_tick, dy*self.dy*time_tick, 0))
        #~ if (self.m_handlefloor.isOnGround()):
            #~ self.m_handlefloor.setVelocity(self.dz)
            
        #~ set camera to player's position (anchored to player, so done automatically
        #~ update the GUI
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

class AI (Actor):
    def __init__(self, team, weapon):
        pass
        #~ set team value to the appropriate side
        #~ initialize actor with the appropriate model
        #Set weapon and attach weapon to AI model's hand
        #~ Parent to the world
        #~ collision setup for movement
        #~ collision setup for weapons targeting
        #~ collision setup for limited AI vision (have collision spheres for LOS)
        #~ empty list for line of sight
    def tick(self):
        pass
        #Look at pseudocode
    
    def attack(self,target):
        #~ Set state to attack and set target
        self.state=attack
        self.target=target

    def fire(self):
        pass
        #~ get properties of current weapon
        #~ start firing animation as self-managing interval
        #~ fire a ray with appropriate range and get collision detection
        #~ if weapon hits an AI
            #~ do damage and alert AI
        #~ elseif weapon hits player
            #~ do damage (give position for HUD graphic?)
    def possess(self):
        pass
        #~ hand over control to the cinema code

    def relinquish(self):
        pass
        #~ return control to the AI
    
    def collided(self, collide_list): #~ movement collision event
        pass
        #~ return to previous position and turn towards the inside of the hallway
        #~ Note that you collided
