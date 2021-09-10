from ctypes import LittleEndianStructure
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

from ballObject import BallObject
from point import Point
from vector import Vector
from rectangle import Rectangle
from line import Line

WIDTH = 800
HEIGTH = 600

class CannonBallGame:

    def __init__(self):
        pygame.display.init()
        pygame.display.set_mode((WIDTH, HEIGTH), DOUBLEBUF|OPENGL)
        glClearColor(0.2, 0.5, 0.4, 0.2)

        self.cannon_point = Point(int(WIDTH/2), 0)


        self.ball_position = Point(0, 0)
        self.ball_motion = Vector(1, 1)

        self.cannonball = BallObject(10, self.ball_position, self.ball_motion, 1.0, 1.0, 1.0)

        self.clock = pygame.time.Clock()
        self.angle = 0
        self.speed = 200
        

        self.rectangles = []
        self.lines = []
        self.delta_time = 0

        self.going_left = False
        self.going_right = False

        self.rectDrawing = False
        self.rectStartPoint = Point(0,0)
        self.lineDrawing = False
        self.lineStartPoint = Point(0,0)

        self.sideLines = [Line(Point(0, 100), Point((WIDTH/6)*2, 100)), Line(Point(WIDTH, 100), Point(WIDTH - (WIDTH/6)*2, 100))]

        self.level = 1

        goal_level1 = Rectangle(Point((WIDTH/2)-50, HEIGTH-100), Point((WIDTH/2)+50, HEIGTH))
        goal_level2 = Rectangle(Point((WIDTH/3)-50, HEIGTH-200), Point((WIDTH/3)+50, HEIGTH - 100))
        goal_level3 = Rectangle(Point((WIDTH/2)-50, HEIGTH-100), Point((WIDTH/2)+50, HEIGTH))
        goal_level4 = Rectangle(Point((WIDTH/2)-50, HEIGTH-100), Point((WIDTH/2)+50, HEIGTH))
        goal_level5 = Rectangle(Point((WIDTH/2)-50, HEIGTH-100), Point((WIDTH/2)+50, HEIGTH))

        self.goals = [goal_level1, goal_level2, goal_level3, goal_level4, goal_level5]



    def update(self):
        self.delta_time = self.clock.tick(60) / 1000


        if self.going_left and self.angle < 45:
            self.angle += 180 * self.delta_time
        if self.going_right and self.angle > -45:
            self.angle -= 180 * self.delta_time

        if self.cannonball.fired == True:
            if self.cannonball.position.x < 0 or self.cannonball.position.x > WIDTH:
                self.cannonball.fired = False
            elif self.cannonball.position.y < 0 or self.cannonball.position.y > HEIGTH:
                self.cannonball.fired = False
            if (self.goals[self.level-1].middle.x - 50) <= self.cannonball.position.x <= (self.goals[self.level-1].middle.x + 50) and (self.goals[self.level-1].middle.y - 50) <= self.cannonball.position.y <= (self.goals[self.level-1].middle.y + 50):
                self.cannonball.fired = False
                print("Next level")

        self.cannonball.position.x += self.cannonball.motion.x * self.delta_time
        self.cannonball.position.y += self.cannonball.motion.y * self.delta_time
        
        if self.cannonball.fired == True:
            self.bounce_check()

    def line_bounce_check(self, line):
        dot_product_denom = line.normal.dot_product(self.cannonball.motion)
        if dot_product_denom != 0:
            thit = (line.normal.dot_product(line.start - self.cannonball.position))/dot_product_denom
            if 0 <= thit < (self.delta_time):
                phit = self.cannonball.position + (self.cannonball.motion * thit)
                if (int(line.start.distance(phit) + line.end.distance(phit))) == int(line.length): # Check if the point is on the line
                    unitNormal = Vector(line.normal.x / sqrt(line.normal.x**2 + line.normal.y**2), line.normal.y / sqrt(line.normal.x**2 + line.normal.y**2))
                    new_motion = self.cannonball.motion - (unitNormal * (2.0 * (self.cannonball.motion.dot_product(unitNormal))))
                    self.cannonball.position = phit
                    self.cannonball.motion = new_motion
                    return True

    def bounce_check(self):
        for rectangle in self.rectangles:
            if self.cannonball.motion.x > 0: #left side of rectangle
                if self.line_bounce_check(Line(rectangle.lt, rectangle.lb)):
                    break
            elif self.cannonball.motion.x < 0: 
                if self.line_bounce_check(Line(rectangle.rt, rectangle.rb)):
                    break

            if self.cannonball.motion.y > 0: # bottom of rectangle
                if self.line_bounce_check(Line(rectangle.lb, rectangle.rb)):
                    break

            elif self.cannonball.motion.y < 0:
                if self.line_bounce_check(Line(rectangle.lt, rectangle.rt)):
                    break
        
        for line in self.lines:
            if self.line_bounce_check(line):
                break
        
        for line in self.sideLines:
            if self.line_bounce_check(line):
                break


    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(0, 0, WIDTH, HEIGTH)
        gluOrtho2D(0, WIDTH, 0, HEIGTH)

        glColor3f(1.0, 0.7, 0.0)
        glLineWidth(2.0)
        for line in self.sideLines:
            line.draw()


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
        glTranslate(self.goals[self.level-1].middle.x, self.goals[self.level-1].middle.y, 0)
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
            rectangle.draw()
        glPopMatrix()

        glPushMatrix()
        glColor3f(0.0, 1.0, 1.0)
        for line in self.lines:
            line.draw()
        glPopMatrix()

        if self.rectDrawing:
            curr = pygame.mouse.get_pos()
            currPoint = Point(curr[0], HEIGTH - curr[1])
            new_rect = Rectangle(currPoint, self.rectStartPoint)
            glPushMatrix()
            glColor3f(1.0, 0.0, 0.0)
            new_rect.draw()
            glPopMatrix()
        
        if self.lineDrawing:
            curr = pygame.mouse.get_pos()
            currPoint = Point(curr[0], HEIGTH - curr[1])
            new_line = Line(currPoint, self.lineStartPoint)
            glPushMatrix()
            glColor3f(1.0, 1.0, 1.0)
            new_line.draw()
            glPopMatrix()

        pygame.display.flip()
    
    def fire_ball(self):
        self.cannonball.fired = True
        self.cannonball.motion.x = self.speed * -sin(self.angle * pi/180.0)
        self.cannonball.motion.y = self.speed * cos(self.angle * pi/180.0)
        self.cannonball.position.x = (WIDTH/2) + self.cannonball.motion.x * self.delta_time
        self.cannonball.position.y = self.cannonball.motion.y * self.delta_time

    def new_rectangle(self, startPoint, endPoint):
        new_rectangle = Rectangle(startPoint, endPoint)
        ok_to_append = True
        for rec in self.rectangles:
            if (abs(rec.middle.x - new_rectangle.middle.x) < (rec.width/2 + new_rectangle.width/2)) and (abs(rec.middle.y - new_rectangle.middle.y) < (rec.height/2 + new_rectangle.height/2)):
                ok_to_append = False
        if (abs(self.goals[self.level-1].middle.x - new_rectangle.middle.x) < ((self.goals[self.level-1].width)/2 + (new_rectangle.width)/2)) and (abs(self.goals[self.level-1].middle.y - new_rectangle.middle.y) < ((self.goals[self.level-1].height)/2 + (new_rectangle.height)/2)):
            ok_to_append = False

        if ok_to_append == True:
            self.rectangles.append(new_rectangle)
    
    def new_line(self, startPoint, endPoint):
        new_line = Line(startPoint, endPoint)
        ok_to_append = True
        for rec in self.rectangles:
                if (abs(rec.middle.x - new_line.start.x) < (rec.width/2)) and (abs(rec.middle.y - new_line.start.y) < (rec.height/2)):
                    if (abs(rec.middle.x - new_line.end.x) < (rec.width/2)) and (abs(rec.middle.y - new_line.end.y) < (rec.height/2)):
                        ok_to_append = False
        if (abs(self.goals[self.level-1].middle.x - new_line.start.x) < ((self.goals[self.level-1].width)/2)) or (abs(self.goals[self.level-1].middle.y - new_line.start.y) < ((self.goals[self.level-1].height)/2)):
            if (abs(self.goals[self.level-1].middle.x - new_line.end.x) < ((self.goals[self.level-1].width)/2)) or (abs(self.goals[self.level-1].middle.y - new_line.end.y) < ((self.goals[self.level-1].height)/2)):
                print("Ég er hér")
                ok_to_append = False
        if (new_line.start.y <= 100) or (new_line.end.y <= 100):
            ok_to_append = False
        
        if ok_to_append:
            self.lines.append(new_line)


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
                    if self.lineDrawing == False and self.rectDrawing == False:
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
                if event.button == 1:   #left click
                    if self.cannonball.fired == False:
                        self.rectDrawing = True
                        startPoint = pygame.mouse.get_pos()
                        self.rectStartPoint = Point(startPoint[0], HEIGTH - startPoint[1])
                if event.button == 3:   #right click
                    if self.cannonball.fired == False:
                        self.lineDrawing = True
                        #draw line 
                        startPoint = pygame.mouse.get_pos()
                        self.lineStartPoint = Point(startPoint[0], HEIGTH - startPoint[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:   #left click
                    if self.cannonball.fired == False:
                        curr = pygame.mouse.get_pos()
                        endPoint = Point(curr[0], HEIGTH - curr[1])
                        if endPoint != self.rectStartPoint:
                            if endPoint.x != self.rectStartPoint.x and endPoint.y != self.rectStartPoint.y:
                                self.new_rectangle(self.rectStartPoint, endPoint)
                        self.rectDrawing = False
                if event.button == 3:   #right click
                    #make line if valid
                    if self.cannonball.fired == False:
                        curr = pygame.mouse.get_pos()
                        endPoint = Point(curr[0], HEIGTH - curr[1])
                        if endPoint != self.lineStartPoint:
                            self.new_line(self.lineStartPoint, endPoint)
                        self.lineDrawing = False
                    

        self.update()
        self.display()

if __name__ == "__main__":
    game = CannonBallGame()
    while True:
        game.game_loop()