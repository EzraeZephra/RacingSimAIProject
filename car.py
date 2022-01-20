from numpy import MAY_SHARE_BOUNDS
import pygame

class Car:

    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.angle = 0
        loadImage = pygame.image.load("top-car-view-png-34878.png")
        self.image = pygame.transform.scale(loadImage,(200,80))
        self.myRect = pygame.Rect(self.x, self.y, self.width, self.length)
    
    def moveUp(self):
        self.y += self.speed
    
    def moveDown(self):
        self.y -= self.speed
    
    def moveRight(self):
        self.x += self.speed
    
    def moveLeft(self):
        self.x -= self.speed

    def draw(self, screen):
        rotatedImage = pygame.transform.rotate(self.image, self.angle)
        screen.blit(rotatedImage, (self.x, self.y))
        self.angle += 1
