import pygame, random

from Constants import *

class Pipe():
    def __init__(self):
        rdmPipe = random.randint(0, len(PIPES_LIST) - 1)
        self._lPipeImg = pygame.image.load(PIPES_LIST[rdmPipe]).convert_alpha()
        self._uPipeImg = pygame.transform.flip(self._lPipeImg, False, True).convert_alpha()
        self._minY = int(BASEY - 0.1 * self._lPipeImg.get_height())
        self._maxY = int(0.1 * self._lPipeImg.get_height() + PIPEGAPSIZE)

        newPipe = self._randomPipe(hard=True)
        self._lPipes = [{'x': newPipe[0]['x'] + DISTANCE, 'y': newPipe[0]['y'], 'vel': newPipe[0]['vel'], 'min': newPipe[0]['min'], 'max': newPipe[0]['max']}]
        self._uPipes = [{'x': newPipe[1]['x'] + DISTANCE, 'y': newPipe[1]['y']}]

        self._pipeVel = -4

    def _randomPipe(self, hard=False):
        minLen = self._lPipeImg.get_height() * 0.2
        maxRandom = int(BASEY - PIPEGAPSIZE - 2 * minLen)
        lengthPipe = random.randint(0, maxRandom)
        lengthPipe += minLen
        pipeLowerY = lengthPipe + PIPEGAPSIZE

        pipeX = SCREENWIDTH
        pipeUpperY = lengthPipe - self._uPipeImg.get_height()

        velY = 0
        min = 0
        max = 0
        if hard:
            velY = random.randint(1, 3)
            randDir = random.randint(0, 100)
            if randDir >= 0 and randDir < 50:
                velY *= -1

            randY = random.randint(0, 200)
            max = pipeLowerY
            min = max + randY
            if min > self._minY:
                min = self._minY
            if min - max < 10:
                rdn = random.randint(10, 50)
                max -= rdn

        return [
            {'x': pipeX, 'y': pipeLowerY, 'vel': velY, 'min': min, 'max': max},
            {'x': pipeX, 'y': pipeUpperY}
        ]

    def _movement(self, hard=False):
        for lPipe, uPipe in zip(self._lPipes, self._uPipes):
            lPipe['x'] += self._pipeVel
            uPipe['x'] += self._pipeVel

        if self._lPipes[-1]['x'] > SCREENWIDTH - DISTANCE - 5 and self._lPipes[-1]['x'] < SCREENWIDTH - DISTANCE:
            newPipe = self._randomPipe(hard)
            self._lPipes.append(newPipe[0])
            self._uPipes.append(newPipe[1])

        if self._lPipes[0]['x'] < -(self._lPipeImg.get_width()):
            self._lPipes.pop(0)
            self._uPipes.pop(0)


    def moveUpDown(self, move):
        if move['y'] > move['min'] or move['y'] < move['max']:
            move['vel'] *= -1

    def draw(self, screen, mainGame=True, hard=False):
        if mainGame:
            self._movement(hard)
            if hard and mainGame:
                for lPipe, uPipe in zip(self._lPipes, self._uPipes):
                    self.moveUpDown(lPipe)
                    lPipe['y'] -= lPipe['vel']
                    uPipe['y'] -= lPipe['vel']

        for lPipe, uPipe in zip(self._lPipes, self._uPipes):
            screen.blit(self._lPipeImg, (lPipe['x'], lPipe['y']))
            screen.blit(self._uPipeImg, (uPipe['x'], uPipe['y']))

    def getHitmaskLowerPipe(self):
        img = self._lPipeImg
        mask = []

        for x in range(img.get_width()):
            mask.append([])
            for y in range(img.get_height()):
                mask[x].append(bool(img.get_at((x, y))[3]))
        return mask

    def getHitmaskUpperPipe(self):
        img = self._uPipeImg
        mask = []

        for x in range(img.get_width()):
            mask.append([])
            for y in range(img.get_height()):
                mask[x].append(bool(img.get_at((x, y))[3]))
        return mask

    def getWidth(self):
        return self._lPipeImg.get_width()

    def getHeight(self):
        return self._uPipeImg.get_height()

    def getUpperPipes(self):
        return self._uPipes

    def getLowerPipes(self):
        return self._lPipes

    def getInfoIA(self, birdX):
        for pipe in self._lPipes:
            if birdX < pipe['x'] + self._lPipeImg.get_width():
                return [pipe['y'] - (PIPEGAPSIZE / 2), pipe['vel']]
