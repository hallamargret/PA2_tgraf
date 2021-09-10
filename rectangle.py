from OpenGL.GL import *
from OpenGL.GLU import *

from point import Point

class Rectangle:
    def __init__(self, startPoint, endPoint): # Finna eitthvad annad ord fyrir extra!! 
        self.height = abs(startPoint.y - endPoint.y)
        self.width = abs(startPoint.x - endPoint.x)
        self.middle = Point(((startPoint.x + endPoint.x)/2), ((startPoint.y + endPoint.y)/2))
        self.lb = Point(self.middle.x - self.width/2, self.middle.y - self.height/2)
        self.rb = Point(self.middle.x + self.width/2, self.middle.y - self.height/2)
        self.lt = Point(self.middle.x - self.width/2, self.middle.y + self.height/2)
        self.rt = Point(self.middle.x + self.width/2, self.middle.y + self.height/2)

    def draw(self):
        glBegin(GL_TRIANGLES)
        glVertex2f(self.lb.x, self.lb.y)
        glVertex2f(self.lt.x, self.lt.y)
        glVertex2f(self.rb.x, self.rb.y)
        glVertex2f(self.lt.x, self.lt.y)
        glVertex2f(self.rb.x, self.rb.y)
        glVertex2f(self.rt.x, self.rt.y)
        glEnd()