class Level(object):
    def __init__(self,levelfile):
        self.level=[]
        self.loadLevelfile(levelfile)	

    def loadLevelfile(self,levelfile):
        grid = open(levelfile, 'r').readlines()
        for row in grid:
            rooms = row.split(',')
            for room in rooms:
                self.level.append(Room(room))
    def draw(self):
	    eviron= loader.loadModel("Art/Models/..")
	    environ.repartentTo(render)
	    environ.setScale(1,1,1)
	    environ.setPos(0,0,0)

class Room(object):
    def __init__(self,room):
        self.WestWall = room[0]
        self.NorthWall = room[1]
        self.Floor = room[2]
        print self.WestWall, self.NorthWall, self.Floor
        
level = Level("1.txt")

level.draw()
run()