cellsize = 10

class Level(object):
    def __init__(self,levelfile):
        self.level=[]
        self.loadLevelfile(levelfile)	

    def loadLevelfile(self,levelfile):
        grid = open(levelfile, 'r').readlines()
        for row in grid:
            rooms = row.split(',')
            list=[]
            for room in rooms:
                list.append(Room(room))
            self.level.append(list)
                
    def draw(self):
        i=0
        for row in self.level:
            j=0
            for room in row:
                environ = loader.loadModel("Art/Models/door_1.egg")
                environ.reparentTo(render)
                environ.setPos(i*cellsize,j*cellsize,0*cellsize)
                environ.setHpr(180,0,0)
                j=j+1
            i=i+1

class Room(object):
    def __init__(self,room):
        self.WestWall = room[0]
        self.NorthWall = room[1]
        self.Floor = room[2]
        
level = Level("1.txt")

level.draw()