import pygame
import math

class Car:

    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.angle = 0
        self.speed = 5
        loadImage = pygame.image.load("top-car-view-png-34878.png")
        self.image = pygame.transform.scale(loadImage,(self.width,self.length))
        self.myRect = pygame.Rect(self.x, self.y, self.width, self.length)
    
    def rotateLeft(self):
        self.angle += 15
    
    def rotateRight(self):
        self.angle -= 15
    
    def decel(self):
        if (self.speed > 0):
            self.speed -= 0.1
    
    def accel(self):
        self.speed += 0.2

    def move(self):
        self.x += self.speed * math.sin((self.angle+270)/180*math.pi)
        self.y += self.speed * math.cos((self.angle+270)/180*math.pi)
    
    def calculate_new_xy(self):
        move_vec = pygame.math.Vector2()
        move_vec.from_polar((self.speed, self.angle))
        self.x += move_vec
        self.y += move_vec
    

    def draw(self, screen):
        rotatedImage = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotatedImage.get_rect(center = self.image.get_rect(center = (self.x, self.y)).center)
        screen.blit(rotatedImage, new_rect)
