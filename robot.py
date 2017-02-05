from constants import Actions
import random
from globalVars import ResourceDepletions


class Robot(object):
    __vision = 2
    __storage_capacity = 10
    __max_capacity = 10
    __pickup_amount = 1
    __held_value = 0
    __x_loc = 0
    __y_loc = 0

    #Args = [vision_range, storage_capacity, pickup_amount, x, y]
    # Done to obscure constructor arguments from users
    def __init__(self, args):
        self.__vision = args[0]
        self.__storage_capacity = args[1]
        self.__max_capacity = args[1]
        self.__pickup_amount = args[2]
        self.__x_loc = args[3]
        self.__y_loc = args[4]
        self.__turn = 0

    def get_fov(self):
        return self.__vision

    def set_loc(self, x,y):
        self.__x_loc = x
        self.__y_loc = y

    def get_loc(self):
        return (self.__x_loc, self.__y_loc)

    def get_max_capacity(self):
        return self.__max_capacity

    def get_pickup_amount(self):
        return self.__pickup_amount

    def pickup_resource(self, tile):
        global ResourceDepletions
        amount_to_pickup = min(self.__pickup_amount, self.__storage_capacity)
        amount_actually_picked_up = tile.Action(amount_to_pickup)
        if tile.IsDepleted():
            tile.ConfirmDeplete()
            ResourceDepletions.append([self.get_loc()[0],self.get_loc()[1],tile.Value()])
        self.__held_value += amount_actually_picked_up * tile.Value()
        self.__storage_capacity -= amount_actually_picked_up


    def drop_resource(self, bank):
        bank.deposit(self.__held_value)
        self.__held_value = 0
        self.__storage_capacity = self.__max_capacity

    def held_value(self):
        return self.__held_value

    def storage_remaining(self):
        return self.__storage_capacity

    def get_turn(self):
        return self.__turn

    def set_turn(self, turn):
        self.__turn = turn

    def __repr__(self):
        return "R[%d,%d]" % (self.get_loc())

    def __str__(self):
        return "R[%d,%d]" % (self.get_loc())

## TODO: Move to own class
class Bank:
    __value = 0

    def __init__(self):
        return

    def get_value(self):
        return self.__value

    def deposit(self, amount):
        self.__value += amount

    def withdraw(self, amount):
        self.__value -= amount

        
