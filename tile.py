from abc import ABCMeta, abstractmethod
from constants import MarkerType, TileType

# I do not know how abstract classes work in python, so I think this class is instantiable.
# Do NOT instantiate this. Only instantiate subclasses of 'Tile'

class Tile:
    __metaclass__ = ABCMeta
    __walkable = False;

    # How the robot can interact with the tile
    @abstractmethod
    def Action(robot):
        pass

    # How the tile affects the robot
    @abstractmethod
    def Effect(robot):
        pass

    # Determines if robots can move to this tile
    @abstractmethod
    def CanMove(self):
        pass

    # Type of Tile
    @abstractmethod
    def GetType(self):
        pass


class Plains(Tile) :
    def __init__(self):
        self.__walkable = True;

    def CanMove(self):
        return self.__walkable;

    def GetType(self):
        return TileType.Plains;

    def Action(self):
        pass

    def Effect(self):
        pass

    def __str__(self):
         return "P   "

    def __repr__(self):
         return "P   "

## Mountains are walkable with reduced speed, but no actions can be performed
class Mountain(Tile) :
    def __init__(self):
        self.__walkable = False;

    def CanMove(self):
        return self.__walkable;

    def GetType(self):
        return TileType.Mountain;

    def Action(self):
        pass

    def Effect(self):
        pass

    def __str__(self):
        return "M   "

    def __repr__(self):
        return "M   "


### TODO: Move to its own file
class Resource(Tile) :
    __value = 1;
    __amount = 1;
    __walkable = True
    __justDepleted = False

    def __init__(self, value, amount):
        self.__value = value;
        self.__amount = amount;

    def Action(self, amount):
        amountPickedUp = min(self.__amount, amount);
        self.__amount -= amountPickedUp;
        if self.__amount == 0 and amountPickedUp > 0: self.__justDepleted = True
        return amountPickedUp;

    def CanMove(self):
        return self.__walkable;

    def GetType(self):
        return TileType.Resource;

    def Value(self):
        return self.__value;

    def AmountRemaining(self):
        return self.__amount;

    def Effect(self, robot):
        return;

    def ConfirmDeplete(self):
        self.__justDepleted = False

    def IsDepleted(self):
        return self.__justDepleted

    def __str__(self):
        if self.__amount > 0:
            return "R   "
        else:
            return "P   "
        return "R(" + str(self.__amount) + ")"

    def __repr__(self):
        return "R   "
        return "R(" + str(self.__amount) + ")"

class Base(Tile) :
    __xLoc = 0;
    __yLoc = 0;

    def __init__(self):
        self.__walkable = True;
        return

    def Action(self, robot):
        pass

    def Effect(self, robot):
        pass

    def CanMove(self):
        return self.__walkable;

    def GetType(self):
        return TileType.Base;

    def UpgradeRobotVision(self, robot, bank):
        cost = robot.GetVisionUpgradeCost();
        if(bank.GetValue() >= cost):
            robot.UpgradeVision();
            bank.Withdraw(cost);
    def UpgradeRobotStorage(self, robot, bank):
        cost = robot.GetStorageUpgradeCost();
        if(bank.GetValue() >= cost):
            robot.UpgradeVision();
            bank.Withdraw(cost);
    def UpgradeRobotRate(self, robot, bank):
        cost = robot.GetRateUpgradeCost();
        if(bank.GetValue() >= cost):
            robot.UpgradeVision();
            bank.Withdraw(cost);

    def DropResources(self, robot, bank):
        robot.DropResource(bank);

    def __str__(self):
        return "B   "

    def __repr__(self):
        return "B   "

class Marker(Tile) :
    __xLoc = 0
    __yLoc = 0
    __type = 0
    __walkable = True

    def __init__(self, x, y, color):
        self.__xLoc = x
        self.__yLoc = y
        self.__type = color
        return
    def GetType(self):
        return self.__type

    def GetTurns(self):
        return self.__numTurns
    
    def GetColor(self):
        return self.__type

    def GetLoc(self):
        return (self.__xLoc, self.__yLoc)
    
    def Action(self, robot):
        pass

    def Effect(self, robot):
        pass

    def CanMove(self):
        return self.__walkable;
    
    def __str__(self):
        if self.__type == MarkerType.RED:
            return "RED"
        elif self.__type == MarkerType.YELLOW:
            return "YELLOW"
        elif self.__type == MarkerType.GREEN:
            return "GREEN"
        elif self.__type == MarkerType.BLUE:
            return "BLUE"
        elif self.__type == MarkerType.ORANGE:
            return "ORANGE"
        else:
            return "UNKNOWN"
        
    def __repr__(self):
        if self.__type == MarkerType.RED:
            return "RED"
        elif self.__type == MarkerType.YELLOW:
            return "YELLOW"
        elif self.__type == MarkerType.GREEN:
            return "GREEN"
        elif self.__type == MarkerType.BLUE:
            return "BLUE"
        elif self.__type == MarkerType.ORANGE:
            return "ORANGE"
        else:
            return "UNKNOWN"