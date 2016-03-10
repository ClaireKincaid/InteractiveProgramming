#Ender's Game
#Claire Kincaid, Maximillian Schommer
#Interactive Programming Mini Project (iter 3)
#March 8 2016

import os
import sys
import pygame
from pygame.locals import *
import time
import random
from random import choice
from collections import deque
import math
import numpy as np
import argparse
import imutils
import cv2

if not pygame.font: print 'Warning: fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class EndersGameView(object):
    """Visualizes Ender's Game in a pygame window"""
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen
    def LoadSprites(self):
        self.UserShip = UserShip()
        self.EnemyShip = EnemyShip()
        self.Asteroid = Asteroid()
        self.Missile = Missile()
        self.Laser = Laser()
        self.UserSprites = pygame.sprite.RenderPlain((self.UserShip))
        self.EnemySprites = pygame.sprite.RenderPlain((self.EnemyShip))
        self.Asteroids = pygame.sprite.RenderPlain((self.Asteroid))
        self.Missiles = pygame.sprite.RenderPlain((self.Missile))
        self.Lasers = pygame.sprite.RenderPlain((self.Laser))
        self.Planet = Planet()
        self.Star = Star()
        self.OpenCVController = OpenCVController(model)
    def draw(self):
        """Draw the game state to the screen"""
        #fills the screen w/ black
        self.screen.fill(pygame.Color('black'))
        #draw planet to the screen
        for Star in self.model.stars:
            pygame.draw.circle(self.screen, pygame.Color('white'), (Star.x, Star.y), Star.radius, 0)
        self.screen.blit(self.Star.image, self.Star.rect)
        self.screen.blit(self.Planet.image, self.Planet.rect)

        for UserShip in self.model.UserSprites:
            self.screen.blit(UserShip.image, UserShip.rect)

        for Asteroid in self.model.asteroids:
            self.screen.blit(Asteroid.image, Asteroid.rect)
        # for i in range(1):
        #     center[i] = self.OpenCVController.previouscenters()[i]
        #     pygame.draw.circle(self.screen, pygame.Color('white'), (center[i][0], center[i][1]), 10, 4)
        pygame.display.update()



class EndersGameModel(object):
    """Stores the game state of Enders Game"""
    def __init__(self):
        self.planet = Planet(400, 1280/2,-200)
        self.stars = []
        self.asteroids = []
        self.UserSprites = []
        self.EnemySprites = []
        self.Missiles = {}
        self.Circles = []
        for i in range(30):
            star = Star(1, random.randint(0, 1280), random.randint(0, 760))
            self.stars.append(star)
        for j in range(10):
            asteroid = Asteroid(random.randint(0, 1280), random.randint(3*760/8, 760*5/8),random.randint(25, 90), 0)
            self.asteroids.append(asteroid)
        for k in range(10):
            mycircle = Circle_Tracker(k)
            myship = UserShip(k)
            self.Circles.append(mycircle)
            self.UserSprites.append(myship)
        for myShip in self.UserSprites:
            myShip.Missiles = myShip.arsenal

class Circle_Tracker(object):
    """Creates a circle that will point out where the open CV ball is in real time."""
    def __init__(self, name=0, radius=10, x=0, y=0):
        self.name = name
        self.radius = radius
        self.x = x
        self.y = y

class Star(object):
    """Creates white points for arbitrary placement in background, inert objects
    attributes: radius, x & y positions"""
    def __init__(self, radius=200, x=640, y=-100):
        self.image = pygame.image.load('stars2.jpg')
        self.image = pygame.transform.scale(self.image, (1280,760))
        self.rect = pygame.Surface.get_rect(self.image)
        
        self.radius = radius
        self.x = x
        self.y = y

class Planet(object):
    """Creates enemy planet in background, is inert object
    attributes: radius, x & y positions"""
    def __init__(self, radius=200, x=640, y=-100, size=700):
        self.image = pygame.image.load('Duna2.BMP')
        self.image = pygame.transform.scale(self.image, (2*size,size))
        self.rect = pygame.Surface.get_rect(self.image)
        self.rect = self.rect.move(x+(self.rect.left-self.rect.right)/2,y+(self.rect.top-self.rect.bottom)/2)
        self.radius = radius
        self.x = x
        self.y = y
        

class Asteroid(pygame.sprite.DirtySprite):
    """Creates asteroids to fill background of game
    attributes: Sprite, x and y positions"""
    def __init__(self, x = 0, y = 0, size = 30, missile_pellets = 0):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load('asteroid.BMP')
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = pygame.Surface.get_rect(self.image)
        self.rect = self.rect.move(x,y)
        self.x = x
        self.y = y
        self.missile_pellets = missile_pellets #of missiles absorbed by asteroid

class UserShip(pygame.sprite.DirtySprite):
    """Creates player's ships attributes: Sprite, heading (angle), velocity, x position, y position, reload counter missile, reload counter laser"""
    def __init__(self, name = 1, x = 0, y = 0, width = 40, height = 60, angle = 0, velocity = 0, arsenal = 10, size=(40,60)):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load('FlagShip.bmp')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = pygame.Surface.get_rect(self.image)
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.velocity = velocity
        self.arsenal = arsenal #of missiles before reload
    def move_ship(self, OpenCVController):
        """This will be the function to move the ship based on the OpenCVController"""
        # for k in range(len(OpenCVController.ballList)):
        # model.UserSprites[k].x = OpenCVController.previouscenters[k][0]
        # model.UserSprites[k].y = OpenCVController.previouscenters[k][1]
        # print math.cos(get_angle(p1, previouscenters[1]))
        # print center[1]
        # if calculate_dist(p1, centers[1]) <

        self.x += .01*(OpenCVController.previouscenters[self.name][0] - self.x)
        print self.x
        self.y += .01*(OpenCVController.previouscenters[self.name][1] - self.y)
        print self.y
        self.rect.centerx = self.x
        self.rect.centery = self.y

class EnemyShip(pygame.sprite.DirtySprite):
    """Creates enemy ships
    attributes:sprite, x & y positions, pattern, shooting timer (missiles), collision w/ missile/laser"""
    def __init__(self, x = 0, y = 0, width = 40, height = 60, angle = 0, velocity = 0):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load('Fighter.bmp')
        self.rect = pygame.image.load('Fighter.bmp')
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.velocity = velocity

class Missile(pygame.sprite.DirtySprite):
    """Missiles created by UserShip and shot in direction UserShip is facing
    attributes: sprite, velocity, x & y positions, collision"""
    def __init__(self, x = 0, y = 0, width = 10, height = 15, angle = 0, velocity = 0, timer = 5):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load('missile.BMP')
        self.rect = pygame.image.load('missile.BMP')
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.velocity = velocity
        self.timer = timer #time between reloads in seconds

class Laser(pygame.sprite.DirtySprite):
    """Lasers created by UserShip and shot in direction usership is facing
    sattributes: sprite, velocity, slope, initial point, collision"""
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

class OpenCVController(object):
    def __init__(self, model):
        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        orangeLower = (29, 58, 85)
        orangeUpper = (39, 255, 255)
        blueLower = (16,136,100)
        blueUpper = (26,255,255)
        self.ballList = [[orangeLower, orangeUpper],[blueLower, blueUpper]]
        self.camera = cv2.VideoCapture(0)
        self.model = model
        self.previouscenters = {}
        for i in range(len(self.ballList)):
            self.previouscenters[i] = [600, 600]


    def get_center(self, model):
        # grab the current frame
        (grabbed, frame) = self.camera.read()
        frame = cv2.flip(frame,1)
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        center = {}
        x = {}
        y = {}
        radius = {}
        for j in range(len(self.ballList)):
            colorLower = self.ballList[j][0]
            colorUpper = self.ballList[j][1]
            mask = cv2.inRange(hsv, colorLower, colorUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center[j] = None
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x[j], y[j]), radius[j]) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center[j] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                center[j] = center[j][0]*3-200, center[j][1]*3-200
        for i in range(len(self.ballList)):  # This makes the center of the last known location equal the center, or else it is the previous location.
            if center[i] != None:
                self.previouscenters[i] = center[i]
            else:
                continue

        for k in range(len(self.ballList)):
            model.UserSprites[k].move_ship(self)
        for l in range(len(self.ballList)):
            model.Circles[l].x = self.previouscenters[l][0]
            model.Circles[l].y = self.previouscenters[l][1]

    def handle_event(self, event):
        """ Look for qawsedrftgyhujikolp; keypresses to
            modify the missile and laser firerings"""
        if event.type != KEYDOWN:
            return

        if event.key == pygame.K_q:
            self.model.ship1.laser = 1
        if event.key == pygame.K_a:
            self.model.ship1.missile = 1

        if event.key == pygame.K_w:
            self.model.ship2.laser = 1
        if event.key == pygame.K_s:
            self.model.ship2.missile = 1

        if event.key == pygame.K_e:
            self.model.ship3.laser = 1
        if event.key == pygame.K_d:
            self.model.ship3.missile = 1

        if event.key == pygame.K_r:
            self.model.ship4.laser = 1
        if event.key == pygame.K_f:
            self.model.ship4.missile = 1

        if event.key == pygame.K_t:
            self.model.ship5.laser = 1
        if event.key == pygame.K_g:
            self.model.ship5.missile = 1

        if event.key == pygame.K_y:
            self.model.ship6.laser = 1
        if event.key == pygame.K_h:
            self.model.ship6.missile = 1

        if event.key == pygame.K_u:
            self.model.ship7.laser = 1
        if event.key == pygame.K_j:
            self.model.ship7.missile = 1

        if event.key == pygame.K_i:
            self.model.ship8.laser = 1
        if event.key == pygame.K_k:
            self.model.ship8.missile = 1

        if event.key == pygame.K_o:
            self.model.ship9.laser = 1
        if event.key == pygame.K_l:
            self.model.ship9.missile = 1

        if event.key == pygame.K_p:
            self.model.ship10.laser = 1
        if event.key == pygame.K_SEMICOLON:
            self.model.ship10.missile = 1


if __name__ == '__main__':
    pygame.init()
    size = (1280, 760)
    screen = pygame.display.set_mode(size)
    model = EndersGameModel()
    view = EndersGameView(model, screen)
    controller1 = OpenCVController(model)
#Main Game Loop, outside of method (could be within method, is cleaner??)
    running = True
    view.LoadSprites()
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller1.handle_event(event)
        controller1.get_center(model)

        view.draw()
        time.sleep(.001)


