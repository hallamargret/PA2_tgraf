from OpenGL.GL import *
from OpenGL.GLU import *

from ball import Ball

class BallObject:
    def __init__(self, radius, position, motion, r, g, b):
        self.position = position
        self.radius = radius
        self.motion = motion
        self.red = r
        self.green = g
        self.blue = b
        self.ball = Ball(24, r, g, b)
        self.fired = False

    def display_object(self):
        glPushMatrix()
        glColor3f(self.red, self.green, self.blue)

        glTranslate(self.position.x, self.position.y, 0)
        glScale(self.radius, self.radius, 1)

        self.ball.display()
        glPopMatrix()