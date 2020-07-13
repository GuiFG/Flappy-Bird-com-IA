import pygame, random

from Constants import *

class Bird():
    def __init__(self):
        randomIndex = random.randint(0, len(PLAYERS_LIST) - 1)
        self._img = (
            pygame.image.load(PLAYERS_LIST[randomIndex][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randomIndex][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randomIndex][2]).convert_alpha()
        )
        self.__playerx = random.randint(0, int(SCREENWIDTH * 0.4))
        self._playery = random.randint(self._img[0].get_height(), int((BASEY - self._img[0].get_height())))
        self._playerIndex = 0
        self._iter = 0
        self._listIndex = [0, 1, 2, 1]
        self._index = 0
        self._moveyStart = {'val': 0, 'dir': 1}
        self._vel = -9
        self._gravity = 1
        self._maxVel = 9
        self._rotation = 45
        self._rotVel = 3

    def moveWelcome(self):
        if abs(self._moveyStart['val']) == 8:
            self._moveyStart['dir'] *= -1

        if self._moveyStart['dir'] == 1:
            self._moveyStart['val'] += 1
        else:
            self._moveyStart['val'] -= 1

    def movement(self, flapped):
        if flapped:
            if self._playery > 0:
                self._vel = -9
                self._rotation = 45

        if self._vel < self._maxVel:
            self._vel += self._gravity

        if self._rotation > -90:
            self._rotation -= self._rotVel

        if self._playery + self._img[0].get_height() <= BASEY:
            self._playery += self._vel

    def moveWing(self):
        if (self._iter % 5 == 0):
            self._playerIndex = self._listIndex[self._index]
            self._index = (self._index + 1) % 4
        self._iter += 1

    def draw(self, screen, mainGame=True, gameOver=False, backwards=False):
        if gameOver:
            self._rotVel = 7
            if self._playery + self._img[0].get_height() <= BASEY:
                self.movement(False)
            if backwards:
                self.__playerx -= 4
        else:
            self.moveWing()

        if mainGame:
            playerSurface = pygame.transform.rotate(self._img[self._playerIndex], self._rotation)
            screen.blit(playerSurface, (self.__playerx, self._playery))
        else:
            screen.blit(self._img[self._playerIndex], (self.__playerx, self._playery + self._moveyStart['val']))

    def getHitmask(self, playerIndex):
        mask = []

        for x in range(self._img[playerIndex].get_width()):
            mask.append([])
            for y in range(self._img[playerIndex].get_height()):
                mask[x].append(bool(self._img[playerIndex].get_at((x,y))[3]))
        return mask

    def getWidth(self, playerIndex):
        return self._img[playerIndex].get_width()

    def getHeight(self, playerIndex):
        return self._img[playerIndex].get_height()

    def getPlayerIndex(self):
        return self._playerIndex

    def getPlayerx(self):
        return self.__playerx

    def getPlayery(self):
        return self._playery

    def setPosition(self):
        self.__playerx = 0.1 * SCREENWIDTH
        self._playery = (SCREENHEIGHT - self._img[0].get_height()) / 2
