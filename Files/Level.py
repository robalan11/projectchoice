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
                list.append(Room(room))
            self.level.append(list)
                
    def start(self):
        self.draw()
        self.loadenemies()
    def loadenemies(self):
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                if(self.level[y][x].Enemy=="a"):
                    #a = AI("badguy","knife","Art/Models/box.egg")
                    target = loader.loadModel("Art/Models/box.egg")
                    target.reparentTo(render)
                    targetnodepath=target.attachNewNode(CollisionNode("AItarget"))
                    targetnodepath.node().addSolid(CollisionSphere(0,0,0,0.75))
                    target.setPos(x*cellsize,(-1*y)*cellsize,0)
                    
    def draw(self):
        #for each room
        for y in xrange(len(self.level)):
            for x in xrange(len(self.level[y])):
                if(self.level[y][x].Floor=="F"):
                    # make a normal floor
                    environ = loader.loadModel("Art/Models/floor_1.egg")
                    environ.setCollideMask(BitMask32(0x02))
                    environ.reparentTo(render)
                    environ.setPos(x*cellsize,(-1*y)*cellsize,0*cellsize)
                if(self.level[y][x].WestWall=="W"):
                    # make a normal wall on the west
                    if(not self.level[y][x].Floor=="."):
                        environ = loader.loadModel("Art/Models/wall_1.egg")
                        environ.setCollideMask(BitMask32(0x01))
                        environ.reparentTo(render)
                        environ.setPos((x-(1-wallbuffer))*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(90,0,0)
                    if(x>0 and not self.level[y][x-1].Floor=="."):
                        # make a normal wall on the east
                        environ = loader.loadModel("Art/Models/wall_1.egg")
                        environ.setCollideMask(BitMask32(0x01))
                        environ.reparentTo(render)
                        environ.setPos((x-(wallbuffer))*cellsize,(-1*y)*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(-90,0,0)
                if(self.level[y][x].NorthWall=="W"):
                    # make a normal north wall
                    if(not self.level[y][x].Floor=="."):
                        environ = loader.loadModel("Art/Models/wall_1.egg")
                        environ.setCollideMask(BitMask32(0x01))
                        environ.reparentTo(render)
                        environ.setPos(x*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                    
                    if(y>0 and not self.level[y-1][x].Floor=="."):
                        environ = loader.loadModel("Art/Models/wall_1.egg")
                        environ.setCollideMask(BitMask32(0x01))
                        environ.reparentTo(render)
                        environ.setPos(x*cellsize,((-1*y)+(wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(180,0,0)
                if(not(not self.level[y][x].Floor=="." and self.level[y][x].WestWall=="." and self.level[y][x].NorthWall==".")
                   and(not self.level[y][x].Floor=="." and self.level[y][x+1].WestWall=="." and self.level[y][x].NorthWall==".")
                   and(not self.level[y][x].Floor=="." and self.level[y][x].WestWall=="." and self.level[y+1][x].NorthWall==".")
                   and(not self.level[y][x].Floor=="." and self.level[y][x+1].WestWall=="." and self.level[y+1][x].NorthWall==".")):
                    if(not self.level[y][x].Floor=="." and self.level[y][x].WestWall=="." and self.level[y][x].NorthWall=="."):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        environ.setCollideMask(BitMask32(0x01))
                        environ.reparentTo(render)
                        environ.setPos((x-(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(-90,0,0)
                    if(not self.level[y][x].Floor=="." and self.level[y][x+1].WestWall=="." and self.level[y][x].NorthWall=="."):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        environ.setCollideMask(BitMask32(0x01))
                        environ.reparentTo(render)
                        environ.setPos((x+(1-wallbuffer))*cellsize,((-1*y)+(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(180,0,0)
                    if(not self.level[y][x].Floor=="." and self.level[y][x].WestWall=="." and self.level[y+1][x].NorthWall=="."):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        environ.setCollideMask(BitMask32(0x01))
                        environ.reparentTo(render)
                        environ.setPos((x-(wallbuffer))*cellsize,((-1*y)-(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(90,0,0)
                    if(not self.level[y][x].Floor=="." and self.level[y][x+1].WestWall=="." and self.level[y+1][x].NorthWall=="."):
                        environ = loader.loadModel("Art/Models/corner_1.egg")
                        environ.setCollideMask(BitMask32(0x01))
                        environ.reparentTo(render)
                        environ.setPos((x+(wallbuffer))*cellsize,((-1*y)-(1-wallbuffer))*cellsize,(0+0.5)*cellsize)
                        environ.setHpr(0,0,0)

class Room(object):
    def __init__(self,room):
        #assign values to variables
        self.Floor = room[0]
        self.WestWall = room[2]
        self.NorthWall = room[1]
        self.Enemy = room[3]
        