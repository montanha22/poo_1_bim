import pygame

class GameObject:
    def __init__ (self, position, width, height, speed = 0):
        self.width = 15
        self.height = 21
        self.velocity = None
        self.moving = False
        self.moveCount = 0
        self.attacking = False
        self.attackCount = 0
        self.hitbox = (self.x + 6, self.y + 3, width, height)



