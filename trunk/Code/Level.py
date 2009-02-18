
class Level(object):
    def __init__(levelfile):
        self.loadLevelfile(levelfile)
        self.run()

    def loadLevelfile(levelfile):
        grid = open(levelfile, 'r').readlines()
        for row in grid:
            rooms = row.split(',')
            for room in rooms:
                self.level.append(Room(room))

class Room(object):
    def __init__(room):
        self.WestWall = room[0]
        self.NorthWall = room[1]
        self.Floor = room[2]