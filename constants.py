class Actions:
    #Movement
    MOVE_N = 0
    MOVE_E = 1
    MOVE_S = 2
    MOVE_W = 3
    MOVE_NW = 4
    MOVE_NE = 5
    MOVE_SW = 6
    MOVE_SE = 7

    #Widget Manipulation
    DROPOFF = 11
    MINE = 13

    #Marker Drops
    DROP_RED = 14
    DROP_YELLOW = 15
    DROP_GREEN = 16
    DROP_BLUE = 17
    DROP_ORANGE = 18
    DROP_NONE = 19

class MarkerType:
    RED = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3
    ORANGE = 4

class SetupConstants:
    BOARD_DIM = 100
    XLOC = 50
    YLOC = 50

    NUM_ROBOTS = 50
    NUM_TURNS = 1000
    DEFAULTVISION = 5
    DEFAULTSTORAGE = 50
    DEFAULTPICKUPRATE = 1

class TileType:
    Plains = 0
    Mountain = 1
    Marker = 2
    Resource = 3
    Base = 4
