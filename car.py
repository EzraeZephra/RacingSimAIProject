import pygame

class Car:
    x = 100;
    y = 100;
    width = 30;
    length = 70;
    speed = 10;
    color = (255,0,0)

    def __init__(self, color):
        self.color = color;
    
    def moveUp(self):
        self.y += self.speed
    
    def moveDown(self):
        self.y -= self.speed
    
    def moveRight(self):
        self.x += self.speed
    
    def moveLeft(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen,(255,255,255),(self.x,self.y,self.length,self.height))
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.length,self.height))

    def getCollisionRectangle(self):
        return pygame.Rect(self.x, self.y, self.length, self.height)

