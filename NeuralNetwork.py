import numpy as np
import random


class NeuralNetwork:
    def __init__(self, nInputs, nHiddens, nOutputs):
        self.input = []
        self.hidden = 0
        self.output = 0
        self.wInput = []
        self.bHidden = []
        self.wHidden = []
        self.bOutput = []
        createMatrix(self.wInput, nInputs, nHiddens)
        createMatrix(self.wHidden, nHiddens, nOutputs)
        createMatrix(self.bHidden, 1, nHiddens)
        createMatrix(self.bOutput, 1, nOutputs)

    def feedforward(self, *inputs):
        for i in inputs:
            self.input.append(i)
        self.hidden = activationReLU(np.dot(self.input, self.wInput) + self.bHidden)
        self.output = activationReLU(np.dot(self.hidden, self.wHidden) + self.bOutput)
        self.input = []

    def mutation(self, wI, wH, bH, bO, error):
        randomMutation(self.wInput, wI, error)
        randomMutation(self.wHidden, wH, error)
        randomMutation(self.bHidden, bH, error)
        randomMutation(self.bOutput, bO, error)

    def customBrain(self, wi, wh, bh, bo):
        self.wInput = wi
        self.wHidden = wh
        self.bHidden = bh
        self.bOutput = bo

def activationReLU(input):
    result = []
    for x in range(len(input)):
        result.append([])
        for y in range(len(input[x])):
            if input[x][y] < 0:
                result[x].append(0)
            else:
                result[x].append(input[x][y])
    return result

def createMatrix(list, lines, col):
    for i in range(lines):
        list.append([])
        for j in range(col):
            list[i].append(random.uniform(-1, 1))

def randomMutation(matrix, best, error):
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            rdn = random.uniform(best[x][y] - error, best[x][y] + error)
            matrix[x][y] = rdn
