import pygame
from pygame import key
from pygame import rect
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
    
    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)
    
    def __sub__(self, other):
        new_x = self.x - other.x
        new_y = self.y - other.y
        return Vector(new_x, new_y)

    def dot_product(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

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
    
    def distance(self, other):
        return sqrt(((self.x - other.x)**2) + ((self.y - other.y)**2))



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

class Rectangle:
    def __init__(self, x, y, height, width): # Finna eitthvad annad ord fyrir extra!! 
        self.x = x
        self.y = y
        self.lb = Point(x - width/2, y - height/2)
        self.rb = Point(x + width/2, y - height/2)
        self.lt = Point(x - width/2, y + height/2)
        self.rt = Point(x + width/2, y + height/2)
        self.hight = height
        self.width = width


WIDTH = 800
HEIGTH = 600

class CannonBallGame:

    def __init__(self):
        pygame.display.init()
        pygame.display.set_mode((WIDTH, HEIGTH), DOUBLEBUF|OPENGL)
        glClearColor(0.2, 0.5, 0.4, 0.2)

        middle = WIDTH/2

        #self.cannon_direction = Vector(0,1)
        self.cannon_point = Point(int(middle), 0)


        self.ball_position = Point(0, 0)
        self.ball_motion = Vector(1, 1)

        self.cannonball = BallObject(10, self.ball_position, self.ball_motion, 1.0, 1.0, 1.0)

        self.clock = pygame.time.Clock()
        self.angle = - 45
        self.speed = 200

        self.goal = Point(WIDTH/2, HEIGTH-100)

        self.rectangles = []
        self.delta_time = 0

        self.going_left = False
        self.going_right = False

        #self.cannon_direction.x = self.speed * cos(self.angle * 3.1415/180.0)
        #self.cannon_direction.y = self.speed * sin(self.angle * 3.1415/180.0)


    def update(self):
        self.delta_time = self.clock.tick(60) / 1000


        if self.going_left and self.angle < 45:
            self.angle += 180 * self.delta_time
        if self.going_right and self.angle > -45:
            self.angle -= 180 * self.delta_time

        # pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_LEFT]:
        #     if self.angle < 45:
        #         self.angle += 180 * self.delta_time
        # if pressed[pygame.K_RIGHT]:
        #     if self.angle > -45:
        #         self.angle -= 180 * self.delta_time
        
        #self.cannon_direction.x = 
        #self.cannon_direction.y = self.speed * cos(self.angle * 3.1415/180.0)

        if self.cannonball.fired == True:
            if self.cannonball.position.x < 0 or self.cannonball.position.x > WIDTH:
                self.cannonball.fired = False
            elif self.cannonball.position.y < 0 or self.cannonball.position.y > HEIGTH:
                self.cannonball.fired = False
            if (self.goal.x - 50) <= self.cannonball.position.x <= (self.goal.x + 50) and (self.goal.y - 50) <= self.cannonball.position.y <= (self.goal.y + 50):
                self.cannonball.fired = False
                print("Next level")


        self.cannonball.position.x += self.cannonball.motion.x * self.delta_time
        self.cannonball.position.y += self.cannonball.motion.y * self.delta_time
        
        if self.cannonball.fired == True:
            self.bounce_check()




    def bounce_check(self):
        for rectangle in self.rectangles:
            if self.cannonball.motion.x > 0: #left side of rectangle
                n = Vector(-(rectangle.lt - rectangle.lb).y, (rectangle.lt - rectangle.lb).x)
                thit = (n.dot_product(rectangle.lt - self.cannonball.position))/(n.dot_product(self.cannonball.motion))
                if 0 <= thit < (self.delta_time):
                    phit = self.cannonball.position + (self.cannonball.motion * thit)
                    print("checking if hits")
                    if (rectangle.lt.distance(phit) + rectangle.lb.distance(phit) == rectangle.lt.distance(rectangle.lb)):
                        print(rectangle.lt.distance(phit) + rectangle.lb.distance(phit) == rectangle.lt.distance(rectangle.lb))
                        new_motion = self.cannonball.motion - (Vector(-1, 0) *(2.0 * (self.cannonball.motion.dot_product(Vector(-1, 0)))))
                        print("it hits")
                        self.cannonball.position = phit
                        self.cannonball.motion = new_motion
            else: 
                n = Vector(-(rectangle.rt - rectangle.rb).y, (rectangle.rt - rectangle.rb).x)
                print("n: (" + str(n.x) + ", " + str(n.y) + ")")
                thit = (n.dot_product(rectangle.rt - self.cannonball.position))/(n.dot_product(self.cannonball.motion))
                if 0 <= thit < (self.delta_time):
                    phit = self.cannonball.position + (self.cannonball.motion * thit)
                    print("checking if hits")
                    if (rectangle.rt.distance(phit) + rectangle.rb.distance(phit) == rectangle.rt.distance(rectangle.rb)):
                        print(rectangle.rt.distance(phit) + rectangle.rb.distance(phit) == rectangle.rt.distance(rectangle.rb))
                        new_motion = self.cannonball.motion - (Vector(1, 0) *(2.0 * (self.cannonball.motion.dot_product(Vector(1, 0)))))
                        print("it hits")
                        self.cannonball.position = phit
                        self.cannonball.motion = new_motion
                        print("the motion: (" + str(self.cannonball.motion.x) + str(", ") + str(self.cannonball.motion.y))

            if self.cannonball.motion.y > 0: # bottom of rectangle
                n = Vector(-(rectangle.lb - rectangle.rb).y, (rectangle.lb - rectangle.rb).x)
                thit = (n.dot_product(rectangle.lb - self.cannonball.position))/(n.dot_product(self.cannonball.motion))
                if 0 <= thit < (self.delta_time):
                    phit = self.cannonball.position + (self.cannonball.motion * thit)
                    print("checking if hits")
                    if (rectangle.lb.distance(phit) + rectangle.rb.distance(phit) == rectangle.lb.distance(rectangle.rb)):
                        print(rectangle.lb.distance(phit) + rectangle.rb.distance(phit) == rectangle.lb.distance(rectangle.rb))
                        new_motion = self.cannonball.motion - (Vector(0, -1) *(2.0 * (self.cannonball.motion.dot_product(Vector(0, -1)))))
                        print("it hits")
                        self.cannonball.position = phit
                        self.cannonball.motion = new_motion
            else:
                n = Vector(-(rectangle.lt - rectangle.rt).y, (rectangle.lt - rectangle.rt).x)
                thit = (n.dot_product(rectangle.lt - self.cannonball.position))/(n.dot_product(self.cannonball.motion))
                if 0 <= thit < (self.delta_time):
                    phit = self.cannonball.position + (self.cannonball.motion * thit)
                    print("checking if hits")
                    if (rectangle.lt.distance(phit) + rectangle.rt.distance(phit) == rectangle.lt.distance(rectangle.rt)):
                        print(rectangle.lt.distance(phit) + rectangle.rt.distance(phit) == rectangle.lt.distance(rectangle.rt))
                        new_motion = self.cannonball.motion - (Vector(0, 1) *(2.0 * (self.cannonball.motion.dot_product(Vector(0, 1)))))
                        print("it hits")
                        self.cannonball.position = phit
                        self.cannonball.motion = new_motion
            
            # if self.cannonball.motion.y > 0:
            #     n = Vector(-((rectangle.y - 30) - (rectangle.y - 30)), (rectangle.x + 30) - (rectangle.x - 30))
            #     thit = (n.dot_product(Vector(((rectangle.x - 30) - self.cannonball.position.x), ((rectangle.y - 30) - self.cannonball.position.y))))/n.dot_product(self.cannonball.motion)
            #     print(thit)
                
    #     # Rulla i gegnum kassana i skjanum og gera bounce check


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


        if self.cannonball.fired == True:
            self.cannonball.display_object()


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

        glPushMatrix()
        glColor3f(0.0, 0.9, 0.0)
        glTranslate(self.goal.x, self.goal.y, 0)
        glBegin(GL_TRIANGLES)
        glVertex2f(0 - 50, 0 - 50)
        glVertex2f(0 - 50, 0 + 50)
        glVertex2f(0 + 50, 0 - 50)
        glVertex2f(0 - 50, 0 + 50)
        glVertex2f(0 + 50, 0 - 50)
        glVertex2f(0 + 50, 0 + 50)
        glEnd()
        glPopMatrix()

        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        for rectangle in self.rectangles:
            glBegin(GL_TRIANGLES)
            glVertex2f(rectangle.lb.x, rectangle.lb.y)
            glVertex2f(rectangle.lt.x, rectangle.lt.y)
            glVertex2f(rectangle.rb.x, rectangle.rb.y)
            glVertex2f(rectangle.lt.x, rectangle.lt.y)
            glVertex2f(rectangle.rb.x, rectangle.rb.y)
            glVertex2f(rectangle.rt.x, rectangle.rt.y)
            glEnd()
        glPopMatrix()

        pygame.display.flip()
    
    def fire_ball(self):
        self.cannonball.fired = True
        self.cannonball.motion.x = self.speed * -sin(self.angle * pi/180.0)
        self.cannonball.motion.y = self.speed * cos(self.angle * pi/180.0)
        self.cannonball.position.x = (WIDTH/2) + self.cannonball.motion.x * self.delta_time
        self.cannonball.position.y = self.cannonball.motion.y * self.delta_time

    def new_rectangle(self, position):
        new_rectangle = Rectangle(position[0], HEIGTH - position[1], 30, 50)
        if len(self.rectangles) == 0:
            self.rectangles.append(new_rectangle)
        else:
            counter = 0
            bool = True
            for rec in self.rectangles:
                counter += 1
                print("rec number: ", str(counter))
                if (abs(rec.x - new_rectangle.x) < (rec.width/2 + new_rectangle.width/2)) and (abs(rec.y - new_rectangle.y) < (rec.hight/2 + new_rectangle.hight/2)):
                    bool = False
                    
            if bool == True:
                self.rectangles.append(new_rectangle)




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
                elif event.key == K_LEFT:
                    self.going_left = True
                elif event.key == K_RIGHT:
                    self.going_right = True

            elif event.type == pygame.KEYUP:
                if event.key == K_LEFT:
                    self.going_left = False
                elif event.key == K_RIGHT:
                    self.going_right = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.new_rectangle(pygame.mouse.get_pos())
                
        self.update()
        self.display()

if __name__ == "__main__":
    game = CannonBallGame()
    while True:
        game.game_loop()