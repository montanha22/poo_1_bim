import pygame

class GameObject:
    def __init__ (self, x=0,y=0, speed = 0):
        self.speed = speed
        self.x = x
        self.y = y
        #Create object rectangle
        self.rect = pygame.Rect(10,10,10,10)