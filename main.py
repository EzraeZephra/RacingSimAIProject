import math
import random
import time
import csv

import pygame

from pygame import key
from pygame.display import update
from pygame.time import Clock

pygame.init()
pygame.font.init()
pygame.mixer.init()

FPS = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((540,875))
gameOver = False

def clear_screen(): #clears screen by covering the screen with a large black rectangle
    global screen
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 540, 900))

while gameOver == False: #main while loops, runs 60 times a second (60fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            quit()
    
    pygame.display.flip()
    fpsClock.tick(FPS)