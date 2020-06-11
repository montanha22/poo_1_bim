import pygame

from .GameObject import GameObject

class Aim(GameObject):

    def __init__(self, pos):
        GameObject.__init__(self)
        self.position = pos
        self.color = (255, 255, 0)
        self.radius = 5
        self.thick = 1


    def new_aim(self,gm):
        self.position = gm.mousepos

    def updateToPosition(self, pos):
        self.position = pos

    def draw(self, gm):
        pygame.draw.circle(gm.fake_screen, self.color, self.position, self.radius, self.thick)

          



