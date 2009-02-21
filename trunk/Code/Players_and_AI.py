import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
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
            #~ open doors in front of player
            #~ if door is locked prisoner door and have key
                #~ release_prisoner
            #~ toggle follow flag of friendly AI in front of player
        #~ if animation playing is not the weapon firing/weapon is not reloading
            #~ if player pressed fire button
        if (key_mapping["shoot"]=1):
            key_mapping["shoot"]=0 #hack for demo, remove once have anims
                #~ get properties of current weapon
                #~ start firing animation as self-managing interval
                #~ fire a ray with appropriate range and get collision detection
            self.ftrav.traverse()
            self.sight.sortEntries()
            for i in range(self.sight.getNumEntries()):
                object=self.sight.getEntry(i)
                #~ if weapon hits an AI
                if (object.getIntoPath().getName()=="AItarget")
                    object.getIntoPath().getParent().Remove() #Current hack
                    break
                if (object.getIntoPath().getName()=="wall" or object.getIntoPath().getName()=="floor")
                    break
                    #~ do damage and alert AI
                    #~ broadcast_attack(AI_hit)
            #~ else if input requests changing the weapon and have that weapon 
                #~ and ammo
            #~ Change to that weapon
    def broadcast_attack(self, AI_hit)
        for enemy in self.enemies_watching
            #~ if AI is not AI_hit
            if (enemy != AI_hit):
                #~ if AI_hit is ally
                if AI_hit.team=enemy.team
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
        self.setPos(self.getPos()+Vec3(dx*self.dx*time_tick, dy*self.dy*time_tick, 0)
        #~ if (self.m_handlefloor.isOnGround()):
            #~ self.m_handlefloor.setVelocity(self.dz)
            
        #~ set camera to player’s position (anchored to player, so done automatically
        #~ update the GUI
    def collided(self):
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
        #~ Unlock the prisoner’s door
        #~ prisoner follows scripted procedure to get out
        #~ broadcast_attack(Dummy guard)
    def possess(self):
        #~ hand over control to the cinema code
    def relinquish(self):
        #~ return control to the player

class AI (Actor):
    def __init__(self, team, weapon):
        #~ set team value to the appropriate side
        #~ initialize actor with the appropriate model
        #~ Set weapon and attach weapon model to AI’s hand
        #~ Parent to the world
        #~ collision setup for movement
        #~ collision setup for weapons targeting
        #~ collision setup for limited AI vision (have collision spheres for LOS)
        #~ empty list for line of sight
    def tick(self):
        #~ check and set lights of current room to player
        #~ if under cinematic control
            #~ run cinema_tick(self) and nothing else
    #~ if in a room and state is get out of room
            #~ follow script for getting out and nothing else
        #~ if in hallway and state is get into room
            #~ follow script for getting in and nothing else
        #~ if running firing animation
            #~ return
        #~ run vision collision detection and recompile list of what AI sees
        #~ if see what you’re attacking
            #~ timestamp where you saw target
    #~ if health is high
                #~ fire
        #~ elseif you see an enemy or the player who’s an enemy
            #~ if self.health is high
                #~ attack(enemy)
            #~ else
                #~ Calculate optimum run away direction
                #~ Run away!
        #~ elseif you see the player and she’s an ally and self.follow=True
            #~ if she’s more than x feet away
                #~ Run to player!
        #~ elseif you don’t see any enemies because your target ran away
                #~ Run to last seen position
    #~ If already there, turn to face the middle of the hallway and wait
    #~ if vision detected the player and not on the player’s AI-that-see-me list
            #~ player.add_to_list(self)
            #~ self.seeplayer=true
        #~ elseif on the player’s AI-that-see-me list
            #~ player.remove_from_list(self)
            #~ self.seeplayer=false
    #~ set the animation to the correct one
        #~ save current location as previous location
        #~ move the AI based upon input commands from code
    
    def attack(self,target):
        #~ Set state to attack and set target
        self.state=attack
        self.target=target

    def fire(self):
        #~ get properties of current weapon
        #~ start firing animation as self-managing interval
        #~ fire a ray with appropriate range and get collision detection
        #~ if weapon hits an AI
            #~ do damage and alert AI
        #~ elseif weapon hits player
            #~ do damage (give position for HUD graphic?)
    def possess(self):
        #~ hand over control to the cinema code

    def relinquish(self):
        #~ return control to the AI
    
    def collided(self, collide_list): #~ movement collision event
        #~ return to previous position and turn towards the inside of the hallway
        #~ Note that you collided
