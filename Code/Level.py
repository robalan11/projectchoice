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

class Room(object):
    def __init__(self,room):
        self.WestWall = room[0]
        self.NorthWall = room[1]
        self.Floor = room[2]
        print self.WestWall, self.NorthWall, self.Floor
        
level = Level("1.txt")