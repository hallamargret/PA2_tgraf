from math import *

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Point(new_x, new_y)
    
    def __sub__(self, other):
        new_x = self.x - other.x
        new_y = self.y - other.y
        return Point(new_x, new_y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
    
    def distance(self, other):
        return sqrt(((self.x - other.x)**2) + ((self.y - other.y)**2))