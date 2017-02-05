import copy
from constants import Actions, MarkerType, SetupConstants
from tile import Tile, Plains, Resource, Base, Marker, Mountain
from robot import Robot, Bank
from globalVars import ResourceDepletions, MarkerLocations


class Board():
    def __init__(self, tiles, robots, bank):
        self.__tiles = tiles    #2d array containing [tile, numRobots, markers] for each location
        self.__robots = robots  #array containing all the player's robot objects
        self.__markers = []
        self.__bank = bank
        self.__length = len(tiles)
    def make_move(self, robot, moveTuple):
        (x,y) = robot.get_loc()
        tiles = self.__tiles

        # print(moveTuple)
        if (not isinstance(moveTuple[0], int)) or (not isinstance(moveTuple[1], int)):
            print('Error: All moves must be of the form (Actions, Actions), where the second Action is for marker color. If you do not wish to drop a marker, Use the DROP_NONE option.')
            return
        move = moveTuple[0]
        marker = moveTuple[1]
        #movement
        if move == Actions.MOVE_E:
            if y+1 < self.__length and tiles[x][y+1][0].CanMove():
                tiles[x][y][1] -= 1
                tiles[x][y+1][1] += 1
                robot.set_loc(x, y+1)
        elif move == Actions.MOVE_S:
            if x+1 < self.__length and tiles[x+1][y][0].CanMove():
                tiles[x][y][1] -= 1
                tiles[x+1][y][1] += 1
                robot.set_loc(x+1, y)
        elif move == Actions.MOVE_W:
            if y > 0 and tiles[x][y-1][0].CanMove():
                tiles[x][y][1] -= 1
                tiles[x][y-1][1] += 1
                robot.set_loc(x, y-1)
        elif move == Actions.MOVE_N:
            if x > 0 and tiles[x-1][y][0].CanMove():
                tiles[x][y][1] -= 1
                tiles[x-1][y][1] += 1
                robot.set_loc(x-1, y)
        elif move == Actions.MOVE_NE:
            if (x > 0 and y+1 < self.__length and
                        tiles[x-1][y+1][0].CanMove()):
                tiles[x][y][1] -= 1
                tiles[x-1][y+1][1] += 1
                robot.set_loc(x-1, y+1)
        elif move == Actions.MOVE_SE:
            if (x+1 < self.__length and y+1 < self.__length and
                        tiles[x+1][y+1][0].CanMove()):
                tiles[x][y][1] -= 1
                tiles[x+1][y+1][1] += 1
                robot.set_loc(x+1, y+1)
        elif move == Actions.MOVE_NW:
            if (x > 0 and y > 0 and
                        tiles[x-1][y-1][0].CanMove()):
                tiles[x][y][1] -= 1
                tiles[x-1][y-1][1] += 1
                robot.set_loc(x-1, y-1)
        elif move == Actions.MOVE_SW:
            if (x+1 < self.__length and y > 0 and
                        tiles[x+1][y-1][0].CanMove()):
                tiles[x][y][1] -= 1
                tiles[x+1][y-1][1] += 1
                robot.set_loc(x+1, y-1)
        #drop off supplies
        elif move == Actions.DROPOFF:
            if type(tiles[x][y][0]) == Base:
                robot.drop_resource(self.__bank)
        elif move == Actions.MINE:
            if type(tiles[x][y][0]) == Resource:
                robot.pickup_resource(tiles[x][y][0])

        # Drop Markers
        newMarker = None
        markerColor = None
        if marker == Actions.DROP_RED:
            newMarker = Marker(x, y, MarkerType.RED)
            markerColor = "RED"
        elif marker == Actions.DROP_YELLOW:
            newMarker = Marker(x, y, MarkerType.YELLOW)
            markerColor = "YELLOW"
        elif marker == Actions.DROP_GREEN:
            newMarker = Marker(x, y, MarkerType.GREEN)
            markerColor = "GREEN"
        elif marker == Actions.DROP_BLUE:
            newMarker = Marker(x, y, MarkerType.BLUE)
            markerColor = "BLUE"
        elif marker == Actions.DROP_ORANGE:
            newMarker = Marker(x, y, MarkerType.ORANGE)
            markerColor = "ORANGE"
    
        if(newMarker):
            alreadyPlaced = False
            for placed_marker in tiles[x][y][2]:
                if(str(placed_marker) == markerColor):
                    alreadyPlaced = True
            if(not alreadyPlaced):
                tiles[x][y][2].append(newMarker)
                self.__markers.append(newMarker)
                MarkerLocations.append([markerColor,[x,y]])
                

    def get_view(self, robot):
        tiles = self.__tiles
        (y,x) = robot.get_loc()
        length = robot.get_fov()//2
        (xMin, yMin) = (max(0, x-length), max(0, y-length))
        (xMax, yMax) = (min(self.__length, x+length+1), min(self.__length, y+length+1))
        xDiff = 0
        yDiff = 0
        atMinX = 0
        atMinY = 0
        if(xMax - xMin != 2 * length + 1):
            xDiff = 2 * length + 1 - (xMax - xMin)
            if(xMin == 0):
                atMinX = 1
        if(yMax - yMin != 2 * length + 1):
            yDiff = 2 * length + 1 - (yMax - yMin)
            if(yMin == 0):
                atMinY = 1
        view = []
        Mount = [Mountain() , 0, []]
        if(atMinY):
            for _ in range(yDiff):
                view.append([Mount for i in range(2 * length + 1)])
        for i in range(yMin, yMax):
            view.append([])
            if(atMinX):
                for _ in range(xDiff):
                    view[-1].append(Mount)
            for j in range(xMin, xMax):
                tile = tiles[i][j]
                view[-1].append((copy.deepcopy(tile[0]),tile[1],copy.deepcopy(tile[2])))
            if(not atMinX):
                for _ in range(xDiff):
                    view[-1].append(Mount)
        if(not atMinY):
            for _ in range(yDiff):
                view.append([Mount for i in range(2 * length + 1)])
        return view

    def display(self):
        for row in range(self.__length):
            string = ''
            for col in range(self.__length):
                string += str(self.__tiles[row][col])
            print (string)

    def get_list(self):
        boardArray = []
        for row in range(self.__length):
            boardArray.append([])
            for col in range(self.__length):
                tile = self.__tiles[row][col]
                if tile[1] > 0:
                    boardArray[row].append("Robot")
                elif len(tile[2]) > 0:
                    boardArray[row].append(str(tile[2][0]))
                else:
                    boardArray[row].append(str(tile[0]))
        return boardArray

    def get_elements(self, first = False):
        global ResourceDepletions
        #find unique locations of robots
        robotStr = [str(robot.get_loc()) for robot in self.__robots]
        robots = []
        for robotLoc in robotStr:
            dims = robotLoc.split(',')
            robots.append([dims[0][1:],dims[1][1:-1]])
        #copy over locations of the depleted resources
        locations = copy.deepcopy(ResourceDepletions)
        #clear list of depleted resources
        ResourceDepletions[:] = []

        markers = copy.deepcopy(MarkerLocations)
        MarkerLocations[:] = []

        returnVal = {'robots' : robots, 'markers' : markers, 'locations' : locations}
        return returnVal


    def get_score(self):
        return self.__bank.get_value()