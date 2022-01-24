from cmath import rect
from numpy import rec
import pygame

class RaceTrack:

    walls = []
    
    def __init__(self, name):
        self.name = name
    
    def addRect(self, rectangle):
        self.walls.append(rectangle)

    def getWalls(self):
        return self.walls

    def drawRaceTrack(self, screen):
        for rectangle in self.walls:
            pygame.draw.rect(screen,(255,0,0),rectangle)

       
    
