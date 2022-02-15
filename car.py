import math
from operator import and_
import random

import pygame

pygame.font.init()

#changed two things:
    #removed collision detection on changing of angle, the car can ALWAYS rotate now
    #changed collision detection to check which side of car is colliding and allowing it to continue moving
    #    in the opposite axis of the collision

class Car:

    new_rect = pygame.Rect(0,0,1,1)
    numLaps = 0
    myfont = pygame.font.SysFont('Comic Sans MS', 15)


    #constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.length = 15
        self.angle = 0
        self.speed = 1
        self.gear = 1
        self.score = 0
        self.checkPoints = [False, False, False, False, False]
        loadImage = pygame.image.load("small car.png")
        var = pygame.PixelArray(loadImage)
        var.replace((0,255,30), (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        del var
        self.image = pygame.transform.scale(loadImage,(15,15))
        self.myRect = pygame.Rect(self.x, self.y, self.width, self.length)

    def rotateLeft(self, track):
        oldAngle = self.angle
        self.angle = (self.angle+5) % 360
        #for rectangle in track:
        #    if pygame.Rect.colliderect(rectangle, self.new_rect):
        #        self.angle = oldAngle

    def canRotateLeft(self, track):
        oldAngle = self.angle
        self.angle+=5
        for rectangle in track:
            if pygame.Rect.colliderect(rectangle, self.new_rect):
                self.angle = oldAngle
                return False
        self.angle = oldAngle
        return True

    def getCheckPoint(self, n):
        if(n < len(self.checkPoints)):
            return self.checkPoints[n]
        else:
            return "BAD DATA"

    def rotateRight(self, track):
        oldAngle = self.angle
        self.angle-=5
        if(self.angle < 0):
            self.angle = 359
        #for rectangle in track:
        #    if pygame.Rect.colliderect(rectangle, self.new_rect):
        #        self.angle = oldAngle

    def canRotateRight(self, track):
        oldAngle = self.angle
        self.angle-=5
        for rectangle in track:
            if pygame.Rect.colliderect(rectangle, self.new_rect):
                self.angle = oldAngle
                return False
        self.angle = oldAngle
        return True

    def reverse(self, track):
        if not self.canMove(track) or not self.canRotateRight(track) or not self.canRotateLeft(track):
            self.x -= self.speed * math.sin((self.angle+90)/180*math.pi)
            self.y -= self.speed * math.cos((self.angle+90)/180*math.pi)

    def shiftUp(self):
        self.gear += 1
        if self.gear > 3:
            self.gear = 3

    def shiftDown(self):
        self.gear -= 1
        if self.gear < 1:
            self.gear = 1
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def move(self, track):
        oldx = self.x
        oldy = self.y
        walls = track.getWalls()
        trackCheckPoints = track.getCheckPoints()
        self.x += (self.speed * self.gear) * math.sin((self.angle+90)/180*math.pi)
        self.y += (self.speed * self.gear) * math.cos((self.angle+90)/180*math.pi)

        for rectangle in walls:
            if pygame.Rect.colliderect(rectangle, self.new_rect):
                #hitting top
                if abs(self.new_rect.y - (rectangle.y + rectangle.height)) < 5:
                    self.y = rectangle.y+rectangle.height+10
                #hitting bottom
                elif abs((self.new_rect.y + self.new_rect.height) - rectangle.y) < 5:
                    self.y = rectangle.y-10
                #hitting left
                elif abs(self.new_rect.x - (rectangle.x + rectangle.width)) < 5:
                    self.x = rectangle.x+rectangle.width+10
                #hitting right
                elif abs((self.new_rect.x+self.new_rect.width) - rectangle.x) < 5:
                    self.x = rectangle.x-10

        for i in range(len(trackCheckPoints)):
            if pygame.Rect.colliderect(trackCheckPoints[i],self.new_rect):
                if i == 0 and self.checkPoints[0] == False:
                    self.checkPoints[i] = True
                    self.score += 1
                else:
                    if i == 4 and self.checkPoints[3] == True and self.checkPoints[4] == False:
                        self.checkPoints[4] = True
                        self.numLaps += 1
                        self.score += 2
                        for x in range(len(self.checkPoints)):
                            self.checkPoints[x] = False    
                    elif i == 4 and self.checkPoints[3] == False:
                        for z in range(len(self.checkPoints)):
                            if (self.checkPoints[z] == True):
                                self.score = 0
                            self.checkPoints[z] = False    
                    elif self.checkPoints[i-1] == True and self.checkPoints[i] == False:
                        self.checkPoints[i] = True
                        self.score += 1                           

    def getNumLaps(self):
        return self.numLaps
    
    def getScore(self):
        return self.score

    def canMove(self, track):
        oldx = self.x
        oldy = self.y
        self.x += self.speed * math.sin((self.angle+90)/180*math.pi)
        self.y += self.speed * math.cos((self.angle+90)/180*math.pi)
        for rectangle in track:
            if pygame.Rect.colliderect(rectangle, self.new_rect):
                self.x = oldx
                self.y = oldy
                return False
        self.x = oldx
        self.y = oldy
        return True

    def draw(self, screen):
        rotatedImage = pygame.transform.rotate(self.image,self.angle)
        textsurface = self.myfont.render(str(self.score), False, (0, 0, 0))
        screen.blit(textsurface,(self.x-2,self.y+15))
        self.new_rect = rotatedImage.get_rect(center = self.image.get_rect(center = (self.x, self.y)).center)
        screen.blit(rotatedImage, self.new_rect)

class AICar(Car):
    '''
    0 = do nothing 20%
    1 = rotate left 15%
    2 = rotate right 15%
    '''
    movementDelay = 10
    nextMove = 0
    currentDNA = 0

    def __init__(self, x, y):
        Car.__init__(self, x, y)
        self.dna = []
        self.nextMove = pygame.time.get_ticks() + self.movementDelay
        self.createDNA()

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def resetDNA(self):
        self.currentDNA = 0
    
    def resetAngles(self):
        self.angle = 0
    
    def resetGear(self):
        self.gear = 1
    
    def resetScore(self):
        self.score = 0
    
    def resetCheckPoints(self):
        for i in range(0,len(self.checkPoints)):
            self.checkPoints[i] = False
    
    def resetLaps(self):
        self.numLaps = 0
    
    def getCurrentDNA(self):
        return self.currentDNA
    
    def getDNA(self):
        return self.dna
    
    def appendDNA(self, DNA):
        self.dna.append(DNA)
    
    def mutate(self):
        for i in range(len(self.dna)):
            if (random.randint(1,100) <= 10):
                self.dna[i] = random.randint(0,4)

    def createDNA(self):
        for i in range(2500):
            randNum = random.randint(1,100)
            if(randNum <= 20):
                self.dna.append(0)
            elif(randNum <= 50):
                self.dna.append(1)
            elif(randNum <= 70):
                self.dna.append(2)
            elif(randNum <= 85):
                self.dna.append(3)
            else:
                self.dna.append(4)

    def rotateRight(self, track):
        oldAngle = self.angle
        self.angle-=8
        if(self.angle < 0):
            self.angle = 359
    
    def rotateLeft(self, track):
        oldAngle = self.angle
        self.angle = (self.angle+8) % 360
    
    def move(self, track):
        if self.nextMove < pygame.time.get_ticks():
            if self.currentDNA < len(self.dna):
                if self.dna[self.currentDNA] == 1:
                    super().shiftUp()
                if self.dna[self.currentDNA] == 2:
                    super().shiftDown()
                if self.dna[self.currentDNA] == 3:
                    self.rotateLeft(track)
                if self.dna[self.currentDNA] == 4:
                    self.rotateRight(track)
                self.nextMove = pygame.time.get_ticks() + self.movementDelay
                if self.currentDNA < len(self.dna):
                    self.currentDNA += 1

        super().move(track)

