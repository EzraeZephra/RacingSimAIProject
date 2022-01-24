import pygame

class RaceTrack:

    walls = []
    
    def __init__(self, name):
        self.name = name
    
    def addWall(self, points):
        self.walls.append(points)

    def drawRaceTrack(self, screen):
        for point in self.walls:
            pygame.draw.line(screen, (255,0,0), (point[0],point[1]), (point[2],point[3]))
    
