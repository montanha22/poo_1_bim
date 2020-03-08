import pygame
import glob
#import definitions
from classes.GameObject import GameObject


class Projectile():

    def __init__(self, position, color ,radius, direction):
        self.position = position
        self.radius = radius
        self.direction = direction
        self.vel = 8 * direction
        self.color = color

    def draw(screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)


        