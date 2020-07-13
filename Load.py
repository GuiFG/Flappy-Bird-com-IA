from NeuralNetwork import NeuralNetwork
from Constants import *

def getMatrix(numbers, indexNum, matrix, lines, columns):
    for i in range(lines):
        matrix.append([])
        for j in range(columns):
            matrix[i].append(numbers[indexNum])
            indexNum += 1

    return [matrix, indexNum]

def getWeights(valuesNetwork):
    numbers = []
    for values in valuesNetwork:
        string = str()
        for element in values:
            if element not in '[],\n':
                if element != ' ':
                    string += element
                else:
                    numbers.append(float(string))
                    string = str()
        numbers.append(float(string))

    indexNum = 0
    info = getMatrix(numbers, indexNum, [], INPUT, HIDDEN)
    wInput, indexNum = info[0], info[1]
    info = getMatrix(numbers, indexNum, [], HIDDEN, OUTPUT)
    wHidden, indexNum = info[0], info[1]
    info = getMatrix(numbers, indexNum, [], 1, HIDDEN)
    bHidden, indexNum = info[0], info[1]
    info = getMatrix(numbers, indexNum, [], 1, OUTPUT)
    bOutput, indexNum = info[0], info[1]

    return {'wInput': wInput, 'wHidden': wHidden, 'bHidden': bHidden, 'bOutput': bOutput}

def loadNetwork(fileName):
    fileName += ".txt"
    network = open(fileName, "r")
    valuesNetwork = network.readlines()

    info = getWeights(valuesNetwork)
    brain = NeuralNetwork(INPUT, HIDDEN, OUTPUT)
    brain.customBrain(info['wInput'], info['wHidden'], info['bHidden'], info['bOutput'])

    return brain
