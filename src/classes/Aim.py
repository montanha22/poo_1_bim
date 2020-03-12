import pygame

from .GameObject import GameObject

class Aim(GameObject):

    def __init__(self, pos):
        GameObject.__init__(self)
        self.position = pos
        self.color = (255, 255, 0)
        self.radius = 20

    def updateToPosition(self, pos):
        self.position = pos

    #def draw(self, screen, pos):