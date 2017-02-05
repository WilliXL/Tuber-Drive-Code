from robot import Robot
from robot import Bank
from board import Board
from PlayerRobot import player_robot
import tile
from constants import Actions, SetupConstants
import random
import json
import time
from globalVars import ResourceDepletions
import threading
import sys

BOARD_DIM = SetupConstants.BOARD_DIM
NUM_ROBOTS = SetupConstants.NUM_ROBOTS
NUM_TURNS = SetupConstants.NUM_TURNS
XLOC = SetupConstants.XLOC
YLOC = SetupConstants.YLOC

def generate_board():
    board = []
    DEFAULT_AMOUNT = 20
    obstacles = []
    for row in range(BOARD_DIM):
        board.append([])
        for col in range(BOARD_DIM):
            if col % 2 == 1 and random.randint(0,3) == 1:
                board[row].append([tile.Resource(1,DEFAULT_AMOUNT),0,[]])
                ResourceDepletions.append([row,col,1])
            elif (col % 2 == 0 and random.randint(0,5) == 1):
                board[row].append([tile.Mountain(),0,[]])
                obstacles.append([row,col])
            else:
                board[row].append([tile.Plains(),0,[]])
    board[XLOC][YLOC] = [tile.Base(),NUM_ROBOTS,[]]


    return (board, obstacles)

def make_board():
    with open(sys.argv[1]) as map1:
        locs = json.load(map1)
    length = locs["map_size"][0]
    board = [[[tile.Plains(),0,[]] for i in range(length)] for i in range(length)]
    for widget in locs["widgets"]:
        board[widget[0]][widget[1]] = [tile.Resource(widget[2],widget[3]),0,[]]
        ResourceDepletions.append([widget[0],widget[1],widget[2]])
    for obstacle in locs["obstacles"]:
        board[obstacle[0]][obstacle[1]] = [tile.Mountain(),0,[]]
    board[length//2][length//2] = [tile.Base(),NUM_ROBOTS,[]]
    return (board, locs["obstacles"], length)


def main():
    #instantiate robots
    game = []
    defaultVision = SetupConstants.DEFAULTVISION
    defaultStorage = SetupConstants.DEFAULTSTORAGE
    defaultPickupRate = SetupConstants.DEFAULTPICKUPRATE

    if(len(sys.argv) > 1):
        (board,obstacles,length) = make_board()
        game += [length, [length//2,length//2]]
        robotX = length//2
        robotY = length//2
    else:
        (board,obstacles) = generate_board()
        game += [BOARD_DIM, [XLOC,YLOC]]
        robotX = XLOC
        robotY = YLOC

    args = [defaultVision, defaultStorage, defaultPickupRate, robotX, robotY]
    robots = []
    for i in range(NUM_ROBOTS):
        robots.append(player_robot(args))

    board = Board(board, robots, Bank())

    game.append(obstacles)
    game.append((board.get_elements(True), board.get_score()))

    gameThread = threading.Thread(None,lambda:run_game(game, robots, board))
    gameThread.daemon = True
    gameThread.start()
    gameThread.join(300)
    if(gameThread.isAlive()):
        print("Your robot timed out")
    with open("visual/map.txt", 'w') as gameFile:
        json.dump(game, gameFile)
    print (board.get_score())


def run_game(game, robots, board):
    for i in range(NUM_TURNS):
        for robot in robots:
            robot.set_turn(i)
            view = board.get_view(robot)
            try:
                move = robot.get_move(view)
                board.make_move(robot, move)
            except KeyboardInterrupt:
                with open("visual/map.txt", 'w') as gameFile:
                    json.dump(game, gameFile)
                    print (board.get_score())
                exit()
        game.append((board.get_elements(), board.get_score()))
#         board.display()
#         print

main()
