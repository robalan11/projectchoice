from pandac.PandaModules import * 
from AI import AI
from direct.actor.Actor import Actor

cellsize = 10
wallbuffer = 0.55
BumpMapping=False


class Level(object):
    def __init__(self,levelfile, player, entrancetype):
        
        self.rootnode = loader.loadModel("Art/Models/wall_1.egg")
        self.rootnode.setPos(0,0,0)
        self.rootnode.reparentTo(render)
        self.geometrynode=loader.loadModel("Art/Models/wall_1.egg")
        self.geometrynode.setPos(0,0,0)
        self.geometrynode.reparentTo(self.rootnode)
        
        self.collisionStuff = loader.loadModel("Art/Models/wall_1.egg")
        self.collisionStuff.setPos(0,0,0)
        self.collisionStuff.reparentTo(self.rootnode)
        
        self.floorceilnode = loader.loadModel("Art/Models/wall_1.egg")
        self.floorceilnode.setPos(0,0,0)
        self.floorceilnode.reparentTo(self.geometrynode)
        
        self.wallnode = loader.loadModel("Art/Models/wall_1.egg")
        self.wallnode.setPos(0,0,0)
        self.wallnode.reparentTo(self.collisionStuff)
        
        player.model.reparentTo(self.collisionStuff)
        self.level=[]
        self.door_dict={}
        self.doornum=0
        self.EntranceP=False
        self.EntranceG=False
        self.EntranceFacingP=0.0
        self.EntranceFacingG=0.0
        self.levelfilename = levelfile.split('/')[-1].split('.')[0]
        self.currentfilename=levelfile
        self.loadLevelfile(levelfile)
        self.cines = {}
        self.ais = []
        self.start()
        self.entrancetype = entrancetype
        self.player=player
        
        
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.1, 0.1, 0.1, 1))
        alnp = self.geometrynode.attachNewNode(alight)
        self.geometrynode.setLight(alnp)
        
        self.lightpivot = render.attachNewNode("lightpivot")
        plight = PointLight('plight')
        plight.setColor(Vec4(1.5, 1.5, 1.5, 1))
        plight.setAttenuation(Vec3(0.7,0.05,0))
        self.plnp = self.lightpivot.attachNewNode(plight)
        self.plnp.setPos(0, 0, 5)
        self.rootnode.setLight(self.plnp)
        self.rootnode.setShaderInput("light", self.plnp)
        
        
        
        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(0.9, 0.9, 0.6, 1))
        dlnp = self.rootnode.attachNewNode(dlight)
        dlnp.setHpr(10, -80, 0)
        self.rootnode.setLight(dlnp)
        
        
        if(entrancetype=="P" and self.EntranceP):
            player.nodepath().setPos(self.EntrancePx*cellsize,(-1*self.EntrancePy)*cellsize, 0.5*cellsize)
            player.nodepath().setHpr(self.EntranceFacingP,0,0)
        elif(entrancetype=="G" and self.EntranceG):
            player.nodepath().setPos(self.EntranceGx*cellsize,(-1*self.EntranceGy)*cellsize, 0.5*cellsize)
            player.nodepath().setHpr(self.EntranceFacingG,0,0)
        else:
            player.nodepath().setPos(1*cellsize,(-1*1)*cellsize,0.5*cellsize) #default location
            player.nodepath().setHpr(0,0,0)
            
        if(BumpMapping==True):
            self.rootnode.setShaderAuto()
    def loadLevelfile(self,levelfile):
        grid = open(levelfile, 'r').readlines()
        for row in grid:
            rooms = row.split(',')
            list=[]
            for room in rooms:
                myTiles=room.split('|')
                list.append(Room(myTiles))
            self.level.append(list)
                
    def start(self):
        self.draw()
        self.loadenemies()
        self.loaditems()
        self.loadcines()
        
    def drawInterior(self, x, y, model, orientation):
        environ=loader.loadModel(model)
        environ.reparentTo(self.collisionStuff)
        environ.setPos(x*cellsize,(-1*y)*cellsize, 0.0)
        environ.setHpr(90.0*int(orientation),0,0)
        tube=None
        if model=="Art/Models/barricade.egg":
            tube=CollisionTube(0,0,0,0,0,4,7)
        else:
            tube=CollisionSphere(0,0,0,3)
        tubep=environ.attachNewNode(CollisionNode("Interior"))
        tubep.node().addSolid(tube)
        tubep.setCollideMask(BitMask32(0x01))
            
    def loadInterior(self, y, x):
        if(self.level[y][x].Interior == "B"):
            self.drawInterior(x, y, "Art/Models/barricade.egg", self.level[y][x].InteriorFacing)
        elif(self.level[y][x].Interior == "T"):
            self.drawInterior(x, y, "Art/Models/table.egg", self.level[y][x].InteriorFacing)
        elif(self.level[y][x].Interior == "C"):
            self.drawInterior(x, y, "Art/Models/chair_wood.egg", self.level[y][x].InteriorFacing)
        elif(self.level[y][x].Interior == "M"):
            self.drawInterior(x, y, "Art/Models/chair_metal.egg", self.level[y][x].InteriorFacing)
        elif(self.level[y][x].Interior == "D"):
            self.drawInterior(x, y, "Art/Models/desk.egg", self.level[y][x].InteriorFacing)
        elif(self.level[y][x].Interior == "K"):
            self.drawInterior(x, y, "Art/Models/oven.egg", self.level[y][x].InteriorFacing)
        elif(self.level[y][x].Interior == "S"):
            self.drawInterior(x, y, "Art/Models/securityconsole.egg", self.level[y][x].InteriorFacing)
        elif(self.level[y][x].Interior == "L"):
            self.drawInterior(x, y, "Art/Models/bookcase.egg", self.level[y][x].InteriorFacing)
    def loadPowerup(self, powerup_model, powerup_name, x, y):
        powerup = None
        if(powerup_name == "armor"):
            powerup = Actor()
            powerup.loadModel(powerup_model)
            powerup.loadAnims({"spin":"Art/Models/body_armor_anim.egg"})
            
            powerup.loop("spin")
        else:
            powerup=loader.loadModel(powerup_model)
        powerup.setPos(Vec3(x*cellsize, -y*cellsize, 0))
        sphere=CollisionSphere(0,0,0,1)
        spherep=powerup.attachNewNode(CollisionNode(powerup_name))
        spherep.node().addSolid(sphere)
        spherep.setCollideMask(BitMask32(0x20))
        powerup.reparentTo(self.rootnode)

    
    def loaditems(self):
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                if(self.level[y][x].Entrance=="P"):
                    self.EntranceP=True
                    self.EntrancePx=x
                    self.EntrancePy=y
                    self.EntranceFacingP=int(self.level[y][x].EntranceFacing)
                elif(self.level[y][x].Entrance=="G"):
                    self.EntranceG=True
                    self.EntranceGx=x
                    self.EntranceGy=y
                    self.EntranceFacingG=int(self.level[y][x].EntranceFacing)
                    
                self.loadInterior(y, x)
                if(self.level[y][x].Items == "A"):
                    self.loadPowerup("Art/Models/pi_ammo_small", "pammo", x, y)
                elif(self.level[y][x].Items == "B"):
                    self.loadPowerup("Art/Models/sh_ammo_small", "sammo", x, y)
                elif(self.level[y][x].Items == "C"):
                    self.loadPowerup("Art/Models/ar_ammo_small", "aammo", x, y)
                elif(self.level[y][x].Items == "D"):
                    self.loadPowerup("Art/Models/health", "health", x, y)
                elif(self.level[y][x].Items == "E"):
                    self.loadPowerup("Art/Models/body_armor", "armor", x, y)
                elif(self.level[y][x].Items == "F"):
                    self.loadPowerup("Art/Models/pi_ammo_large", "pammolarge", x, y)
                elif(self.level[y][x].Items == "G"):
                    self.loadPowerup("Art/Models/sh_ammo_large", "sammolarge", x, y)
                elif(self.level[y][x].Items == "H"):
                    self.loadPowerup("Art/Models/ar_ammo_large", "aammolarge", x, y)
                    
    def loadenemies(self):
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                enemyFacing=int(self.level[y][x].EnemyFacing)*90.0+180.0
                #TO BE FIXED: AUTOMATIC WEAPONS DON"T LOAD
                #TO BE FIXED: Beefy guys are the same as normal guys
                
                if(self.level[y][x].Enemy=="A"):
                    #prison knife
                    self.ais.append(AI(1,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0,self.collisionStuff, self))
                elif(self.level[y][x].Enemy=="B"):
                    #prison pistol
                    self.ais.append(AI(1,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1,self.collisionStuff, self))
                elif(self.level[y][x].Enemy=="C"):
                    #prison shotgun
                    self.ais.append(AI(1,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2,self.collisionStuff, self))
                elif(self.level[y][x].Enemy=="D"):
                    #prison AK
                    pass#AI(loader.loadModel("Art/Models/human1-model.egg"),False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.collisionStuff,self)
                    self.ais.append(AI(1,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.collisionStuff, self))
                elif(self.level[y][x].Enemy=="E"):
                    #guard melee
                    AI(1,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="F"):
                    #guard pistol
                    self.ais.append(AI(1,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1,self.collisionStuff, self))
                elif(self.level[y][x].Enemy=="G"):
                    #guard shotgun
                    self.ais.append(AI(1,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2,self.collisionStuff, self))
                elif(self.level[y][x].Enemy=="H"):
                    #guard ak
                    AI(1,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="I"):
                    #prison knife
                    AI(2,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="J"):
                    #prison pistol
                    AI(2,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="K"):
                    #prison shotgun
                    AI(2,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="L"):
                    #prison AK
                    AI(2,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="M"):
                    #guard melee
                    AI(2,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="N"):
                    #guard pistol
                    AI(2,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="O"):
                    #guard shotgun
                    AI(2,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="P"):
                    #guard ak
                    AI(2,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.collisionStuff, self)
                elif(self.level[y][x].Enemy=="Q"):
                    #Warden
                    AI(3,False,2,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,5,self.collisionStuff, self)
                
    
    def loadcines(self):
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                self.cines[(y, x)] = self.level[y][x].Cin
    
    def prepareFloorModel(self, environ, texture):
        myTexture = loader.loadTexture(texture)
        environ.setCollideMask(BitMask32(0x02))
        environ.reparentTo(self.floorceilnode)
        
        environ.setTexture(myTexture, 1) 
        
    def prepareWallModel(self, environ, texture):
        myTexture = loader.loadTexture(texture)
        environ.setCollideMask(BitMask32(0x01))
        environ.reparentTo(self.wallnode)
        environ.setTexture(myTexture, 1)
        
        
    def drawCeiling(self, y, x):
        environ = loader.loadModel("Art/Models/ceiling_1.egg")
        environ.setCollideMask(BitMask32(0x02))
        environ.reparentTo(self.floorceilnode)
        environ.setPos(x*cellsize,(-1*y)*cellsize,1*cellsize)
        
    def drawFloor(self, y, x):
        texture = self.getFloorTextureName(self.level[y][x].Floor)
        
        environ = None
        type = self.level[y][x].Floor
        if(type=='F' or type=='g' or type=='h'):
            environ=loader.loadModel("Art/Models/floor_1.egg")
            environ.setPos(x*cellsize,(-1*y)*cellsize,0)
            self.drawCeiling( y, x)
            
            if(BumpMapping==True):
                normtext=self.getFloorNormalName(self.level[y][x].Floor)
                myTexture = loader.loadTexture(normtext)
                ts = TextureStage('ts')
                ts.setMode(TextureStage.MNormal)
                environ.setTexture(ts, myTexture)
            
        elif(type=='a' or type == 'b' or type == 'c' or type == 'e'):
            environ=loader.loadModel("Art/Models/stairs_2.egg")
        elif(type=='u' or type == 'd' or type == 'l' or type == 'r'):
            environ=loader.loadModel("Art/Models/stairs_up.egg")
        self.prepareFloorModel(environ, texture)
        if(type=='a' or type == 'l'):
            environ.setHpr(-90,0,0)
            environ.setPos(x*cellsize,(-1*y)*cellsize,0)
        elif(type=='b' or type == 'u'):
            environ.setHpr(0,0,0)
            environ.setPos((x)*cellsize,(-1*y)*cellsize,0)
        elif(type=='c' or type == 'r'):
            environ.setHpr(90,0,0)
            environ.setPos(x*cellsize,(-1*y)*cellsize,0)
        elif(type=='e' or type == 'd'):
            environ.setHpr(180,0,0)
            environ.setPos((x)*cellsize,(-1*y)*cellsize,0)
        
        
    def prepareDoor(self, environ):
        sphere=CollisionSphere(0,0,0,3)
        spherep=environ.attachNewNode(CollisionNode("door"+str(self.doornum)))
        spherep.node().addSolid(sphere)
        spherep.setCollideMask(BitMask32(0x21))
        self.door_dict["door"+str(self.doornum)]=environ
        self.doornum=self.doornum+1
        
    def drawWestDoor(self, y, x, texture):
        if(not self.level[y][x].Floor=="."):
            environ = loader.loadModel("Art/Models/wall_door_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos((x-(1-wallbuffer))*cellsize,(-1*y)*cellsize,(0.5)*cellsize)
            environ.setHpr(0,0,0)
            
        if(x>0 and not self.level[y][x-1].Floor=="."):
            # make a normal wall on the east
            environ = loader.loadModel("Art/Models/wall_door_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos((x-(wallbuffer))*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
            environ.setHpr(-180,0,0)
        environ = loader.loadModel("Art/Models/door_spacer_1.egg")
        self.prepareWallModel(environ,texture)
        environ.setPos((x-1+wallbuffer)*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
        environ.setHpr(-180,0,0)
        
        #Create the Door Itself
        environ = Actor()
        environ.loadModel("Art/Models/door_2")
        
        environ.loadAnims({'open':"Art/Models/door_2_open.egg"})
        environ.reparentTo(self.wallnode)
        environ.setPos((x-(wallbuffer)+0.05)*cellsize,(-1*y)*cellsize,(0+0.4)*cellsize)
        environ.setHpr(-180,0,0)
        
        self.prepareDoor(environ)
        
        
        
    def drawWestSliding(self, y, x, texture):
        if(not self.level[y][x].Floor=="."):
            environ = loader.loadModel("Art/Models/wall_door_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos((x-(1-wallbuffer))*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
            environ.setHpr(0,0,0)
            
        if(x>0 and not self.level[y][x-1].Floor=="."):
            # make a normal wall on the east
            environ = loader.loadModel("Art/Models/wall_door_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos((x-(wallbuffer))*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
            environ.setHpr(-180,0,0)
        environ = loader.loadModel("Art/Models/door_spacer_1.egg")
        self.prepareWallModel(environ,texture)
        environ.setPos((x-1+wallbuffer)*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
        environ.setHpr(-180,0,0)
        
        #Create the Door Itself
        environ = Actor("Art/Models/door_1")
        environ.loadAnims({'open':"Art/Models/door_1_open.egg"})
        environ.setCollideMask(BitMask32(0x01))
        environ.reparentTo(self.wallnode)
        environ.setPos((x-(wallbuffer)+0.1)*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
        environ.setHpr(-180,0,0)
        
        self.prepareDoor(environ)
            
    def drawWestWall(self, y, x, texture):
        
        if(not self.level[y][x].Floor=="."):
            environ = loader.loadModel("Art/Models/wall_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos((x-(1-wallbuffer))*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
            environ.setHpr(90,0,0)
            
        if(x>0 and not self.level[y][x-1].Floor=="."):
            # make a normal wall on the east
            environ = loader.loadModel("Art/Models/wall_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos((x-(wallbuffer))*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
            environ.setHpr(-90,0,0)
            
    def drawNorthWall(self, y, x, texture):
        myTexture = loader.loadTexture(texture)
        if(not self.level[y][x].Floor=="."):
            environ = loader.loadModel("Art/Models/wall_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos(x*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                    
        if(y>0 and not self.level[y-1][x].Floor=="."):
            environ = loader.loadModel("Art/Models/wall_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos(x*cellsize,((-1*y)+(wallbuffer))*cellsize,(0+0.5)*cellsize)
            environ.setHpr(180,0,0)
            
    def drawNorthDoor(self, y, x, texture):
        myTexture = loader.loadTexture(texture)
        if(not self.level[y][x].Floor=="."):
            environ = loader.loadModel("Art/Models/wall_door_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos(x*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
            environ.setHpr(-90,0,0)
                    
        if(y>0 and not self.level[y-1][x].Floor=="."):
            environ = loader.loadModel("Art/Models/wall_door_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos(x*cellsize,((-1*y)+(wallbuffer))*cellsize,(0+0.5)*cellsize)
            environ.setHpr(90,0,0)
        environ = loader.loadModel("Art/Models/door_spacer_1.egg")
        self.prepareWallModel(environ,texture)
        environ.setPos(x*cellsize,((-1*y)+(wallbuffer))*cellsize,(0+0.5)*cellsize)
        environ.setHpr(-90,0,0)
        
        #Create the Door Itself
        environ = Actor("Art/Models/door_2")
        environ.loadAnims({'open':"Art/Models/door_2_open.egg"})
        environ.setCollideMask(BitMask32(0x01))
        environ.reparentTo(self.wallnode)
        environ.setPos(x*cellsize,((-1*y)+(wallbuffer)-0.05)*cellsize,(0+0.4)*cellsize)
        environ.setHpr(-90,0,0)
        
        self.prepareDoor(environ)
        
    def drawNorthSliding(self, y, x, texture):
        myTexture = loader.loadTexture(texture)
        if(not self.level[y][x].Floor=="."):
            environ = loader.loadModel("Art/Models/wall_door_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos(x*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
            environ.setHpr(-90,0,0)
                    
        if(y>0 and not self.level[y-1][x].Floor=="."):
            environ = loader.loadModel("Art/Models/wall_door_1.egg")
            self.prepareWallModel(environ, texture)
            environ.setPos(x*cellsize,((-1*y)+(wallbuffer))*cellsize,(0+0.5)*cellsize)
            environ.setHpr(90,0,0)
        environ = loader.loadModel("Art/Models/door_spacer_1.egg")
        self.prepareWallModel(environ,texture)
        environ.setPos(x*cellsize,((-1*y)+(wallbuffer))*cellsize,(0+0.5)*cellsize)
        environ.setHpr(-90,0,0)
        
        #Create the Door Itself
        environ = Actor("Art/Models/door_1")
        environ.loadAnims({'open':"Art/Models/door_1_open.egg"})
        environ.setCollideMask(BitMask32(0x01))
        environ.reparentTo(self.wallnode)
        environ.setPos(x*cellsize,((-1*y)+(wallbuffer))*cellsize,(0+0.5)*cellsize)
        environ.setHpr(-90,0,0)
        
        self.prepareDoor(environ)
            
            
    def isWestWallEmpty(self,y,x):
        return (self.level[y][x].WestWall == "." and self.level[y][x].WestWallType == ".")
    def isNorthWallEmpty(self,y,x):
        return (self.level[y][x].NorthWall == "." and self.level[y][x].NorthWallType == ".")
        
    def getFloorTextureName(self, type):
        if(type == "F"):
            return "Art/Textures/stone_tiles_1.jpg"
        elif(type == "g"):
            return "Art/Textures/stone_bricks_1.jpg"
        elif(type == "h"):
            return "Art/Textures/dirty_bricks.jpg"
        else:
            return "Art/Textures/stone_tiles_1.jpg"
    def getFloorNormalName(self, type):
        if(type == "F"):
            return "Art/Textures/stone_tiles_1_norm.jpg"
        elif(type == "g"):
            return "Art/Textures/stone_bricks_1_norm.jpg"
        elif(type == "h"):
            return "Art/Textures/dirty_bricks_norm.jpg"
        else:
            return "Art/Textures/stone_tiles_1_norm.jpg"
            
    def draw(self):
        #for each room
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
            
                if(not self.level[y][x].Floor == "."):
                    # make a normal floor
                    self.drawFloor(y,x)
                    
                NorthWallTexture="Art/Textures/concrete1.jpg"
                if(self.level[y][x].NorthWallType == "A"):
                    NorthWallTexture="Art/Textures/stone_bricks_1.jpg"
                    
                    
                elif(self.level[y][x].NorthWallType == "B"):
                    NorthWallTexture="Art/Textures/dirty_bricks.jpg"
                    
                    
                elif(self.level[y][x].NorthWallType == "C"):
                    NorthWallTexture="Art/Textures/drywall_rough.jpg"
                else:
                    NorthWallTexture="Art/Textures/concrete2.jpg"
                    
                
                WestWallTexture="Art/Textures/concrete1.jpg"
                if(self.level[y][x].WestWallType == "A"):
                    WestWallTexture="Art/Textures/stone_bricks_1.jpg"
                    
                elif(self.level[y][x].WestWallType == "B"):
                    WestWallTexture="Art/Textures/dirty_bricks.jpg"
                elif(self.level[y][x].WestWallType == "C"):
                    WestWallTexture="Art/Textures/drywall_rough.jpg"
                    
                else:
                    WestWallTexture="Art/Textures/concrete2.jpg"
                        
                #NorthWallTexture="Art/Textures/dirty_bricks.jpg"
                
                if(self.level[y][x].WestWall=="." and not self.level[y][x].WestWallType == "."):
                    # make a normal wall on the west
                    self.drawWestWall(y,x,WestWallTexture)
                    
                elif(self.level[y][x].WestWall=="D"):
                    # make a door on the west
                    self.drawWestDoor(y,x,WestWallTexture)
                elif(self.level[y][x].WestWall=="S"):
                    #make a sliding door on the west
                    self.drawWestSliding(y,x,WestWallTexture)
                        
                if(self.level[y][x].NorthWall=="." and not self.level[y][x].NorthWallType == "." ):
                    # make a normal north wall
                    self.drawNorthWall(y,x, NorthWallTexture)
                    
                elif(self.level[y][x].NorthWall=="D"):
                    # make a door on the north
                    self.drawNorthDoor(y,x,NorthWallTexture)
                
                elif(self.level[y][x].NorthWall=="S"):
                    #make a sliding door on the west
                    self.drawNorthSliding(y,x,NorthWallTexture)
                  
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x) and self.isNorthWallEmpty(y,x)):
                    if(x>0 and y>0 and not( self.isWestWallEmpty(y-1,x) and self.isNorthWallEmpty(y,x-1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, NorthWallTexture)
                        environ.setPos((x-(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(-90,0,0)
                        tube=CollisionTube(0,0,0,0,0,cellsize,2)
                        tubep=environ.attachNewNode(CollisionNode("corner"))
                        tubep.node().addSolid(tube)
                        tubep.setCollideMask(BitMask32(0x01))
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x+1) and self.isNorthWallEmpty(y,x)):
                    if(x>0 and y>0 and not( self.isNorthWallEmpty(y,x+1) and self.isWestWallEmpty(y-1,x+1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, NorthWallTexture)
                        environ.setPos((x+(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(180,0,0)
                        tube=CollisionTube(0,0,0,0,0,cellsize,2)
                        tubep=environ.attachNewNode(CollisionNode("corner"))
                        tubep.node().addSolid(tube)
                        tubep.setCollideMask(BitMask32(0x01))
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x) and self.isNorthWallEmpty(y+1,x)):
                    if(x>0 and y>0 and not( self.isWestWallEmpty(y+1,x) and self.isNorthWallEmpty(y+1,x-1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, NorthWallTexture)
                        environ.setPos((x-(1-wallbuffer))*cellsize,((-1*y)-(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(0,0,0)
                        tube=CollisionTube(0,0,0,0,0,cellsize,2)
                        tubep=environ.attachNewNode(CollisionNode("corner"))
                        tubep.node().addSolid(tube)
                        tubep.setCollideMask(BitMask32(0x01))
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x+1) and self.isNorthWallEmpty(y+1,x)):
                    if(x>0 and y>0 and not( self.isWestWallEmpty(y+1,x+1) and self.isNorthWallEmpty(y+1,x+1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, NorthWallTexture)
                        environ.setPos((x+(1-wallbuffer))*cellsize,((-1*y)-(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(90,0,0)
                        tube=CollisionTube(0,0,0,0,0,cellsize,2)
                        tubep=environ.attachNewNode(CollisionNode("corner"))
                        tubep.node().addSolid(tube)
                        tubep.setCollideMask(BitMask32(0x01))

class Room(object):
    def __init__(self,room):
        #assign values to variables
        self.Floor = room[0]
        self.WestWall = room[4]
        self.WestWallType = room[3]
        self.NorthWall = room[2]
        self.NorthWallType = room[1]
        self.Enemy = room[8]
        self.EnemyFacing = room[7]
        self.Interior = room[6]
        self.InteriorFacing = room[5]
        self.Items = room[10]
        self.Cin = room[12]
        self.Entrance = room[14]
        self.EntranceFacing = room[13]
        
        
        if(self.EnemyFacing == "."):
            self.EnemyFacing = "0"
        if(self.InteriorFacing == "."):
            self.InteriorFacing = "0"
        if(self.EntranceFacing == "."):
            self.EntranceFacing = "0"
            
        if(int(self.InteriorFacing)% 2 == 1):
            self.InteriorFacing= str(int(self.InteriorFacing)-2)
        
        if(int(self.EnemyFacing)% 2 == 1):
            self.EnemyFacing= str(int(self.EnemyFacing)-2)
            
        
        if(int(self.EntranceFacing)% 2 == 1):
            self.EntranceFacing= str(int(self.EntranceFacing)-2)
        self.EntranceFacing=str((int(self.EntranceFacing)+2)*90)
        
