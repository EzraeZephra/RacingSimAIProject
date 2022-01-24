import math
import random
import time
import csv
from numpy import rec

import pygame

from pygame import key
from pygame.display import update
from pygame.time import Clock

from car import Car
from race_track import RaceTrack

pygame.init()
pygame.font.init()
pygame.mixer.init()

FPS = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720))
gameOver = False

p1 = Car(500,500,50,35)
track1 = RaceTrack("track 1")

def getPlayerInput(): #Takes in user keyboard input (A/D - Left/Right), (SPACE - Double Jump), (LMB - Shoot)
    global p1 
    keyPressed = pygame.key.get_pressed()

    if keyPressed[pygame.K_a]:
        p1.rotateLeft()
    if keyPressed[pygame.K_d]:
        p1.rotateRight()
    if keyPressed[pygame.K_w]:
        p1.accel()
    if keyPressed[pygame.K_s]:
        p1.decel()

def checkCollision():
    walls = track1.getWalls()
    for rectangle in walls:
        if p1.getCollisionRectangle().colliderect(pygame.Rect(rectangle)):
            p1.setSpeed(-1 * p1.getSpeed())

def clear_screen(): #clears screen by covering the screen with a large black rectangle
    global screen
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

track1.addRect(pygame.Rect(100,100,400,300))

while gameOver == False: #main while loops, runs 60 times a second (60fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            quit()

    clear_screen()
    p1.draw(screen)
    track1.drawRaceTrack(screen)
    p1.move()
    p1.friction()
    p1.boundaries()
    getPlayerInput()
    checkCollision()
    
    pygame.display.flip()
    fpsClock.tick(FPS)