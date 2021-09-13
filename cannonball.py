'''
Project 2 in Computer Grafics, fall 2021
2D game - Bouncing cannonball game
Authors: Eva Sol Petursdottir (evap19@ru.is) and Halla Margret Jonsdottir (hallaj19@ru.is)

The player can change the angle of the cannon and fire the ball from the cannon. 
The goal is to hit the green rectangle on the screen for all 5 levels. The player has 3 lives.
The player can draw lines and rectangles on the screen before firing the ball to help the ball hit the goal.
'''



from ctypes import LittleEndianStructure
import pygame
from pygame import key
from pygame import rect
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random
from random import *

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

        self.sideLines = [Line(Point(0, 100), Point((WIDTH/6)*2, 100)), Line(Point(WIDTH, 100), Point(WIDTH - (WIDTH/6)*2, 100))]

        goal_level1 = Rectangle(Point((WIDTH/2)-50, HEIGTH-100), Point((WIDTH/2)+50, HEIGTH))
        goal_level2 = Rectangle(Point((WIDTH/3)-50, HEIGTH-200), Point((WIDTH/3)+50, HEIGTH - 100))
        goal_level3 = Rectangle(Point((WIDTH/6)-50, HEIGTH-300), Point((WIDTH/6)+50, HEIGTH - 200))
        goal_level4 = Rectangle(Point((WIDTH/2)-50, HEIGTH-200), Point((WIDTH/2)+50, HEIGTH - 100))
        goal_level5 = Rectangle(Point(WIDTH - 150, HEIGTH-200), Point(WIDTH - 50, HEIGTH - 100))
        self.goals = [goal_level1, goal_level2, goal_level3, goal_level4, goal_level5]
        
        self.rectangles = [] # Rectangles drawn by player

        self.lines = []      # Lines drawn by player

        lines_level1 = [] # Empty in our version but easy to add some lines to level 1
        lines_level2 = [Line(Point((WIDTH/3)-150, HEIGTH-300), Point((WIDTH/3)+150, HEIGTH-300))]
        lines_level3 = [Line(Point((WIDTH/6)-50, HEIGTH-350), Point((WIDTH/6)+100, HEIGTH - 350)), Line(Point((WIDTH/6)+100, HEIGTH - 350), Point((WIDTH/6)+100, HEIGTH - 200))]
        lines_level4 = [Line(Point((WIDTH/2)-200, 200), Point((WIDTH/2)+200, 200))]
        lines_level5 = [Line(Point(WIDTH - (WIDTH/6)*2, 100), Point(WIDTH, HEIGTH/2)), Line(Point(WIDTH - 70, HEIGTH-230), Point(WIDTH - 30, HEIGTH-230)), Line(Point(WIDTH - 30, HEIGTH-230), Point(WIDTH - 30, HEIGTH-70)), Line(Point(WIDTH - 30, HEIGTH-70), Point(WIDTH - 180, HEIGTH-70)), Line(Point(WIDTH - 180, HEIGTH-70), Point(WIDTH - 180, HEIGTH - 230)), Line(Point(WIDTH - 180, HEIGTH - 230), Point(WIDTH - 130, HEIGTH - 230))]
        self.level_lines = [lines_level1, lines_level2, lines_level3, lines_level4, lines_level5]

        self.delta_time = 0

        self.going_left = False
        self.going_right = False

        self.rectDrawing = False
        self.rectStartPoint = Point(0,0)
        self.lineDrawing = False
        self.lineStartPoint = Point(0,0)

        self.level = 1
        self.lives = 3
        self.victory = False
        self.game_over = False
    
    def reset_game(self):
        '''Resets level and lives for a new game'''
        self.lives = 3
        self.level = 1
        self.victory = False
        self.game_over = False

    def update(self):
        '''Updates angle, motion of ball, checks if ball is on the screen or has hit the goal, updates level and lives. Calls bounce check.'''
        self.delta_time = self.clock.tick(60) / 1000

        # Change the angle of the cannon
        if self.going_left and self.angle < 45:
            self.angle += 180 * self.delta_time
        if self.going_right and self.angle > -45:
            self.angle -= 180 * self.delta_time

        # Happens if the ball has been fired
        if self.cannonball.fired == True:
            # Ball is outside of the screen and player looses a life
            if self.cannonball.position.x < 0 or self.cannonball.position.x > WIDTH or self.cannonball.position.y < 0 or self.cannonball.position.y > HEIGTH:
                self.cannonball.fired = False
                self.rectangles = []
                self.lines = []
                if self.lives > 1:
                    self.lives -= 1
                else:
                    # Player has lost all of his lives
                    self.game_over = True
            # Ball has hit the goal and player goes to next level
            if (self.goals[self.level-1].middle.x - 50) <= self.cannonball.position.x <= (self.goals[self.level-1].middle.x + 50) and (self.goals[self.level-1].middle.y - 50) <= self.cannonball.position.y <= (self.goals[self.level-1].middle.y + 50):
                self.cannonball.fired = False
                self.rectangles = []
                self.lines = []
                if self.level < 5:
                    self.level += 1
                    self.rectangles = []
                    self.lines = []
                else:
                    # Player has won the game
                    self.victory = True

        # Moves the ball
        self.cannonball.position.x += self.cannonball.motion.x * self.delta_time
        self.cannonball.position.y += self.cannonball.motion.y * self.delta_time
        
        # Calls bounce check if ball is moving
        if self.cannonball.fired == True:
            self.bounce_check()

    def line_bounce_check(self, line):
        '''Gets line as an argument and checks if the ball hits it in the next frame. 
        If so it changes the potition and motion of the ball'''
        dot_product_denom = line.normal.dot_product(self.cannonball.motion)
        if dot_product_denom != 0:
            thit = (line.normal.dot_product(line.start - self.cannonball.position))/dot_product_denom
            # If thit is smaller that delta time, the hit will happen in the next frame
            if 0 <= thit < (self.delta_time):
                phit = self.cannonball.position + (self.cannonball.motion * thit)
                # Check if the point is on the line
                if (int(line.start.distance(phit) + line.end.distance(phit))) == int(line.length): 
                    unitNormal = Vector(line.normal.x / sqrt(line.normal.x**2 + line.normal.y**2), line.normal.y / sqrt(line.normal.x**2 + line.normal.y**2))
                    new_motion = self.cannonball.motion - (unitNormal * (2.0 * (self.cannonball.motion.dot_product(unitNormal))))
                    self.cannonball.position = phit
                    self.cannonball.motion = new_motion
                    return True

    def bounce_check(self):
        '''Checks if the ball hits any object on the screen. Calls line_bounce check for individual lines in the object.'''
        # Check all drawn rectangles
        for rectangle in self.rectangles:
            # check left side of rectangle, ball is going right
            if self.cannonball.motion.x > 0: 
                if self.line_bounce_check(Line(rectangle.lt, rectangle.lb)):
                    break
             # check right side of rectangle, ball is going left
            elif self.cannonball.motion.x < 0:
                if self.line_bounce_check(Line(rectangle.rt, rectangle.rb)):
                    break
            # check bottom of rectangle, ball is going up
            if self.cannonball.motion.y > 0: 
                if self.line_bounce_check(Line(rectangle.lb, rectangle.rb)):
                    break
            # check top of rectangle, ball is going down
            elif self.cannonball.motion.y < 0: 
                if self.line_bounce_check(Line(rectangle.lt, rectangle.rt)):
                    break
        
        # Check all drawn lines
        for line in self.lines:
            if self.line_bounce_check(line):
                break
        
        # Check side lines
        for line in self.sideLines:
            if self.line_bounce_check(line):
                break

        # Check level lines
        for line in self.level_lines[self.level - 1]:
            if self.line_bounce_check(line):
                break


    def display(self):
        '''Displays every frame, the cannon, the ball in motion, already set objects, 
        drawn objects and objects that are currently being drawn'''
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(0, 0, WIDTH, HEIGTH)
        gluOrtho2D(0, WIDTH, 0, HEIGTH)

        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(2.0)
        # Drawing side lines
        for line in self.sideLines:
            line.draw()

        # The ball is drawn if it has already been fired
        if self.cannonball.fired == True:
            self.cannonball.display_object()


        # The cannon
        glPushMatrix()
        glTranslate(self.cannon_point.x, self.cannon_point.y, 0)
        glRotate(self.angle, 0, 0, 1)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(0 - 15, 0 - 100)
        glVertex2f(0 - 15, 0 + 100)
        glVertex2f(0 + 15, 0 - 100)
        glVertex2f(0 - 15, 0 + 100)
        glVertex2f(0 + 15, 0 - 100)
        glVertex2f(0 + 15, 0 + 100)
        glEnd()
        glPopMatrix()

        # The current goal (different for each level)
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

        # Lines that are set for each level
        glPushMatrix()
        glColor3f(0.0, 0.4, 0.0)
        for line in self.level_lines[self.level - 1]:
            line.draw()
        glPopMatrix()

        # Already drawn rectangles
        glPushMatrix()
        glColor3f(0.3, 0.0, 0.3)
        for rectangle in self.rectangles:
            rectangle.draw()
        glPopMatrix()

        # Already drawn lines
        glPushMatrix()
        glColor3f(0.0, 1.0, 1.0)
        for line in self.lines:
            line.draw()
        glPopMatrix()

        # Rectangle currently being drawn
        if self.rectDrawing:
            curr = pygame.mouse.get_pos()
            currPoint = Point(curr[0], HEIGTH - curr[1])
            new_rect = Rectangle(currPoint, self.rectStartPoint)
            glPushMatrix()
            glColor3f(0.4, 0.4, 1.0)
            new_rect.draw()
            glPopMatrix()
        
        # Line currently being drawn
        if self.lineDrawing:
            curr = pygame.mouse.get_pos()
            currPoint = Point(curr[0], HEIGTH - curr[1])
            new_line = Line(currPoint, self.lineStartPoint)
            glPushMatrix()
            glColor3f(1.0, 1.0, 1.0)
            new_line.draw()
            glPopMatrix()

        if not self.game_over:
            glPushMatrix()
            glColor3f(1.0, 0.0, 0.0)
            space_between = 30
            start_position = 10
            width_of_life = 20
            for life in range(self.lives):
                glBegin(GL_TRIANGLES)
                glVertex2f(start_position + space_between * life, 50 - 10)
                glVertex2f(start_position + space_between * life, 50 + 10)
                glVertex2f(start_position + width_of_life + space_between * life, 50 - 10)
                glVertex2f(start_position + space_between * life, 50 + 10)
                glVertex2f(start_position + width_of_life + space_between * life, 50 - 10)
                glVertex2f(start_position + width_of_life + space_between * life, 50 + 10)
                glEnd()
            glPopMatrix()

        # Displays victory message
        if self.victory:
            glColor3f(1.0, 0.7, 0.0)
            glLineWidth(2.0)
            middle = Point(WIDTH/2, HEIGTH/2)
            glPushMatrix()
            glBegin(GL_LINES)
            #Y
            glVertex2f(middle.x - 160, middle.y + 15)
            glVertex2f(middle.x - 160, middle.y - 50)
            glVertex2f(middle.x - 160, middle.y + 15)
            glVertex2f(middle.x - 185, middle.y + 50)
            glVertex2f(middle.x - 160, middle.y + 15)
            glVertex2f(middle.x - 135, middle.y + 50)
            #O
            glVertex2f(middle.x - 125, middle.y - 50)
            glVertex2f(middle.x - 125, middle.y + 50)
            glVertex2f(middle.x - 125, middle.y + 50)
            glVertex2f(middle.x - 75, middle.y + 50)
            glVertex2f(middle.x - 75, middle.y + 50)
            glVertex2f(middle.x - 75, middle.y - 50)
            glVertex2f(middle.x - 75, middle.y - 50)
            glVertex2f(middle.x - 125, middle.y - 50)
            #U
            glVertex2f(middle.x - 65, middle.y + 50)
            glVertex2f(middle.x - 65, middle.y - 50)
            glVertex2f(middle.x - 65, middle.y - 50)
            glVertex2f(middle.x - 15, middle.y - 50)
            glVertex2f(middle.x - 15, middle.y - 50)
            glVertex2f(middle.x - 15, middle.y + 50)
            #W
            glVertex2f(middle.x + 15, middle.y + 50)
            glVertex2f(middle.x + 27, middle.y - 50)
            glVertex2f(middle.x + 27, middle.y - 50)
            glVertex2f(middle.x + 40, middle.y)
            glVertex2f(middle.x + 40, middle.y)
            glVertex2f(middle.x + 53, middle.y - 50)
            glVertex2f(middle.x + 53, middle.y - 50)
            glVertex2f(middle.x + 65, middle.y + 50)
            #O
            glVertex2f(middle.x + 125, middle.y - 50)
            glVertex2f(middle.x + 125, middle.y + 50)
            glVertex2f(middle.x + 125, middle.y + 50)
            glVertex2f(middle.x + 75, middle.y + 50)
            glVertex2f(middle.x + 75, middle.y + 50)
            glVertex2f(middle.x + 75, middle.y - 50)
            glVertex2f(middle.x + 75, middle.y - 50)
            glVertex2f(middle.x + 125, middle.y - 50)
            #N
            glVertex2f(middle.x + 135, middle.y - 50)
            glVertex2f(middle.x + 135, middle.y + 50)
            glVertex2f(middle.x + 135, middle.y + 50)
            glVertex2f(middle.x + 185, middle.y - 50)
            glVertex2f(middle.x + 185, middle.y - 50)
            glVertex2f(middle.x + 185, middle.y + 50)
            glEnd()
            glPopMatrix()
        
        # Displays game over message
        if self.game_over:
            glColor3f(1.0, 0.7, 0.0)
            glLineWidth(2.0)
            middle = Point(WIDTH/2, HEIGTH/2)
            glPushMatrix()
            glBegin(GL_LINES)
            # G
            glVertex2f(middle.x - 195, middle.y + 50)
            glVertex2f(middle.x - 245, middle.y + 50)
            glVertex2f(middle.x - 245, middle.y + 50)
            glVertex2f(middle.x - 245, middle.y - 50)
            glVertex2f(middle.x - 245, middle.y - 50)
            glVertex2f(middle.x - 195, middle.y - 50)
            glVertex2f(middle.x - 195, middle.y - 50)
            glVertex2f(middle.x - 195, middle.y)
            glVertex2f(middle.x - 190, middle.y)
            glVertex2f(middle.x - 200, middle.y)
            # A
            glVertex2f(middle.x - 135, middle.y - 50)
            glVertex2f(middle.x - 160, middle.y + 50)
            glVertex2f(middle.x - 160, middle.y + 50)
            glVertex2f(middle.x - 185, middle.y - 50)
            glVertex2f(middle.x - 147.5, middle.y)
            glVertex2f(middle.x - 172.5, middle.y)
            # M
            glVertex2f(middle.x - 75, middle.y - 50)
            glVertex2f(middle.x - 75, middle.y + 50)
            glVertex2f(middle.x - 75, middle.y + 50)
            glVertex2f(middle.x - 100, middle.y)
            glVertex2f(middle.x - 100, middle.y)
            glVertex2f(middle.x - 125, middle.y + 50)
            glVertex2f(middle.x - 125, middle.y + 50)
            glVertex2f(middle.x - 125, middle.y - 50)
            # E
            glVertex2f(middle.x - 65, middle.y - 50)
            glVertex2f(middle.x - 65, middle.y + 50)
            glVertex2f(middle.x - 65, middle.y - 50)
            glVertex2f(middle.x - 15, middle.y - 50)
            glVertex2f(middle.x - 65, middle.y + 50)
            glVertex2f(middle.x - 15, middle.y + 50)
            glVertex2f(middle.x - 65, middle.y)
            glVertex2f(middle.x - 35, middle.y)
            # O
            glVertex2f(middle.x + 15, middle.y - 50)
            glVertex2f(middle.x + 15, middle.y + 50)
            glVertex2f(middle.x + 15, middle.y + 50)
            glVertex2f(middle.x + 65, middle.y + 50)
            glVertex2f(middle.x + 65, middle.y + 50)
            glVertex2f(middle.x + 65, middle.y - 50)
            glVertex2f(middle.x + 65, middle.y - 50)
            glVertex2f(middle.x + 15, middle.y - 50)
            # V
            glVertex2f(middle.x + 75, middle.y + 50)
            glVertex2f(middle.x + 100, middle.y - 50)
            glVertex2f(middle.x + 100, middle.y - 50)
            glVertex2f(middle.x + 125, middle.y + 50)
            # E
            glVertex2f(middle.x + 135, middle.y - 50)
            glVertex2f(middle.x + 135, middle.y + 50)
            glVertex2f(middle.x + 135, middle.y - 50)
            glVertex2f(middle.x + 185, middle.y - 50)
            glVertex2f(middle.x + 135, middle.y + 50)
            glVertex2f(middle.x + 185, middle.y + 50)
            glVertex2f(middle.x + 135, middle.y)
            glVertex2f(middle.x + 165, middle.y)
            # R
            glVertex2f(middle.x + 195, middle.y - 50)
            glVertex2f(middle.x + 195, middle.y + 50)
            glVertex2f(middle.x + 195, middle.y + 50)
            glVertex2f(middle.x + 245, middle.y + 25)
            glVertex2f(middle.x + 245, middle.y + 25)
            glVertex2f(middle.x + 195, middle.y)
            glVertex2f(middle.x + 195, middle.y)
            glVertex2f(middle.x + 245, middle.y - 50)
            glEnd()
            glPopMatrix()

        pygame.display.flip()
    
    def fire_ball(self):
        '''Called when ball is fired from the cannon. Motion is set to the angle of 
        the cannon at that time. Potition of the ball is initialized'''
        self.cannonball.fired = True
        self.cannonball.motion.x = self.speed * -sin(self.angle * pi/180.0)
        self.cannonball.motion.y = self.speed * cos(self.angle * pi/180.0)
        self.cannonball.position.x = (WIDTH/2) + self.cannonball.motion.x * self.delta_time
        self.cannonball.position.y = self.cannonball.motion.y * self.delta_time

    def new_rectangle(self, startPoint, endPoint):
        '''Takes start point and end point as arguments and creates a new rectangle. 
        Checks if the rectangle is at a valid position on the screen. If so it is added to the rectangle list.'''
        new_rectangle = Rectangle(startPoint, endPoint)
        ok_to_append = True
        for rec in self.rectangles:
            # The new rectangle may not overlap another rectangle
            if (abs(rec.middle.x - new_rectangle.middle.x) < (rec.width/2 + new_rectangle.width/2)) and (abs(rec.middle.y - new_rectangle.middle.y) < (rec.height/2 + new_rectangle.height/2)):
                ok_to_append = False
        # The new rectangle may not overlap the goal
        if (abs(self.goals[self.level-1].middle.x - new_rectangle.middle.x) < ((self.goals[self.level-1].width)/2 + (new_rectangle.width)/2)) and (abs(self.goals[self.level-1].middle.y - new_rectangle.middle.y) < ((self.goals[self.level-1].height)/2 + (new_rectangle.height)/2)):
            ok_to_append = False
        # The new rectangle may not go below the side lines
        if new_rectangle.lb.y < 100:
            ok_to_append = False
        
        # If everything is ok. The rectangle is added to the rectangles list
        if ok_to_append == True:
            self.rectangles.append(new_rectangle)
    
    def new_line(self, startPoint, endPoint):
        '''Takes start point and end point as arguments and creates a new line. 
        Checks if the line is at a valid position on the screen. If so it is added to the lines list.'''
        new_line = Line(startPoint, endPoint)
        ok_to_append = True
        for rec in self.rectangles:
            # The line can not be all inside of a rectangle
            if (abs(rec.middle.x - new_line.start.x) < (rec.width/2)) and (abs(rec.middle.y - new_line.start.y) < (rec.height/2)):
                if (abs(rec.middle.x - new_line.end.x) < (rec.width/2)) and (abs(rec.middle.y - new_line.end.y) < (rec.height/2)):
                    ok_to_append = False
        # The line can not start or end inside of the goal
        if (abs(self.goals[self.level-1].middle.x - new_line.start.x) < ((self.goals[self.level-1].width)/2)) and (abs(self.goals[self.level-1].middle.y - new_line.start.y) < ((self.goals[self.level-1].height)/2)):
            ok_to_append = False
        if (abs(self.goals[self.level-1].middle.x - new_line.end.x) < ((self.goals[self.level-1].width)/2)) and (abs(self.goals[self.level-1].middle.y - new_line.end.y) < ((self.goals[self.level-1].height)/2)):
            ok_to_append = False
        
        # The line can not go below the side lines
        if (new_line.start.y <= 100) or (new_line.end.y <= 100):
            ok_to_append = False
        
        # If everything is ok. The line is added to the lines list
        if ok_to_append:
            self.lines.append(new_line)


    def game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                # ESC always quits the game
                if event.key == K_ESCAPE:
                        pygame.quit()
                        quit()
                # If victory or game over messages are on screen any key will restart the game
                elif self.victory or self.game_over:
                    self.reset_game()
                else:
                    # Randomize backround color
                    if event.key == K_q:
                        glClearColor(random(), random(), random(), 1.0)
                    #Fires ball from cannon
                    elif event.key == K_SPACE or event.key == K_z:
                        if self.lineDrawing == False and self.rectDrawing == False:
                            if self.cannonball.fired == False:
                                self.fire_ball()
                    # Changing the angle of the cannon
                    elif event.key == K_LEFT:
                        self.going_left = True
                    elif event.key == K_RIGHT:
                        self.going_right = True

            elif event.type == pygame.KEYUP:
                # Stop changing the angle of the cannon
                if event.key == K_LEFT:
                    self.going_left = False
                elif event.key == K_RIGHT:
                    self.going_right = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If victory or game over messages are on screen mouse click will restart the game
                if self.victory or self.game_over:
                    self.reset_game()
                else:
                    if event.button == 1:   #left click
                        # If cannonball has not been fired the user starts drawing a rectangle
                        if self.cannonball.fired == False:
                            self.rectDrawing = True
                            startPoint = pygame.mouse.get_pos()
                            self.rectStartPoint = Point(startPoint[0], HEIGTH - startPoint[1])
                    if event.button == 3:   #right click
                        # If cannonball has not been fired the user starts drawing a line
                        if self.cannonball.fired == False:
                            self.lineDrawing = True
                            startPoint = pygame.mouse.get_pos()
                            self.lineStartPoint = Point(startPoint[0], HEIGTH - startPoint[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:   #left click
                    # If cannonball has not been fired the user stops drawing a rectangle, and new_rectangle() is called
                    if self.cannonball.fired == False:
                        curr = pygame.mouse.get_pos()
                        endPoint = Point(curr[0], HEIGTH - curr[1])
                        if endPoint != self.rectStartPoint:
                            if endPoint.x != self.rectStartPoint.x and endPoint.y != self.rectStartPoint.y:
                                self.new_rectangle(self.rectStartPoint, endPoint)
                        self.rectDrawing = False
                if event.button == 3:   #right click
                    # If cannonball has not been fired the user stops drawing a line, and new_line() is called
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