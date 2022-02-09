from cgitb import reset
from posixpath import split
import pygame
from car import *
from race_track import *

#start the pygame engine
pygame.init()
pygame.font.init()


myfont = pygame.font.SysFont('Comic Sans MS', 23)

FPS = 120
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720))

player1 = Car(100,100)
AICars = []
track1 = RaceTrack("track 1")

def getUserInput():
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a]:
        player1.rotateLeft(track1.getWalls())
    elif pressed[pygame.K_d]:
        player1.rotateRight(track1.getWalls())
    if pressed[pygame.K_w]:
        player1.move(track1)
    elif pressed[pygame.K_s]:
        player1.reverse(track1.getWalls())

def drawHUD():
    textsurface = myfont.render("check point 0: " + str(player1.getCheckPoint(0)), False, (0, 0, 0))
    screen.blit(textsurface,(900,0))
    textsurface = myfont.render("check point 1: " + str(player1.getCheckPoint(1)), False, (0, 0, 0))
    screen.blit(textsurface,(900,30))
    textsurface = myfont.render("check point 2: " + str(player1.getCheckPoint(2)), False, (0, 0, 0))
    screen.blit(textsurface,(900,60))
    textsurface = myfont.render("check point 3: " + str(player1.getCheckPoint(3)), False, (0, 0, 0))
    screen.blit(textsurface,(900,90))
    textsurface = myfont.render("check point 4: " + str(player1.getCheckPoint(4)), False, (0, 0, 0))
    screen.blit(textsurface,(900,120))
    textsurface = myfont.render("laps: " + str(AICars[0].getNumLaps()), False, (0, 0, 0))
    screen.blit(textsurface,(900,150))
    textsurface = myfont.render("cars: " + str(len(AICars)), False, (0, 0, 0))
    screen.blit(textsurface,(900,180))
    textsurface = myfont.render("DNA: " + str(AICars[0].getCurrentDNA()), False, (0,0,0))
    screen.blit(textsurface,(900,210))

def createAICars():
    for i in range(100):
        AICars.append(AICar(100,100))

def moveAIs():
    for car in AICars:
        car.move(track1)

def drawAIs():
    for car in AICars:
        car.draw(screen)

def resetAllCars():
    for car in AICars:
        car.setPosition(100,100)
        car.resetDNA()
        car.resetAngles()
        car.resetGear()
        car.resetScore()
        car.resetCheckPoints()
        car.resetLaps()

def clear_screen():
    pygame.draw.rect(screen, (255,255,255), (0, 0, 1280, 720))

def createTrack1():
    track1.addRect(pygame.Rect(0,0,800,25))
    track1.addRect(pygame.Rect(800,0,25,325))
    track1.addRect(pygame.Rect(810,300,300,25))
    track1.addRect(pygame.Rect(1100,300,25,300))
    track1.addRect(pygame.Rect(0,600,1125,25))
    track1.addRect(pygame.Rect(0,0,25,600))
    track1.addRect(pygame.Rect(200,200,400,25))
    track1.addRect(pygame.Rect(200,200,25,250))
    track1.addRect(pygame.Rect(600,200,25,200))
    track1.addRect(pygame.Rect(600,400,150,25))
    track1.addRect(pygame.Rect(750,400,25,100))
    track1.addRect(pygame.Rect(200,400,400,25))

    track1.addCheckPoint(pygame.Rect(500,0,25,200))
    track1.addCheckPoint(pygame.Rect(600,300,200,25))
    track1.addCheckPoint(pygame.Rect(500,425,25,200))
    track1.addCheckPoint(pygame.Rect(0,400,200,25))
    track1.addCheckPoint(pygame.Rect(0,200,200,25))

def killBottomHalf():
    global AICars
    '''for i in range(0, len(AICars)):
        for j in range(0, len(AICars)-1):
            if AICars[i].getScore() < AICars[j+1].getScore():
                temp = AICars[j]
                AICars[j] = AICars[j+1]
                AICars[j+1] = temp'''
    AICars = AICars[:int(len(AICars)/2)]

def makeCarBabies():
    if (len(AICars) == 50):
        Car1 = AICars[0]
    else:
        Car1 = AICars[random.randint(0,len(AICars)-1)]
    Car2 = AICars[random.randint(0,len(AICars)-1)]
    Split = random.randint(0,1000)
    temp = AICar(100,100)

    for i in range(0,Split):
        temp.appendDNA(Car1.getDNA()[i])
    for j in range(Split,1000-Split):
        temp.appendDNA(Car2.getDNA()[j])

    temp.mutate()
    AICars.append(temp)


createTrack1()
createAICars()
while True:
    #loop through and empty the event queue, key presses
    #buttons, clicks, etc.
    for event in pygame.event.get():
        #if the event is a click on the "X" close button
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.shiftUp()
            if event.key == pygame.K_DOWN:
                player1.shiftDown()

    getUserInput()
    clear_screen()

    drawAIs()
    moveAIs()
    track1.drawRaceTrack(screen)
    player1.draw(screen)
    drawHUD()
    pygame.display.flip()
    fpsClock.tick(FPS)

    if (AICars[0].getCurrentDNA() >= 2500):
        AICars.sort(key=lambda x: x.getScore(), reverse=True)
        killBottomHalf()
        resetAllCars()
        for i in range(50):
            makeCarBabies()
        