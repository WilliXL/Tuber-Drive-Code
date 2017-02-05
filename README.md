# 15097-s17

################################################################################
# 1) INTRODUCTION
#
# Do not make any API calls not listed below
# The following API is available from the Robot Class
# self.get_fov()                     - \return(int): Range of vision that robot can see. Vision/2 to the left and Vision/2 to the right.
# self.get_max_capacity()            - \return(int): Max amount of resources that the robot can hold.
# self.get_pickup_amount()           - \return(int): Amount of resources the robot can pick up every turn
# self.held_value()                  - \return(int): Value of resources currently held
# self.storage_remaining()           - \return(int): Amount of resources the robot can still pick up
# self.get_turn()                    - \return(int): Current turn number

# The following API is available from the Tile Class
# Tile.CanMove()                     - \return(bool): Determines whether or not robot is able to move to that tile
# Tile.GetType()                     - \return(TileType): Enum in constants.py that determines what type of tile it is

# The following API is available from the Resource Class, subclass of Tile
# Resource.Value()                   - \return(int): Value of 1 unit of resource
# Resource.AmountRemaining()         - \return(int): Number of units of resource remaining

# The following API is available from the Marker Class
# Marker.GetColor()                  - \return(MarkerType): Enum in constants.py that determines color of marker

# 2) My_Robot 
#
# self.toHome = []                   - Where your base is    
# self.numturns = 0                  - Number of turns, don't run out of time!
# self.goinghome = False;            - State of the robot
# self.targetPath = None             - How to get where you want
# self.targetDest = (0,0)            - Where you are going!


# 3) Get_Move
#
# This method is called every iteration to determine what action to take
# \param view = A nxnx3 array of the board centered on the robot
#    - view[x][y][0] = Tile object for location (x,y)
#    - view[x][y][1] = Number of robots at position (x,y)
#    - view[x][y][2] = List of Marker objects at location (x,y)
#    - x = [0, Vision], y = [0, Vision]
#    - RobotLocation = (Vision/2, Vision/2) - Note: This is a relative location
# This function needs to return a tuple ({Action}, {Marker, None}) where
# {Action} is one of the actions defined in constants.py, and {Marker, None} is
# one of the markers defined in constants.py or None
# e.g. Returning (Actions.MOVE_N, Actions.DROP_RED) means an action of moving North and dropping a red marker
# e.g. Returning (Actions.MINE, Actions.DROP_NONE) means an action of mining a resource and not dropping a marker
################################################################################
