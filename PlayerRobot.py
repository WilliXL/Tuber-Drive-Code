from robot import Robot
from constants import Actions, TileType
from tile import Tile, Plains, Resource, Base, Marker, Mountain
import random
import time

##########################################################################
# One of your team members, Chris Hung, has made a starter bot for you.  #
# Unfortunately, he is busy on vacation so he is unable to aid you with  #
# the development of this bot.                                           #
#                                                                        #
# Make sure to read the README for the documentation he left you         #
#                                                                        #
# @authors: christoh, [TEAM_MEMBER_1], [TEAM_MEMBER_2], [TEAM_MEMBER_3]  #
# @version: 2/4/17                                                       #
#                                                                        #
# README - Introduction                                                  #
#                                                                        #
# Search the README with these titles to see the descriptions.           #
##########################################################################

# !!!!! Make your changes within here !!!!!
class player_robot(Robot):
    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        ##############################################
        # A couple of variables - read what they do! # 
        #                                            #
        # README - My_Robot                          #
        ##############################################
        self.toHome = []      
        self.toFlag = []    
        self.toFlag2 = []   
        self.numturns = 0
        
    
        self.placingFlag = 0
        self.flagToHome = 1   
        self.homeToFlag = 2
        self.resourceToFlag = 3
        self.flagToResource = 4
        self.mining = 5
        
        self.state = self.placingFlag;
         
        
        
        self.targetPath = None;
        self.targetDest = (0,0)
        
        self.density1 = 1
        self.density2 = 150
        
        self.flagPos = None
        self.position = [0,0]

        
        # self.defaultAction = self.FindRandomPath(view)

    # A couple of helper functions (Implemented at the bottom)
    def OppositeDir(self, direction):
        return # See below

    def ViewScan(self, view):
        return # See below

    def FindRandomPath(self, view):
        return # See below

    def UpdateTargetPath(self):
        return # See below

    ###########################################################################################
    # This function is called every iteration. This method receives the current robot's view  #
    # and returns a tuple of (move_action, marker_action).                                    #
    #                                                                                         #
    # README - Get_Move                                                                       #
    ###########################################################################################
    def get_move(self, view):
        markerDrop = Actions.DROP_NONE
        actionToTake = None
        
        print("State: ", self.state)
        print("To Flag: ", self.toFlag)
        
        totalResource=self.getTotalResources(view)
        #print("Resource in View: ", totalResource)
        if self.state == self.placingFlag:
            if(actionToTake != None):
                self.toHome.append(actionToTake)
            #Put random direction here
            actionToTake = self.FindRandomPath(view)
            if (totalResource > 0) and not self.isFlag(view):
                markerDrop = Actions.DROP_GREEN
                self.flagPos = self.position
                self.toFlag.append(actionToTake)
                self.state = self.flagToResource;
                self.ViewScan(view); #Run thisoncetostart flagto resource
        
        
        if self.state == self.flagToResource:
            if(self.targetPath != [] and self.targetPath != None):
                actionToTake = self.UpdateTargetPath()
                self.toFlag.append(actionToTake);
            else:
                self.state = self.mining;
                
                
        
        if self.state == self.mining:
            if(self.storage_remaining() == 0):
                print("FULL!")
                self.state = self.resourceToFlag
            elif(self.amountOfResourceAtPosition(view) == 0):
                self.state = self.resourceToFlag
                print("RESOURCE DEPLETED, GOING TO FLAG");
            else:
                actionToTake = Actions.MINE
                
                
        if self.state == self.flagToHome:
            print(self.toHome)
            if(self.toHome == []):
                self.state = self.homeToFlag
                return (Actions.DROPOFF,Actions.DROP_NONE)
               
            else:
                # Trace your steps back home
                prevAction = self.toHome.pop()
                revAction = self.OppositeDir(prevAction)
                assert(isinstance(revAction, int))
                #return (revAction, Actions.DROP_NONE)
                actionToTake = revAction   
                
                
        if self.state == self.resourceToFlag:
            
            if(self.toFlag == []):
                if(self.storage_remaining() == 0):
                    self.state = self.flagToHome
                    self.toFlag2 = self.toHome
                else:
                    print("Available Resources:",self.getTotalResources(view))
                    if (self.getTotalResources(view) > 0):
                        self.ViewScan(view)
                        print(self.targetPath)
                        actionToTake = self.UpdateTargetPath()
                        self.state = self.flagToResource
                    else:
                        markerDrop = Actions.DROP_RED
                        self.state = self.placingFlag
                        actionToTake = self.FindRandomPath(view)
                        
            else:
                prevAction = self.toFlag.pop()
                print(self.toFlag)
                revAction = self.OppositeDir(prevAction)
                #return (revAction, Actions.DROP_NONE)
                actionToTake = revAction
        
        if self.state == self.homeToFlag:
            if(self.toFlag2 == []):
                self.state = self.flagToResource
            else:
                prevAction = self.toFlag2.pop()
                print(self.toFlag)
                actionToTake = prevAction
        
            
        
            


        viewLen = len(view)
        score = 0
        # Run BFS to find closest resource

        # Search for resources
        # Updates self.targetPath, sefl.targetDest
        
        
        # If you can't find any resources...go in a random direction!
        # actionToTake = None
        # if(self.targetPath == None):
        #     actionToTake = self.FindRandomPath(view)

        # Congrats! You have found a resource
        # print("TP: ", self.targetPath)
        # if(self.targetPath == []):
        #     return (Actions.MINE, Actions.DROP_NONE)
        # else:
        #     # Use the first coordinate on the path as the destination , and action to move
        #     actionToTake = self.UpdateTargetPath()
            
        self.updatePosition(actionToTake)
        
        if self.targetPath == []:
            self.targetPath = None
        
        
        print("Action:", actionToTake)
        #print("Marker:", markerDrop)
        print()
        return (actionToTake, markerDrop)
        
    def getTotalResources(self,view):
        resourceTotal = 0
        for i in range(5):
            for j in range(5):
               currentTile = view[i][j][0]
               if(type(currentTile) == Resource):
                   resourceTotal += currentTile.AmountRemaining()
        return resourceTotal
        
    def isFlag(self,view):
        for i in range(5):
            for j in range(5):
               currentFlag = view[i][j][2];
               if(currentFlag != [] and (self.flagPos[0],self.flagPos[1]) != (self.position[0] - 2 + i,self.position[1] - 2 + j) ):
                   print(view[i][j][2])
                   return True
        return False
        
    def amountOfResourceAtPosition(self,view):
        robotTile = view[2][2][0]
        if(type(robotTile) == Resource):
            return(robotTile.AmountRemaining())
        return 0
                    
                
    
    def updatePosition(self,actionToTake):
        if(actionToTake == Actions.MOVE_N):
            self.position[0] += 0;
            self.position[1] += 1;
        elif(actionToTake == Actions.MOVE_NE):
            self.position[0]  += 1;
            self.position[1]  += 1;
        elif(actionToTake == Actions.MOVE_E):
            self.position[0]  += 1;
            self.position[1]  += 0;
        elif(actionToTake == Actions.MOVE_SE):
            self.position[0]  += 1;
            self.position[1]  -= 1;
        elif(actionToTake == Actions.MOVE_S):
            self.position[0]  += 0;
            self.position[1]  -= 1;
        elif(actionToTake == Actions.MOVE_SW):
            self.position[0]  -= 1;
            self.position[1]  -= 1;
        elif(actionToTake == Actions.MOVE_W):
            self.position[0]  -= 1;
            self.position[1]  += 0;
        elif(actionToTake == Actions.MOVE_NW):
            self.position[0]  -= 1;
            self.position[1]  += 1;
    
    # Returns opposite direction
    def OppositeDir(self, prevAction):
        if(prevAction == Actions.MOVE_N):
            return Actions.MOVE_S
        elif(prevAction == Actions.MOVE_NE):
            return Actions.MOVE_SW
        elif(prevAction == Actions.MOVE_E):
            return Actions.MOVE_W
        elif(prevAction == Actions.MOVE_SE):
            return Actions.MOVE_NW
        elif(prevAction == Actions.MOVE_S):
            return Actions.MOVE_N
        elif(prevAction == Actions.MOVE_SW):
            return Actions.MOVE_NE
        elif(prevAction == Actions.MOVE_W):
            return Actions.MOVE_E
        elif(prevAction == Actions.MOVE_NW):
            return Actions.MOVE_SE
        else:
            return Actions.MOVE_S

    # Scans the entire view for resource searching
    # REQUIRES: view (see call location)
    def ViewScan(self, view):
        viewLen = len(view)
        queue = [[(0,0)]]
        deltas = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        visited = set()
        visited.add((0,0))

        targetDepleted = (view[self.targetDest[0]][self.targetDest[1]][0].GetType() == TileType.Resource and
                         view[self.targetDest[0]][self.targetDest[1]][0].AmountRemaining() <= 0)

        # BFS TO find the next resource within your view
        if(self.targetPath == None or targetDepleted):
            while(len(queue)>0):
                path = queue[0]
                loc = path[0]
                queue = queue[1:]
                viewIndex = (loc[0] + viewLen//2,loc[1]+viewLen//2)
                if (view[viewIndex[0]][viewIndex[1]][0].GetType() == TileType.Resource and
                    view[viewIndex[0]][viewIndex[1]][0].AmountRemaining() > 0):
                    # print(path)
                    self.targetPath = path[1:]
                    self.targetDest = path[0]
                    return
                elif(view[viewIndex[0]][viewIndex[1]][0].CanMove()):
                    for i in range(8):
                        x = loc[0] + deltas[i][0]
                        y = loc[1] + deltas[i][1]
                        if(abs(x) <= viewLen//2 and abs(y) <= viewLen//2):
                            if((x,y) not in visited):
                                queue.append([(x,y)] + path[1:] + [deltas[i]])
                                visited.add((x,y))

        return

    # Picks a random move based on the view - don't crash into mountains!
    # REQUIRES: view (see call location)
    def FindRandomPath(self, view):
        viewLen = len(view)

        while(True):
            actionToTake = random.choice([Actions.MOVE_E,Actions.MOVE_N,
                                          Actions.MOVE_S,Actions.MOVE_W,
                                          Actions.MOVE_NW,Actions.MOVE_NE,
                                          Actions.MOVE_SW,Actions.MOVE_SE])
            if ((actionToTake == Actions.MOVE_N and view[viewLen//2-1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_S and view[viewLen//2+1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_E and view[viewLen//2][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_W and view[viewLen//2][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NW and view[viewLen//2-1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NE and view[viewLen//2-1][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SW and view[viewLen//2+1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SE and view[viewLen//2+1][viewLen//2+1][0].CanMove()) ):
               return actionToTake

        return None

    # Returns actionToTake
    # REQUIRES: self.targetPath != []
    def UpdateTargetPath(self):
        actionToTake = None
        (x, y) = self.targetPath[0]

        if(self.targetPath[0] == (1,0)):
            actionToTake = Actions.MOVE_S
        elif(self.targetPath[0] == (1,1)):
            actionToTake = Actions.MOVE_SE
        elif(self.targetPath[0] == (0,1)):
            actionToTake = Actions.MOVE_E
        elif(self.targetPath[0] == (-1,1)):
            actionToTake = Actions.MOVE_NE
        elif(self.targetPath[0] == (-1,0)):
            actionToTake = Actions.MOVE_N
        elif(self.targetPath[0] == (-1,-1)):
            actionToTake = Actions.MOVE_NW
        elif(self.targetPath[0] == (0,-1)):
            actionToTake = Actions.MOVE_W
        elif(self.targetPath[0] == (1,-1)):
            actionToTake = Actions.MOVE_SW

        # Update destination using path
        self.targetDest = (self.targetDest[0]-x, self.targetDest[1]-y)
        # We will continue along our path    
        self.targetPath = self.targetPath[1:]

        return actionToTake

