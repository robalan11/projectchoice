from pandac.PandaModules import * 
from AI import AI

cellsize = 10
wallbuffer = 0.55

class Level(object):
    def __init__(self,levelfile):
        self.level=[]
        self.loadLevelfile(levelfile)    
        self.start()

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
    def loadenemies(self):
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                enemyFacing=self.level[y][x].EnemyFacing*90
                if(self.level[y][x].Enemy=="a"):
                    #prison knife
                    Enemy(loader.loadModel("Art/Models/human1-model.egg"),False,True,(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0)
                if(self.level[y][x].Enemy=="b"):
                    #prison pistol
                    Enemy(loader.loadModel("Art/Models/human1-model.egg"),False,True,(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1)
                if(self.level[y][x].Enemy=="c"):
                    #prison shotgun
                    Enemy(loader.loadModel("Art/Models/human1-model.egg"),False,True,(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2)
                if(self.level[y][x].Enemy=="d"):
                    #prison AK
                    Enemy(loader.loadModel("Art/Models/human1-model.egg"),False,True,(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3)
                if(self.level[y][x].Enemy=="e"):
                    #guard melee
                    Enemy(loader.loadModel("Art/Models/human1-model.egg"),False,False,(x*cellsize,(-1*y)*cellsize,0),enemyFacing,0)
                if(self.level[y][x].Enemy=="f"):
                    #guard pistol
                    Enemy(loader.loadModel("Art/Models/human1-model.egg"),False,False,(x*cellsize,(-1*y)*cellsize,0),enemyFacing,1)
                if(self.level[y][x].Enemy=="g"):
                    #guard shotgun
                    Enemy(loader.loadModel("Art/Models/human1-model.egg"),False,False,(x*cellsize,(-1*y)*cellsize,0),enemyFacing,2)
                if(self.level[y][x].Enemy=="h"):
                    #guard ak
                    Enemy(loader.loadModel("Art/Models/human1-model.egg"),False,False,(x*cellsize,(-1*y)*cellsize,0),enemyFacing,3)
                
    def prepareFloorModel(self, environ, texture):
        myTexture = loader.loadTexture(texture)
        environ.setCollideMask(BitMask32(0x02))
        environ.reparentTo(render)
        environ.setTexture(myTexture, 1)
        
    def prepareWallModel(self, environ, texture):
        myTexture = loader.loadTexture(texture)
        environ.setCollideMask(BitMask32(0x01))
        environ.reparentTo(render)
        environ.setTexture(myTexture, 1)
        
    def drawFloor(self, y, x, texture):
        
        environ = loader.loadModel("Art/Models/floor_1.egg")
        self.prepareFloorModel(environ, texture)
        environ.setPos(x*cellsize,(-1*y)*cellsize,0*cellsize)
        
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
            
    def draw(self):
        #for each room
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                
                if(self.level[y][x].Floor=="F"):
                    # make a normal floor
                    self.drawFloor(y,x, "Art/Textures/stone_tiles_1.jpg")
                
                if(self.level[y][x].WestWall=="." and not self.level[y][x].WestWallType == "."):
                    # make a normal wall on the west
                    self.drawWestWall(y,x,"Art/Textures/stone_tiles_1.jpg")
                    
                if(self.level[y][x].NorthWall=="." and not self.level[y][x].NorthWallType == "." ):
                    # make a normal north wall
                    self.drawNorthWall(y,x, "Art/Textures/stone_tiles_1.jpg")
                    
                if(not self.level[y][x].Floor=="." and self.level[y][x].WestWall=="." and self.level[y][x].NorthWall=="."):
                    if(x>0 and y>0 and not( self.level[y-1][x].WestWall=="." and self.level[y][x-1].NorthWall==".")):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, "Art/Textures/stone_tiles_1.jpg")
                        environ.setPos((x-(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(-90,0,0)
                if(not self.level[y][x].Floor=="." and self.level[y][x+1].WestWall=="." and self.level[y][x].NorthWall=="."):
                    if(x>0 and y>0 and not( self.level[y][x+1].NorthWall=="." and self.level[y-1][x+1].WestWall==".")):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, "Art/Textures/stone_tiles_1.jpg")
                        environ.setPos((x+(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(180,0,0)
                if(not self.level[y][x].Floor=="." and self.level[y][x].WestWall=="." and self.level[y+1][x].NorthWall=="."):
                    if(x>0 and y>0 and not( self.level[y+1][x].WestWall=="." and self.level[y+1][x-1].NorthWall==".")):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        self.prepareWallModel(environ, "Art/Textures/stone_tiles_1.jpg")
                        environ.setPos((x-(1-wallbuffer))*cellsize,((-1*y)-(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(0,0,0)
                if(not self.level[y][x].Floor=="." and self.level[y][x+1].WestWall=="." and self.level[y+1][x].NorthWall=="."):
                    if(x>0 and y>0 and not( self.level[y+1][x+1].WestWall=="." and self.level[y+1][x+1].NorthWall==".")):
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
        