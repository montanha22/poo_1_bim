import pygame

class GameObject(pygame.Rect):
    def __init__ (self, position = (720, 480), width = 100, height = 100, velocity = [0, 0]):
        
        pygame.Rect.__init__(self)
        self.velocity = velocity
        self.moving = False
        self.moveCount = 0
        self.attacking = False
        self.attackCount = 0








