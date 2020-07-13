import pygame
from pygame.locals import *
import sys
import random
import time
import sqlite3
import os

from Constants import *
from Bird import Bird
from Base import Base
from Pipe import Pipe
from Collision import *
from NeuralNetwork import NeuralNetwork
from Load import loadNetwork

IMAGES, SOUNDS, HITMASK, OBJECTS = {}, {}, {}, {}

def menu():
    pygame.init()
    global SCREEN, CLOCK

    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')
    CLOCK = pygame.time.Clock()

    IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[0]).convert()
    OBJECTS['base'] = Base()
    OBJECTS['bird'] = Bird()
    OBJECTS['bird'].setPosition()

    click = False
    while True:
        SCREEN.blit(IMAGES['background'], (0, 0))
        OBJECTS['base'].draw(SCREEN)

        OBJECTS['bird'].moveWelcome()
        OBJECTS['bird'].draw(SCREEN, False)

        posX = int(SCREENWIDTH / 2 - 30)
        playButton = pygame.Rect((posX, 100), (45, 30))
        trainIAButton = pygame.Rect((posX - 110, 150), (290, 30))
        matchButton = pygame.Rect((posX-140, 200), (350, 30))
        quitButton = pygame.Rect((posX, 250), (50, 30))

        black = (0, 0, 0)
        drawText(posX, 100, 'Play', black, 40)
        drawText(posX - 110, 150, 'Train a Neural Network', black, 40)
        drawText(posX - 140, 200, 'Play against Neural Network', black, 40)
        drawText(posX, 250, 'Quit', black, 40)

        mx, my = pygame.mouse.get_pos()

        if playButton.collidepoint((mx, my)):
            if click:
                mode = options(local=True)
                if mode == 'solo':
                    options(play=True, solo=True)
                else:
                    options(play=True, solo=False)

        if trainIAButton.collidepoint((mx, my)):
            if click:
                train()

        if matchButton.collidepoint((mx, my)):
            if click:
                file = options(ia=True)
                if file != None:
                    path = os.path.join(os.path.abspath(os.getcwd()), file + ".txt")
                    if os.path.isfile(path):
                        difficulty = options(nn=True)
                        if difficulty != None:
                            match(file, difficulty)
                    else:
                        options(error=True)

        if quitButton.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        if click:
            click = False
            OBJECTS['bird'] = Bird()
            OBJECTS['bird'].setPosition()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button:
                    click = True

        pygame.display.update()
        CLOCK.tick(FPS)

def options(play=False, local=False, solo=False, nn=False, ia=False, error=False):
    click = False
    button = False
    while True:
        SCREEN.blit(IMAGES['background'], (0, 0))
        OBJECTS['base'].draw(SCREEN)
        OBJECTS['bird'].moveWelcome()
        OBJECTS['bird'].draw(SCREEN, False)

        posX = int(SCREENWIDTH / 2 - 30)
        mx, my = pygame.mouse.get_pos()
        color = SCREEN.get_at((posX, 150))
        black = (0, 0, 0)
        if play or nn:
            easyButton = pygame.Rect((posX, 150), (50, 30))
            hardButton = pygame.Rect((posX, 200), (50, 30))

            drawText(posX, 150, 'Easy', black, 40)
            drawText(posX, 200, 'Hard', black, 40)

            if easyButton.collidepoint((mx, my)):
                if click:
                    button = True
                    if play:
                        if solo:
                            normal(False)
                        else:
                            matchX1(False)

                    if nn:
                        return False

            if hardButton.collidepoint((mx, my)):
                if click:
                    button = True
                    if play:
                        if solo:
                            normal(True)
                        else:
                            matchX1(True)

                    if nn:
                        return True
        elif local:
            soloButton = pygame.Rect((posX, 150), (50, 30))
            pairButton = pygame.Rect((posX - 90, 200), (230, 30))

            drawText(posX, 150, 'Solo', black, 40)
            drawText(posX - 90, 200, 'Player1 vs Player2', black, 40)

            if soloButton.collidepoint((mx, my)):
                if click:
                    return 'solo'

            if pairButton.collidepoint((mx, my)):
                if click:
                    return 'pair'

        elif ia:
            trainedButton = pygame.Rect((posX - 30, 150), (135, 30))
            iaButton = pygame.Rect((posX - 20, 200), (125, 30))

            drawText(posX - 30, 150, 'Trainded IA', black, 40)
            drawText(posX - 20, 200, 'Default IA', black, 40)

            if trainedButton.collidepoint((mx, my)):
                if click:
                    return "TrainedNetwork"
            if iaButton.collidepoint((mx, my)):
                if click:
                    return "Network"
        else:
            errorButton1 = pygame.Rect((posX-100, 150), (300, 30))
            errorButton2 = pygame.Rect((posX-180, 200), (450, 30))

            drawText(posX - 100, 150, 'You need to have some', black, 40)
            drawText(posX - 180, 200, 'trained neural network to continue', black, 40)

            if errorButton1.collidepoint((mx, my)) or errorButton2.collidepoint((mx, my)):
                if click:
                    return 


        if click and not button:
            click = False
        elif click and button:
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            if event.type == MOUSEBUTTONDOWN:
                if event.button:
                    click = True

        pygame.display.update()
        CLOCK.tick(FPS)


def normal(difficulty):
    insert = False
    path = os.path.join(os.path.abspath(os.getcwd()), "registers.db")
    if not os.path.isfile(path):
        insert = True

    connection = sqlite3.connect("registers.db")
    sql = connection.cursor()

    sql.execute(''' CREATE TABLE IF NOT EXISTS score (
                        recordEasy INT(10),
                        recordHard INT(10)
                    );''')

    if insert:
        sql.execute(''' INSERT INTO score (recordEasy, recordHard)
                        VALUES (0, 0)''')

    connection.commit()

    IMAGES['message'] = pygame.image.load('assets/images/message.png').convert_alpha()
    IMAGES['numbers'] = (
        pygame.image.load('assets/images/0.png').convert_alpha(),
        pygame.image.load('assets/images/1.png').convert_alpha(),
        pygame.image.load('assets/images/2.png').convert_alpha(),
        pygame.image.load('assets/images/3.png').convert_alpha(),
        pygame.image.load('assets/images/4.png').convert_alpha(),
        pygame.image.load('assets/images/5.png').convert_alpha(),
        pygame.image.load('assets/images/6.png').convert_alpha(),
        pygame.image.load('assets/images/7.png').convert_alpha(),
        pygame.image.load('assets/images/8.png').convert_alpha(),
        pygame.image.load('assets/images/9.png').convert_alpha()
    )
    IMAGES['gameover'] = pygame.image.load('assets/images/gameover.png').convert_alpha()

    if 'win' in sys.platform:
        extension = '.wav'
    else:
        extension = '.ogg'
    SOUNDS['wing']  = pygame.mixer.Sound('assets/audio/wing' + extension)
    SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point' + extension)
    SOUNDS['hit']   = pygame.mixer.Sound('assets/audio/hit' + extension)
    SOUNDS['die']   = pygame.mixer.Sound('assets/audio/die' + extension)

    apresentation = False
    while True:
        OBJECTS['bird'] = Bird()
        OBJECTS['bird'].setPosition()
        OBJECTS['base'] = Base()
        OBJECTS['pipe'] = Pipe()

        HITMASK['bird'] = (
            OBJECTS['bird'].getHitmask(0),
            OBJECTS['bird'].getHitmask(1),
            OBJECTS['bird'].getHitmask(2)
        )

        HITMASK['pipe'] = (
            OBJECTS['pipe'].getHitmaskLowerPipe(),
            OBJECTS['pipe'].getHitmaskUpperPipe()
        )

        rdmBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[rdmBg]).convert()

        if difficulty:
            sql.execute('''SELECT recordHard FROM score''')
            record = int(sql.fetchall()[0][0])
        else:
            sql.execute(''' SELECT recordEasy FROM score''')
            record = int(sql.fetchall()[0][0])

        if not apresentation:
            if welcomeAnimation():
                break
        apresentation = True
        score = 0
        if normalGame(score, difficulty, record):
            break

def welcomeAnimation():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return True

            if event.type == KEYDOWN and (event.key ==  K_SPACE or event.key == K_UP):
                SOUNDS['wing'].play()
                return False

        OBJECTS['bird'].moveWelcome()

        SCREEN.blit(IMAGES['background'], (0, 0))
        OBJECTS['base'].draw(SCREEN)
        OBJECTS['bird'].draw(SCREEN, False)

        messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
        messagey = int(SCREENHEIGHT * 0.12)
        SCREEN.blit(IMAGES['message'], (messagex, messagey))

        pygame.display.update()
        CLOCK.tick(FPS)

def normalGame(score, difficulty, record):
    while True:
        flap = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                if pause():
                    return True

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                SOUNDS['wing'].play()
                flap = True

        collision = Collision(OBJECTS['bird'], OBJECTS['pipe'], HITMASK)
        infoCollision = collision.checkCollision()
        if infoCollision[0]:
            if gameOver({'collision': infoCollision, 'score': score, 'difficulty': difficulty, 'record': record}):
                return True
            else:
                return False

        SCREEN.blit(IMAGES['background'], (0, 0))
        OBJECTS['pipe'].draw(SCREEN, hard=difficulty)
        OBJECTS['base'].draw(SCREEN)
        OBJECTS['bird'].draw(SCREEN)
        OBJECTS['bird'].movement(flap)

        score = showScore(score)

        stringRecord = "Record: " + str(record)
        drawText(10, 10, stringRecord, (255, 255, 255), 35)

        pygame.display.update()
        CLOCK.tick(FPS)

def gameOver(info):
    SOUNDS['hit'].play()
    if info['collision'][1] == 'pipe':
        SOUNDS['die'].play()

    update = True
    while True:
        playery = OBJECTS['bird'].getPlayery()
        playerHeight = OBJECTS['bird'].getHeight(OBJECTS['bird'].getPlayerIndex())
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return True

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight > BASEY:
                    return False

        SCREEN.blit(IMAGES['background'], (0, 0))
        OBJECTS['pipe'].draw(SCREEN, False)
        OBJECTS['base'].draw(SCREEN, False)
        OBJECTS['bird'].draw(SCREEN, gameOver=True)

        showScore(info['score'], True)
        SCREEN.blit(IMAGES['gameover'], (200, 180))

        conn = sqlite3.connect("registers.db")
        sql = conn.cursor()

        if info['score'] > info['record'] and update:
            update = False
            score = info['score']
            if info['difficulty']:
                sql.execute(f'''UPDATE score SET recordHard = '{score}' ''')
            else:
                sql.execute(f'''UPDATE score SET recordEasy = '{score}' ''')

            conn.commit()

        pygame.display.update()
        CLOCK.tick(FPS)

def showScore(score, gameOver=False):
    if not gameOver:
        playerWidth = OBJECTS['bird'].getWidth(OBJECTS['bird'].getPlayerIndex())
        playerX = OBJECTS['bird'].getPlayerx()
        playerMid = playerX + playerWidth / 2
        pipes = OBJECTS['pipe'].getLowerPipes()
        pipeWidth = OBJECTS['pipe'].getWidth()
        for pipe in pipes:
            pipeMid = pipe['x'] + pipeWidth / 2
            if playerMid > pipeMid and playerMid < pipeMid + 4:
                score += 1
                SOUNDS['point'].play()

    listScore = list(str(score))
    i = 0
    totalWidth = 0
    for digit in listScore:
        digit = int(digit)
        listScore[i] = digit
        totalWidth += IMAGES['numbers'][digit].get_width()
        i += 1

    scoreX = (SCREENWIDTH - totalWidth) / 2

    for digit in listScore:
        SCREEN.blit(IMAGES['numbers'][digit], (scoreX, SCREENHEIGHT * 0.1))
        scoreX += IMAGES['numbers'][digit].get_width()

    return score

def matchX1(difficulty):
    if 'win' in sys.platform:
        extension = '.wav'
    else:
        extension = '.ogg'

    SOUNDS['hit']   = pygame.mixer.Sound('assets/audio/hit' + extension)

    while True:
        OBJECTS['bird'] = [Bird(), Bird()]

        OBJECTS['base'] = Base()
        OBJECTS['pipe'] = Pipe()

        HITMASK['bird'] = []
        for bird in range(2):
            HITMASK['bird'].append((
                OBJECTS['bird'][bird].getHitmask(0),
                OBJECTS['bird'][bird].getHitmask(1),
                OBJECTS['bird'][bird].getHitmask(2)
            ))

        HITMASK['pipe'] = (
            OBJECTS['pipe'].getHitmaskLowerPipe(),
            OBJECTS['pipe'].getHitmaskUpperPipe()
        )

        rdmBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[rdmBg]).convert()

        if gameX1(difficulty):
            break

def gameX1(difficulty):
    dead = [False, False]
    sound = [False, False]

    iterMessage = 0
    while True:
        flap1 = False
        flap2 = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                if pause():
                    return True

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    flap1 = True
                elif event.key == K_UP:
                    flap2 = True

        collision = CollisionIA(OBJECTS['bird'], OBJECTS['pipe'], HITMASK)
        infoCollision = collision.checkCollision()

        if infoCollision[0]:
            dead[0] = True
            if not sound[0]:
                SOUNDS['hit'].play()
                sound[0] = True

        if infoCollision[1]:
            dead[1] = True
            if not sound[1]:
                SOUNDS['hit'].play()
                sound[1] = True

        SCREEN.blit(IMAGES['background'], (0, 0))
        OBJECTS['pipe'].draw(SCREEN, hard=difficulty)
        OBJECTS['base'].draw(SCREEN)

        if not dead[0]:
            OBJECTS['bird'][0].draw(SCREEN)
            OBJECTS['bird'][0].movement(flap1)
        else:
            OBJECTS['bird'][0].draw(SCREEN, gameOver=True, backwards=True)

        if not dead[1]:
            OBJECTS['bird'][1].draw(SCREEN)
            OBJECTS['bird'][1].movement(flap2)
        else:
            OBJECTS['bird'][1].draw(SCREEN, gameOver=True, backwards=True)

        if dead[0] and dead[1]:
            return False

        if iterMessage < 100:
            drawText(10, 10, 'P1 use space and P2 use up arrow', (255, 255, 255), 30)
            if iterMessage < 50:
                drawText(OBJECTS['bird'][0].getPlayerx(), OBJECTS['bird'][0].getPlayery() - 20, 'P1', (255, 255, 255), 30)
                drawText(OBJECTS['bird'][1].getPlayerx(), OBJECTS['bird'][1].getPlayery() - 20, 'P2', (255, 255, 255), 30)
            iterMessage += 1

        pygame.display.update()
        CLOCK.tick(FPS)

def train():
    generation = 0
    brain = []
    record = 0
    bestBird = NeuralNetwork(INPUT, HIDDEN, OUTPUT)
    velGame = 0

    info = {'close': False, 'brain': brain, 'generation': generation, 'record': record, 'bestBird': bestBird, 'velGame': velGame}
    for i in range(BIRDS):
        brain.append(NeuralNetwork(INPUT, HIDDEN, OUTPUT))

    start = time.time()
    while True:
        OBJECTS['bird'] = []
        HITMASK['bird'] = []
        for bird in range(BIRDS):
            OBJECTS['bird'].append(Bird())
            HITMASK['bird'].append((
                OBJECTS['bird'][bird].getHitmask(0),
                OBJECTS['bird'][bird].getHitmask(1),
                OBJECTS['bird'][bird].getHitmask(2)
            ))
        OBJECTS['base'] = Base()
        OBJECTS['pipe'] = Pipe()

        HITMASK['pipe'] = (
            OBJECTS['pipe'].getHitmaskLowerPipe(),
            OBJECTS['pipe'].getHitmaskUpperPipe()
        )

        rdmBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[rdmBg]).convert()

        if not info['close']:
            info = trainGame(info['brain'], info['generation'], info['record'], info['bestBird'], info['velGame'])
        else:
            break

    end = time.time()
    t = end - start
    hour = int(t / 3600)
    min = int((t % 3600) / 60)
    sec = int((t % 3600) % 60)
    stringTime = 'Time:' + str(hour) + 'h ' + str(min) + 'm ' + str(sec) + 's'
    drawText(10, 35, stringTime, (0, 0, 0), 35)
    pygame.display.update()
    time.sleep(3)

def trainGame(brain, generation, record, bestBird, velGame):
    live = 0
    deads = []
    fitness = []
    for i in range(len(OBJECTS['bird'])):
        deads.append(False)
        fitness.append(0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                drawText(10, 10, "Extracting neural network...", (0, 0, 0), 35)
                pygame.display.update()
                time.sleep(1)
                neuralFile = open("TrainedNetwork.txt", "w")
                list = []
                list.append(str(bestBird.wInput) + "\n")
                list.append(str(bestBird.wHidden) + "\n")
                list.append(str(bestBird.bHidden) + "\n")
                list.append(str(bestBird.bOutput) + "\n")

                neuralFile.writelines(list)

                neuralFile.close()

                return {'close': True, 'brain': brain, 'generation': generation, 'record': record, 'bestBird': bestBird, 'velGame': velGame}

            if event.type == KEYDOWN and event.key == K_RIGHT:
                    if velGame < 100:
                        velGame += 10

            if event.type == KEYDOWN and event.key == K_LEFT:
                if velGame > -20:
                    velGame -= 10

        SCREEN.blit(IMAGES['background'], (0, 0))
        OBJECTS['pipe'].draw(SCREEN, hard=True)
        OBJECTS['base'].draw(SCREEN)

        collision = CollisionIA(OBJECTS['bird'], OBJECTS['pipe'], HITMASK)
        infoCollision = collision.checkCollision()

        for bird in range(BIRDS):
            if not infoCollision[bird] and not deads[bird]:
                live += 1
                pipeInfo = OBJECTS['pipe'].getInfoIA(OBJECTS['bird'][bird].getPlayerx())
                distY = pipeInfo[0] - OBJECTS['bird'][bird].getPlayery()
                brain[bird].feedforward(distY, pipeInfo[1])

                if brain[bird].output[0][0] > 0:
                        OBJECTS['bird'][bird].movement(True)
                else:
                        OBJECTS['bird'][bird].movement(False)

                OBJECTS['bird'][bird].draw(SCREEN)

                fitness[bird] += 1
            else:
                OBJECTS['bird'][bird].draw(SCREEN, gameOver=True, backwards=True)
                deads[bird] = True

        stringGen = 'Generation: ' + str(generation)
        stringLive = 'Live: ' + str(live)
        stringRecord = 'Record: ' + str(record)
        drawText(420, 10, stringGen, (255, 255, 255), 30)
        drawText(420, 40, stringLive, (255, 255, 255), 30)
        drawText(420, 70, stringRecord, (255, 255, 255), 30)

        if live == 0:
            max = 0
            for i in range(len(fitness)):
                if fitness[i] > fitness[max]:
                    max = i

            if fitness[max] > record:
                record = fitness[max]

            bestBird = brain[max]

            for i in range(BIRDS):
                rdn = random.randint(0, 100)
                if rdn <= 10:
                    error = 0.5
                else:
                    error = random.uniform(0.1, 0.3)
                if i != max:
                    brain[i].mutation(bestBird.wInput, bestBird.wHidden, bestBird.bHidden, bestBird.bOutput, error)

            generation += 1
            return {'close': False, 'brain': brain, 'generation': generation, 'record': record, 'bestBird': bestBird, 'velGame': velGame}

        live = 0
        pygame.display.update()
        CLOCK.tick(FPS + velGame)

def match(file, difficulty):
    while True:
        OBJECTS['bird'] = []
        HITMASK['bird'] = []
        for bird in range(2):
            OBJECTS['bird'].append(Bird())
            HITMASK['bird'].append((
                OBJECTS['bird'][bird].getHitmask(0),
                OBJECTS['bird'][bird].getHitmask(1),
                OBJECTS['bird'][bird].getHitmask(2)
            ))


        OBJECTS['base'] = Base()
        OBJECTS['pipe'] = Pipe()

        HITMASK['pipe'] = (
            OBJECTS['pipe'].getHitmaskLowerPipe(),
            OBJECTS['pipe'].getHitmaskUpperPipe()
        )

        if 'win' in sys.platform:
            extension = '.wav'
        else:
            extension = '.ogg'
        SOUNDS['wing']  = pygame.mixer.Sound('assets/audio/wing' + extension)
        SOUNDS['hit']   = pygame.mixer.Sound('assets/audio/hit' + extension)

        rdmBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[rdmBg]).convert()

        if matchGame(file, difficulty):
            break


def matchGame(file, difficulty):
    nn = loadNetwork(file)
    dead = [False, False]
    sound = False

    iterMessage = 0
    while True:
        flap = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                if pause():
                    return True

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if not dead[0]:
                    SOUNDS['wing'].play()
                    flap = True

            if event.type == KEYDOWN and event.key == K_RETURN:
                return False

        collision = CollisionIA(OBJECTS['bird'], OBJECTS['pipe'], HITMASK)
        infoCollision = collision.checkCollision()

        if infoCollision[0]:
            dead[0] = True
            if not sound:
                SOUNDS['hit'].play()
                sound = True

        if infoCollision[1]:
            dead[1] = True

        SCREEN.blit(IMAGES['background'], (0, 0))
        OBJECTS['pipe'].draw(SCREEN, hard=difficulty)
        OBJECTS['base'].draw(SCREEN)
        if not dead[0]:
            OBJECTS['bird'][0].draw(SCREEN)
            OBJECTS['bird'][0].movement(flap)
        else:
            OBJECTS['bird'][0].draw(SCREEN, gameOver=True, backwards=True)

        if not dead[1]:
            pipeInfo = OBJECTS['pipe'].getInfoIA(OBJECTS['bird'][1].getPlayerx())
            distY = pipeInfo[0] - OBJECTS['bird'][1].getPlayery()
            nn.feedforward(distY, pipeInfo[1])
            if nn.output[0][0] > 0:
                    OBJECTS['bird'][1].movement(True)
            else:
                    OBJECTS['bird'][1].movement(False)

            OBJECTS['bird'][1].draw(SCREEN)
        else:
            OBJECTS['bird'][1].draw(SCREEN, gameOver=True, backwards=True)

        if iterMessage < 100:
            drawText(10, 10, 'Click ENTER for restart', (255, 255, 255), 30)
            if iterMessage < 50:
                drawText(OBJECTS['bird'][0].getPlayerx(), OBJECTS['bird'][0].getPlayery() - 20, 'You', (255, 255, 255), 30)
            iterMessage += 1

        pygame.display.update()
        CLOCK.tick(FPS)

def pause():
    click = False
    button = False
    background = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
    background.fill((0, 0, 0))
    background.set_alpha(1)
    for i in range(20):
        SCREEN.blit(background, (0, 0))

    posX = int(SCREENWIDTH / 2 - 30)
    continueButton = pygame.Rect((posX - 20, 150), (100, 30))
    backButton = pygame.Rect((posX, 200), (50, 30))

    while True:
        drawText(posX - 20, 150, 'Continue', (0, 0, 0), 40)
        drawText(posX, 200, 'Back', (0, 0, 0), 40)

        mx, my = pygame.mouse.get_pos()

        if continueButton.collidepoint((mx, my)):
            if click:
                button = True
                return False
        if backButton.collidepoint((mx, my)):
            if click:
                button = True
                return True

        if click and not button:
            click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                click = True

        pygame.display.update()
        CLOCK.tick(FPS)

def drawText(x, y, text, color, size):
    font = pygame.font.Font("assets/font/flappy-bird-font.ttf", size)
    txtObj = font.render(text, 1, color)
    txtRect = txtObj.get_rect()
    txtRect.topleft = (x, y)
    SCREEN.blit(txtObj, txtRect)


menu()
