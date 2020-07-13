import pygame
from Constants import *

class Base():
    def __init__(self):
        self.__basey = SCREENHEIGHT * 0.79
        self._basex = 0
        self._img = pygame.image.load('assets/images/base.png').convert_alpha()
        self._baseShift = self._img.get_width() - SCREENWIDTH


    def draw(self, screen, mainGame=True):
        if mainGame:
            self.moveBase()
        screen.blit(self._img, (self._basex, self.__basey))


    def moveBase(self):
        self._basex = -((-self._basex + 4) % self._baseShift)
