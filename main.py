import math
import random
import time
import csv

import pygame

from pygame import key
from pygame.display import update
from pygame.time import Clock

from car import Car

pygame.init()
pygame.font.init()
pygame.mixer.init()

FPS = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720))
gameOver = False

p1 = Car(500,500,50,25)

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

def clear_screen(): #clears screen by covering the screen with a large black rectangle
    global screen
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

while gameOver == False: #main while loops, runs 60 times a second (60fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            quit()

    clear_screen()
    p1.draw(screen)
    p1.move()
    p1.friction()
    p1.boundaries()
    getPlayerInput()
    
    pygame.display.flip()
    fpsClock.tick(FPS)