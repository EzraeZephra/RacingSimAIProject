import pygame

class RaceTrack:

    walls = []
    check_points = []

    def __init__(self, name):
        self.name = name

    def addCheckPoint(self, rectangle):
        self.check_points.append(rectangle)

    def addRect(self, rectangle):
        self.walls.append(rectangle)

    def drawRaceTrack(self, screen):
        for rectangle in self.walls:
            pygame.draw.rect(screen, (128, 128, 128), rectangle)
        for rectangle in self.check_points:
            pygame.draw.rect(screen, (0, 155, 30), rectangle)

    def getWalls(self):
        return self.walls

    def getCheckPoints(self):
        return self.check_points