import pygame

from Bird import Bird
from Base import Base
from Pipe import Pipe
from Constants import *

class Collision():
    def __init__(self, bird, pipe, hitmask):
        self.bird = bird
        self.pipe = pipe
        self.playerX = bird.getPlayerx()
        self.playerY = bird.getPlayery()
        self.playerIndex = bird.getPlayerIndex()
        self.playerWidth = bird.getWidth(self.playerIndex)
        self.playerHeight = bird.getHeight(self.playerIndex)
        self.lowerPipes = pipe.getLowerPipes()
        self.upperPipes = pipe.getUpperPipes()
        self.pipeWidth = pipe.getWidth()
        self.pipeHeight = pipe.getHeight()
        self.hitmask = hitmask

    def checkCollision(self):
        if self.playerHeight + self.playerY > BASEY:
            return [True, 'ground']
        else:
            playerRect = pygame.Rect(self.playerX, self.playerY, self.playerWidth, self.playerHeight)

            for lPipe, uPipe in zip(self.lowerPipes, self.upperPipes):
                lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], self.pipeWidth, self.pipeHeight)
                uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], self.pipeWidth, self.pipeHeight)

                crashLower = self.analysesPixel(playerRect, lPipeRect, self.playerIndex, 0)
                crashUpper = self.analysesPixel(playerRect, uPipeRect, self.playerIndex, 1)

                if crashLower or crashUpper:
                    return [True, 'pipe']

        return [False, '']

    def analysesPixel(self, playerRect, pipeRect, playerIndex, pipeIndex):
        rectOverlap = playerRect.clip(pipeRect)

        if rectOverlap.width == 0:
            return False

        playerHitmask = self.hitmask['bird'][playerIndex]
        pipeHitmask = self.hitmask['pipe'][pipeIndex]

        distX, distY = rectOverlap.x - playerRect.x, rectOverlap.y - playerRect.y

        for x in range(rectOverlap.width):
            for y in range(rectOverlap.height):
                if playerHitmask[distX + x][distY + y] and pipeHitmask[x][y]:
                    return True
        return False

class CollisionIA():
    def __init__(self, birds, pipe, hitmask):
        self.birds = birds
        self.pipe = pipe
        self.playerX = []
        self.playerY = []
        self.playerIndex = []
        self.playerWidth = []
        self.playerHeight = []
        for i, bird in enumerate(self.birds):
            self.playerX.append(bird.getPlayerx())
            self.playerY.append(bird.getPlayery())
            self.playerIndex.append(bird.getPlayerIndex())
            self.playerWidth.append(bird.getWidth(self.playerIndex[i]))
            self.playerHeight.append(bird.getHeight(self.playerIndex[i]))
        self.lowerPipes = pipe.getLowerPipes()
        self.upperPipes = pipe.getUpperPipes()
        self.pipeWidth = pipe.getWidth()
        self.pipeHeight = pipe.getHeight()
        self.hitmask = hitmask
        self.infoCollision = []
        for i in range(len(self.birds)):
            self.infoCollision.append(False)

    def checkCollision(self):
        for i in range(len(self.birds)):
            if self.playerHeight[i] + self.playerY[i] > BASEY:
                self.infoCollision[i] = True
            else:
                playerRect = pygame.Rect(self.playerX[i], self.playerY[i], self.playerWidth[i], self.playerHeight[i])

                for lPipe, uPipe in zip(self.lowerPipes, self.upperPipes):
                    lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], self.pipeWidth, self.pipeHeight)
                    uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], self.pipeWidth, self.pipeHeight)

                    crashLower = self.analysesPixel(playerRect, lPipeRect, self.playerIndex[i], i, 0)
                    crashUpper = self.analysesPixel(playerRect, uPipeRect, self.playerIndex[i], i, 1)

                    if crashLower or crashUpper:
                        self.infoCollision[i] = True

        return self.infoCollision


    def analysesPixel(self, playerRect, pipeRect, playerIndex, indexBird, pipeIndex):
        rectOverlap = playerRect.clip(pipeRect)

        if rectOverlap.width == 0:
            return False

        playerHitmask = self.hitmask['bird'][indexBird][playerIndex]
        pipeHitmask = self.hitmask['pipe'][pipeIndex]

        distX, distY = rectOverlap.x - playerRect.x, rectOverlap.y - playerRect.y

        for x in range(rectOverlap.width):
            for y in range(rectOverlap.height):
                if playerHitmask[distX + x][distY + y] and pipeHitmask[x][y]:
                    return True
        return False
