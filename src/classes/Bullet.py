from .GameObject import GameObject
import numpy as np
import pygame
from math import atan2
class Bullet (GameObject):

    def __init__(self, direction = [1, 0], start_position = [500, 500], width = 20, height = 20, scalar_velocity = 20):
            GameObject.__init__(self, position = start_position, velocity = np.array(direction), width = width, height = height, scalar_velocity = scalar_velocity)
            self.limitx = pygame.display.Info().current_w
            self.limity = pygame.display.Info().current_h

            self.position = np.array(start_position)

            self.abs_speed = np.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

            self.velocity[0] = self.scalar_velocity * self.velocity[0] / self.abs_speed
            self.velocity[1] = self.scalar_velocity * self.velocity[1] / self.abs_speed

            self.keep_on_screen = True

    def update_position(self):

        self.position = self.position + self.velocity
        self.clamp_ip(pygame.Rect(self.position[0], self.position[1], self.width, self.height))
        
        if self.centerx > self.limitx or self.centerx < 0 or self.centery > self.limity or self.centery < 0:
            self.keep_on_screen = False
    
