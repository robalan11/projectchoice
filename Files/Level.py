from pandac.PandaModules import * 
from AI import AI
from direct.actor.Actor import Actor

cellsize = 10
wallbuffer = 0.55

class Level(object):
    def __init__(self,levelfile, player, entrancetype):
        self.rootnode = loader.loadModel("Art/Models/wall_1.egg")
        self.rootnode.setPos(-1,-1,-1)
        self.rootnode.reparentTo(render)
        self.level=[]
        self.EntranceP=False
        self.EntranceG=False
        self.EntranceFacingP=0.0
        self.EntranceFacingG=0.0
        self.levelfilename = levelfile.split('/')[-1].split('.')[0]
        self.loadLevelfile(levelfile)
        self.cines = {}
        self.ais = []
        self.start()
        self.entrancetype = entrancetype
        if(entrancetype=="P" and self.EntranceP):
            player.nodepath().setPos(self.EntrancePx*cellsize,(-1*self.EntrancePy)*cellsize, 0.5*cellsize)
            player.nodepath().setHpr(self.EntranceFacingP,0,0)
        elif(entrancetype=="G" and self.EntranceG):
            player.nodepath().setPos(self.EntranceGx*cellsize,(-1*self.EntranceGy)*cellsize, 0.5*cellsize)
            player.nodepath().setHpr(self.EntranceFacingG,0,0)
        else:
            player.nodepath().setPos(1*cellsize,(-1*1)*cellsize,0.5*cellsize) #default location
            player.nodepath().setHpr(0,0,0)
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
        environ.reparentTo(self.rootnode)
        environ.setPos(x*cellsize,(-1*y)*cellsize,(0)*cellsize)
        environ.setHpr(90.0*int(orientation),0,0)
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
            powerup.loadAnims({'spin':powerup_model})
            powerup.play('spin')
        else:
            powerup=loader.loadModel(powerup_model)
        powerup.setPos(Vec3(x*cellsize, -y*cellsize, 3))
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
                    self.EntranceFacingP=int(self.level[y][x].EntranceFacing) + 180
                elif(self.level[y][x].Entrance=="G"):
                    self.EntranceG=True
                    self.EntranceGx=x
                    self.EntranceGy=y
                    self.EntranceFacingG=int(self.level[y][x].EntranceFacing) + 180
                    
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
                    self.ais.append(AI(1,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0,self.rootnode))
                elif(self.level[y][x].Enemy=="B"):
                    #prison pistol
                    self.ais.append(AI(1,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1,self.rootnode))
                elif(self.level[y][x].Enemy=="C"):
                    #prison shotgun
                    self.ais.append(AI(1,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2,self.rootnode))
                elif(self.level[y][x].Enemy=="D"):
                    #prison AK
                    pass#AI(loader.loadModel("Art/Models/human1-model.egg"),False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.rootnode)
                    pass#self.ais.append(AI(loader.loadModel("Art/Models/human1-model.egg"),False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.rootnode))
                elif(self.level[y][x].Enemy=="E"):
                    #guard melee
                    AI(1,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0,self.rootnode)
                elif(self.level[y][x].Enemy=="F"):
                    #guard pistol
                    self.ais.append(AI(1,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1,self.rootnode))
                elif(self.level[y][x].Enemy=="G"):
                    #guard shotgun
                    self.ais.append(AI(1,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2,self.rootnode))
                elif(self.level[y][x].Enemy=="H"):
                    #guard ak
                    AI(1,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.rootnode)
                elif(self.level[y][x].Enemy=="I"):
                    #prison knife
                    AI(2,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0,self.rootnode)
                elif(self.level[y][x].Enemy=="J"):
                    #prison pistol
                    AI(2,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1,self.rootnode)
                elif(self.level[y][x].Enemy=="K"):
                    #prison shotgun
                    AI(2,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2,self.rootnode)
                elif(self.level[y][x].Enemy=="L"):
                    #prison AK
                    AI(2,False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.rootnode)
                elif(self.level[y][x].Enemy=="M"):
                    #guard melee
                    AI(2,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0,self.rootnode)
                elif(self.level[y][x].Enemy=="N"):
                    #guard pistol
                    AI(2,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1,self.rootnode)
                elif(self.level[y][x].Enemy=="O"):
                    #guard shotgun
                    AI(2,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2,self.rootnode)
                elif(self.level[y][x].Enemy=="P"):
                    #guard ak
                    AI(2,False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3,self.rootnode)
                
    
    def loadcines(self):
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                self.cines[(y, x)] = self.level[y][x].Cin
    
    def prepareFloorModel(self, environ, texture):
        myTexture = loader.loadTexture(texture)
        environ.setCollideMask(BitMask32(0x02))
        environ.reparentTo(self.rootnode)
        
        #TO BE FIXED
        environ.setTexture(myTexture, 1) 
        #Causes flickering, but texture doesn't appear!
        
    def prepareWallModel(self, environ, texture):
        myTexture = loader.loadTexture(texture)
        environ.setCollideMask(BitMask32(0x01))
        environ.reparentTo(self.rootnode)
        environ.setTexture(myTexture, 1)
        
        
    def drawCeiling(self, y, x):
        environ = loader.loadModel("Art/Models/ceiling_1.egg")
        environ.setCollideMask(BitMask32(0x02))
        environ.reparentTo(self.rootnode)
        environ.setPos(x*cellsize,(-1*y)*cellsize,1*cellsize)
        
    def drawFloor(self, y, x):
        texture = self.getFloorTextureName(self.level[y][x].Floor)
        
        environ = None
        type = self.level[y][x].Floor
        if(type=='F' or type=='g' or type=='h'):
            environ=loader.loadModel("Art/Models/floor_1.egg")
            environ.setPos(x*cellsize,(-1*y)*cellsize,0*cellsize)
            self.drawCeiling( y, x)
        elif(type=='a' or type == 'b' or type == 'c' or type == 'e'):
            environ=loader.loadModel("Art/Models/stairs_2.egg")
        elif(type=='u' or type == 'd' or type == 'l' or type == 'r'):
            environ=loader.loadModel("Art/Models/stairs_up.egg")
        self.prepareFloorModel(environ, texture)
        if(type=='a' or type == 'l'):
            environ.setHpr(-90,0,0)
            environ.setPos(x*cellsize,(-1*y)*cellsize,0*cellsize)
        elif(type=='b' or type == 'u'):
            environ.setHpr(0,0,0)
            environ.setPos((x)*cellsize,(-1*y)*cellsize,0*cellsize)
        elif(type=='c' or type == 'r'):
            environ.setHpr(90,0,0)
            environ.setPos(x*cellsize,(-1*y)*cellsize,0*cellsize)
        elif(type=='e' or type == 'd'):
            environ.setHpr(180,0,0)
            environ.setPos((x)*cellsize,(-1*y)*cellsize,0*cellsize)
        
        
        
        
        
    def drawWestDoor(self, y, x, texture):
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
            
            
    def isWestWallEmpty(self,y,x):
        return (self.level[y][x].WestWall == "." and self.level[y][x].WestWallType == ".")
    def isNorthWallEmpty(self,y,x):
        return (self.level[y][x].NorthWall == "." and self.level[y][x].NorthWallType == ".")
        
    def getFloorTextureName(self, type):
        if(type == "F"):
            return "Art/Textures/stone_tiles_1.jpg"
        else:
            return "Art/Textures/stone_tiles_1.jpg"
            
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
                    
                    
                elif(self.level[y][x].WestWallType == "B"):
                    NorthWallTexture="Art/Textures/dirty_bricks.jpg"
                    
                    
                elif(self.level[y][x].WestWallType == "C"):
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
                        self.prepareWallModel(environ, WestWallTexture)
                        environ.setPos((x-(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(-90,0,0)
                        tube=CollisionTube(0,0,0,0,0,cellsize,2)
                        tubep=environ.attachNewNode(CollisionNode("corner"))
                        tubep.node().addSolid(tube)
                        tubep.setCollideMask(BitMask32(0x01))
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x+1) and self.isNorthWallEmpty(y,x)):
                    if(x>0 and y>0 and not( self.isNorthWallEmpty(y,x+1) and self.isWestWallEmpty(y-1,x+1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, WestWallTexture)
                        environ.setPos((x+(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(180,0,0)
                        tube=CollisionTube(0,0,0,0,0,cellsize,2)
                        tubep=environ.attachNewNode(CollisionNode("corner"))
                        tubep.node().addSolid(tube)
                        tubep.setCollideMask(BitMask32(0x01))
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x) and self.isNorthWallEmpty(y+1,x)):
                    if(x>0 and y>0 and not( self.isWestWallEmpty(y+1,x) and self.isNorthWallEmpty(y+1,x-1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, WestWallTexture)
                        environ.setPos((x-(1-wallbuffer))*cellsize,((-1*y)-(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(0,0,0)
                        tube=CollisionTube(0,0,0,0,0,cellsize,2)
                        tubep=environ.attachNewNode(CollisionNode("corner"))
                        tubep.node().addSolid(tube)
                        tubep.setCollideMask(BitMask32(0x01))
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x+1) and self.isNorthWallEmpty(y+1,x)):
                    if(x>0 and y>0 and not( self.isWestWallEmpty(y+1,x+1) and self.isNorthWallEmpty(y+1,x+1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, WestWallTexture)
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
        
