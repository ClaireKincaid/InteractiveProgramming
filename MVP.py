#minimum viable product for Interactive programming project
#Claire Kincaid
#Maximillian Schommer

import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
from random import choice

class EndersGameView(object):
    """ Visualizes Ender's Game in a pygame window """
    def __init__(self, model, screen):
        """ Initialize the view with the specified model
            and screen. """
        self.model = model
        self.screen = screen
    def draw(self):
        """ Draw the game state to the screen """
        self.screen.fill(pygame.Color('black'))
        # draw the bar on the screen
        r = pygame.Rect(self.model.bar.left,
                        self.model.bar.top,
                        self.model.bar.width,
                        self.model.bar.height)
        pygame.draw.rect(self.screen, pygame.Color('white'), r)
        pygame.display.update()

class Bar(object):
    """ Represents the bar in our MVP """
    def __init__(self, left, top, width, height):
        """ Initialize the bar for MVP with the specified geometry """
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class MVP(object):
    """ Stores the game state for our game MVP """
    def __init__(self):
        self.bar = Bar(640/2, 480 - 30, 50, 20)

class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model
    def handle_event(self, event):
        """ Look for left and right keypresses to
            modify the x position of the bar """
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_UP:
        	self.model.bar.top -= 10
        if event.key == pygame.K_DOWN:
        	self.model.bar.top += 10
        if event.key == pygame.K_LEFT:
            self.model.bar.left -= 10
        if event.key == pygame.K_RIGHT:
            self.model.bar.left += 10

class PyGameMouseController(object):
    def __init__(self, model):
        self.model = model
    def handle_event(self, event):
        """ Look for mouse movements and respond appropriately """
        if event.type != MOUSEMOTION:
            return
        self.model.bar.left = event.pos[0]
        self.model.bar.top = event.pos[1]

if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)

    model = MVP()
    view = EndersGameView(model, screen)
    #controller = PyGameKeyboardController(model)
    controller = PyGameMouseController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        view.draw()
        time.sleep(.001)