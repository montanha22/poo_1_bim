from .GameObject import GameObject
import pygame
import numpy as np
from math import atan2

class WeakPoint (GameObject):
    def __init__(self, boss_position = [0, 0], boss_radius = 10, boss_direction = [1, 0], radius = 10, color = (255, 255, 255)):
        GameObject.__init__(self, position = boss_position, velocity = np.array([1, 0]), width = 2*radius, height = 2*radius, scalar_velocity = 0)
        
        self.limitx = pygame.display.Info().current_w
        self.limity = pygame.display.Info().current_h
        self.radius = radius
        self.boss_radius = boss_radius
    
        self.color = color
        self.got_hit = False

    def update_position(self, boss_position, boss_direction, eye_got_hit):

        if not eye_got_hit:
            self.position[0] = boss_position[0] - self.boss_radius * boss_direction[0] / np.sqrt(boss_direction[0] ** 2 + boss_direction[1] ** 2) 
            self.position[1] = boss_position[1] - self.boss_radius * boss_direction[1] / np.sqrt(boss_direction[0] ** 2 + boss_direction[1] ** 2)
            self.clamp_ip(pygame.Rect(self.position[0]-self.radius, self.position[1]-self.radius, self.width, self.height))
        
        if self.got_hit:
            self.color = (0, 0, 0)
            





        

