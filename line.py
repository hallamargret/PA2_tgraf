from OpenGL.GL import *
from OpenGL.GLU import *

from point import Point
from vector import Vector

from math import *

class Line:
    def __init__(self, startPoint, endPoint):
        self.length = sqrt(((startPoint.x - endPoint.x)**2) + ((startPoint.y - endPoint.y)**2))
        self.start = startPoint
        self.end = endPoint
        self.normal = Vector(-(startPoint.y - endPoint.y), startPoint.x - endPoint.x)

    def draw(self):
        glBegin(GL_LINES)
        glVertex2f(self.start.x, self.start.y)
        glVertex2f(self.end.x, self.end.y)
        glEnd()