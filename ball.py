from math import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Ball:
    def __init__(self, slices, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.angle_change = (pi * 2)/slices

    def display(self):
        glColor3f(self.r, self.g, self.b)
        glBegin(GL_TRIANGLE_FAN)
        tmp_angle = 0
        while tmp_angle < 2 * pi:
            x = cos(tmp_angle)
            y = sin(tmp_angle)
            glVertex2f(x, y)
            tmp_angle += self.angle_change
        glEnd()