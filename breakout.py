import pygame
from pygame import key
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random
from random import *

import math
from math import *

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

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



WIDTH = 800
HEIGTH = 600

class VectorMotion:

    def __init__(self):
        pygame.display.init()
        pygame.display.set_mode((WIDTH, HEIGTH), DOUBLEBUF|OPENGL)
        glClearColor(0.2, 0.5, 0.4, 0.2)

        middle = WIDTH/2

        self.cannon_direction = Vector(0,1)
        self.cannon_point = Point(int(middle), 0)


        self.ball_position = Point((WIDTH/2), 100)
        self.ball_motion = Vector(0, 0)

        self.cannonball = BallObject(10, self.ball_position, self.ball_motion, 1.0, 1.0, 1.0)

        self.clock = pygame.time.Clock()
        self.angle = - 45
        self.speed = 20

        self.goal_large = BallObject(40, Point(WIDTH/2, 480), Vector(0,0), 0.0, 1.0, 0.0)
        self.goal_small = BallObject(30, Point(WIDTH/2, 480), Vector(0,0), 0.0, 0.8, 0.0)

        #self.cannon_direction.x = self.speed * cos(self.angle * 3.1415/180.0)
        #self.cannon_direction.y = self.speed * sin(self.angle * 3.1415/180.0)


    def update(self):
        delta_time = self.clock.tick() / 1000


        pressed = pygame.key.get_pressed()
        #if pressed[pygame.K_UP]:
            #self.motion.y += 15 * delta_time
        #if pressed[pygame.K_DOWN]:
            #self.motion.y -= 15 * delta_time
        #if pressed[pygame.K_LEFT]:
            #self.motion.x -= 15 * delta_time
        #if pressed[pygame.K_RIGHT]:
            #self.motion.x += 15 * delta_time
        if pressed[pygame.K_LEFT]:
            if self.angle < 45:
                self.angle += 180 * delta_time
        if pressed[pygame.K_RIGHT]:
            if self.angle > -45:
                self.angle -= 180 * delta_time
        
        self.cannon_direction.x = self.speed * -sin(self.angle * 3.1415/180.0)
        self.cannon_direction.y = self.speed * cos(self.angle * 3.1415/180.0)

        if self.cannonball.position.x < 0 or self.cannonball.position.x > WIDTH:
            self.cannonball.fired = False
        elif self.cannonball.position.y < 0 or self.cannonball.position.y > HEIGTH:
            self.cannonball.fired = False

        self.cannonball.position.x += self.cannonball.motion.x
        self.cannonball.position.y += self.cannonball.motion.y





    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(0, 0, WIDTH, HEIGTH)
        gluOrtho2D(0, WIDTH, 0, HEIGTH)

        glColor3f(1.0, 0.7, 0.0)
        glBegin(GL_LINES)
        glVertex2f(0, 100)
        glVertex2f((WIDTH/6)*2, 100)
        glVertex2f(WIDTH, 100)
        glVertex2f(WIDTH - (WIDTH/6)*2, 100)
        glEnd()

        glPushMatrix()
    
        self.goal_large.display_object()
        self.goal_small.display_object()

        if self.cannonball.fired == True:
            self.cannonball.display_object()

        glPopMatrix()

        glPushMatrix()
        


        glTranslate(self.cannon_point.x, self.cannon_point.y, 0)
        glRotate(self.angle, 0, 0, 1)

        glColor3f(1.0, 0.7, 0.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(0 - 15, 0 - 100)
        glVertex2f(0 - 15, 0 + 100)
        glVertex2f(0 + 15, 0 - 100)
        glVertex2f(0 - 15, 0 + 100)
        glVertex2f(0 + 15, 0 - 100)
        glVertex2f(0 + 15, 0 + 100)
        glEnd()

        glPopMatrix()

        

        pygame.display.flip()
    
    def fire_ball(self):
        self.cannonball.fired = True
        self.cannonball.motion.x = self.cannon_direction.x/30
        self.cannonball.motion.y = self.cannon_direction.y/30
        self.cannonball.position.x = (WIDTH/2) + self.cannon_direction.x
        self.cannonball.position.y = self.cannon_direction.y


    def game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == K_q:
                    glClearColor(random(), random(), random(), 1.0)
                elif event.key == K_SPACE or event.key == K_z:
                    if self.cannonball.fired == False:
                        self.fire_ball()
                
        self.update()
        self.display()

if __name__ == "__main__":
    game = VectorMotion()
    while True:
        game.game_loop()