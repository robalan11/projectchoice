from pandac.PandaModules import * 
from AI import AI

cellsize = 10
wallbuffer = 0.55

class Level(object):
    def __init__(self,levelfile, player, entrancetype):
        self.level=[]
        self.EntranceP=False
        self.EntranceG=False
        self.loadLevelfile(levelfile)    
        self.start()
        if(entrancetype=="P" and self.EntranceP):
            player.nodepath().setPos(self.EntrancePx*cellsize,(-1*self.EntrancePy)*cellsize, 0.5*cellsize)
        elif(entrancetype=="G" and self.EntranceG):
            player.nodepath().setPos(self.EntranceGx*cellsize,(-1*self.EntranceGy)*cellsize, 0.5*cellsize)
        else:
            player.nodepath().setPos(1*cellsize,(-1*1)*cellsize,0.5*cellsize) #default location

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
        
    def loaditems(self):
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                if(self.level[y][x].Entrance=="P"):
                    self.EntranceP=True
                    self.EntrancePx=x
                    self.EntrancePy=y
                elif(self.level[y][x].Entrance=="G"):
                    self.EntranceG=True
                    self.EntranceGx=x
                    self.EntranceGy=y
            
                if(self.level[y][x].Items == "A"):
                    pass
                elif(self.level[y][x].Items == "B"):
                    pass
                elif(self.level[y][x].Items == "C"):
                    pass
                elif(self.level[y][x].Items == "D"):
                    pass
                elif(self.level[y][x].Items == "E"):
                    pass
                elif(self.level[y][x].Items == "F"):
                    pass
                elif(self.level[y][x].Items == "G"):
                    pass
                elif(self.level[y][x].Items == "H"):
                    pass
                    
    def loadenemies(self):
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                enemyFacing=int(self.level[y][x].EnemyFacing)*90.0
                if(self.level[y][x].Enemy=="a"):
                    #prison knife
                    AI(loader.loadModel("Art/Models/human1-model.egg"),False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0)
                if(self.level[y][x].Enemy=="b"):
                    #prison pistol
                    AI(loader.loadModel("Art/Models/human1-model.egg"),False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1)
                if(self.level[y][x].Enemy=="c"):
                    #prison shotgun
                    AI(loader.loadModel("Art/Models/human1-model.egg"),False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2)
                if(self.level[y][x].Enemy=="d"):
                    #prison AK
                    AI(loader.loadModel("Art/Models/human1-model.egg"),False,True,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3)
                if(self.level[y][x].Enemy=="e"):
                    #guard melee
                    AI(loader.loadModel("Art/Models/human1-model.egg"),False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0)
                if(self.level[y][x].Enemy=="f"):
                    #guard pistol
                    AI(loader.loadModel("Art/Models/human1-model.egg"),False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1)
                if(self.level[y][x].Enemy=="g"):
                    #guard shotgun
                    AI(loader.loadModel("Art/Models/human1-model.egg"),False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2)
                if(self.level[y][x].Enemy=="h"):
                    #guard ak
                    AI(loader.loadModel("Art/Models/human1-model.egg"),False,False,Vec3(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3)
                
    def prepareFloorModel(self, environ, texture):
        myTexture = loader.loadTexture(texture)
        environ.setCollideMask(BitMask32(0x02))
        environ.reparentTo(render)
        
        #TO BE FIXED
        environ.setTexture(myTexture, 1) 
        #Causes flickering, but texture doesn't appear!
        
    def prepareWallModel(self, environ, texture):
        myTexture = loader.loadTexture(texture)
        environ.setCollideMask(BitMask32(0x01))
        environ.reparentTo(render)
        environ.setTexture(myTexture, 1)
        
    def drawFloor(self, y, x, texture):
        
        environ = loader.loadModel("Art/Models/floor_1.egg")
        self.prepareFloorModel(environ, texture)
        environ.setPos(x*cellsize,(-1*y)*cellsize,0*cellsize)
        
        
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
                    self.drawFloor(y,x, self.getFloorTextureName(self.level[y][x].Floor))
                
                if(self.level[y][x].WestWall=="." and not self.level[y][x].WestWallType == "."):
                    # make a normal wall on the west
                    self.drawWestWall(y,x,"Art/Textures/stone_tiles_1.jpg")
                    
                if(self.level[y][x].WestWall=="D"):
                    # make a door on the west
                    self.drawWestDoor(y,x,"Art/Textures/stone_tiles_1.jpg")
                    
                if(self.level[y][x].NorthWall=="." and not self.level[y][x].NorthWallType == "." ):
                    # make a normal north wall
                    self.drawNorthWall(y,x, "Art/Textures/stone_tiles_1.jpg")
                    
                if(self.level[y][x].NorthWall=="D"):
                    # make a door on the north
                    self.drawNorthDoor(y,x,"Art/Textures/stone_tiles_1.jpg")
                    
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x) and self.isNorthWallEmpty(y,x)):
                    if(x>0 and y>0 and not( self.isWestWallEmpty(y-1,x) and self.isNorthWallEmpty(y,x-1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, "Art/Textures/stone_tiles_1.jpg")
                        environ.setPos((x-(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(-90,0,0)
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x+1) and self.isNorthWallEmpty(y,x)):
                    if(x>0 and y>0 and not( self.isNorthWallEmpty(y,x+1) and self.isWestWallEmpty(y-1,x+1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, "Art/Textures/stone_tiles_1.jpg")
                        environ.setPos((x+(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(180,0,0)
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x) and self.isNorthWallEmpty(y+1,x)):
                    if(x>0 and y>0 and not( self.isWestWallEmpty(y+1,x) and self.isNorthWallEmpty(y+1,x-1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, "Art/Textures/stone_tiles_1.jpg")
                        environ.setPos((x-(1-wallbuffer))*cellsize,((-1*y)-(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(0,0,0)
                if(not self.level[y][x].Floor=="." and self.isWestWallEmpty(y,x+1) and self.isNorthWallEmpty(y+1,x)):
                    if(x>0 and y>0 and not( self.isWestWallEmpty(y+1,x+1) and self.isNorthWallEmpty(y+1,x+1))):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, "Art/Textures/stone_tiles_1.jpg")
                        environ.setPos((x+(1-wallbuffer))*cellsize,((-1*y)-(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(90,0,0)

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
        