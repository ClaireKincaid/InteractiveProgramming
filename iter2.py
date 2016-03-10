#iteration 2 of ender's game
#Max Schommer
#Claire Kincaid
#March 3, 2016

import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
from random import choice
from collections import deque
import math
import numpy as np
import argparse
import imutils
import cv2

class EndersGameView(object):
    """ Visualizes an enders game in a pygame window """
    def __init__(self, model, screen):
        """ Initialize the view with the specified model
            and screen. """
        self.model = model
        self.screen = screen

    def draw(self):
        """ Draw the game state to the screen """
        a = FlagShip.angle
        self.screen.fill(pygame.Color('black'))
        # # draw the Ship to the screen
        img = pygame.image.load("FlagShip.bmp")
        r = pygame.Rect(FlagShip.x-20,
                        FlagShip.y-30,
                        FlagShip.width,
                        FlagShip.height)
        img = pygame.transform.rotate(img, a)
        screen.blit(img, r)
        pygame.draw.circle(screen, (  0,   0, 255), (flagShipTracker.x, flagShipTracker.y), 20, 4)
        pygame.display.update()


class Ship(object):
    """Represents a ship. """
    def __init__(self, x=0, y=0, width=40, height=60, angle=0, velocity=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.velocity = velocity
        
class Ball_Circle(object):
    """Represents a circle where the cv is pointing"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
class EndersGameModel(object):
    """ Stores the game state for our Enders game """
    def __init__(self):
        self.Ship = Ship(640/2, 480 - 30, 10, 10)
        self.ship1 = Ship(300, 300)

class OpenCVController_notreally(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event, centers, previouscenters):
        """ Look for mouse movements and respond appropriately """
        p1 = [FlagShip.x, FlagShip.y]
        # print math.cos(get_angle(p1, previouscenters[1]))
        # print center[1]
        # if calculate_dist(p1, centers[1]) <
        try:
            # print 90+get_angle(p1, centers[1])
            FlagShip.x += .01*(centers[1][0]-FlagShip.x)
            FlagShip.y += .01*(centers[1][1]-FlagShip.y)
        except TypeError:
            FlagShip.x += .01*(previouscenters[1][0]-FlagShip.x)
            FlagShip.y += .01*(previouscenters[1][1]-FlagShip.y)

class OpenCVController(object):
    def __init__(self, model):
        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        orangeLower = (2, 144, 139)
        orangeUpper = (12, 255, 255)
        blueLower = (20,171,93)
        blueUpper = (29,255,255)
        self.ballList = [[orangeLower, orangeUpper],[blueLower, blueUpper]]
        self.camera = cv2.VideoCapture(0)
        self.model = model

    def get_center(self):
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
        return center


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




def get_angle(p1, p2):
    dx = float(p2[0] - p1[0])
    dy = float(p2[1] - p1[1])
    rads = math.atan2(-dy,dx)
    degs = -90.0 + math.degrees(rads)
    
    return degs


def calculate_dist(p1, p2):
    dist = math.sqrt(float((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))
    
    # velocity = math.sqrt(dist)/20.0

    return dist

if __name__ == '__main__':
    pygame.init()
    size = (1280, 840)
    screen = pygame.display.set_mode(size)

    model = EndersGameModel()

    view = EndersGameView(model, screen)
    false_controller = OpenCVController_notreally(model)
    controller = OpenCVController(model)
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    
    # # keep looping
    previouscenters = {}
    for i in range(len(controller.ballList)):
      previouscenters[i] = [200, 200]
    running = True
    FlagShip = Ship()
    flagShipTracker = Ball_Circle()
    while running:
        center = controller.get_center()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        false_controller.handle_event(event, center, previouscenters) # This is not an event, it just always is.
        for i in range(len(controller.ballList)):  # This makes the center of the last known location equal the center, or else it
            if center[i] != None:
                previouscenters[i] = center[i]
            else:
                continue
        flagShipTracker.x = previouscenters[1][0]
        flagShipTracker.y = previouscenters[1][1]
        point = (FlagShip.x, FlagShip.y)
        FlagShip.angle = get_angle(point,previouscenters[1])
        view.draw()
        time.sleep(.001)

camera.release()
cv2.destroyAllWindows()
