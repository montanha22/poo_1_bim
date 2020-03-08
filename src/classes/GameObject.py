import pygame

class GameObject:
    def __init__ (self, position=(720, 480), width=0, height=0, velocity=0):
        self.velocity = velocity

        self.moving = False
        self.moveCount = 0
        self.attacking = False
        self.attackCount = 0


        self.rect = pygame.Rect(position[0], position[1], width, height)





