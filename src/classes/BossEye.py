from .GameObject import GameObject
import pygame
import os
import numpy as np
from .Bullet import Bullet
from math import atan2
from math import sqrt
from .WeakPoint import WeakPoint


class BossEye (GameObject):
    def __init__(self, boss_position = [0, 0], boss_radius = 10, boss_direction = [1, 0], radius = 10, color = (255, 0, 0)):
        GameObject.__init__(self, position = boss_position, velocity = np.array([1, 0]), width = 2*radius, height = 2*radius, scalar_velocity = 0)
        
        self.limitx = pygame.display.Info().current_w
        self.limity = pygame.display.Info().current_h
        self.radius = radius
        self.boss_radius = boss_radius
        self.color = color
        self.image =  pygame.image.load('imgs/eye.png')


    def update_position(self, boss_position, boss_direction, eye_got_hit):

        if not eye_got_hit:
            if(boss_direction[0] ** 2 + boss_direction[1] ** 2):
                self.position[0] = boss_position[0] + self.boss_radius * boss_direction[0] / np.sqrt(boss_direction[0] ** 2 + boss_direction[1] ** 2)
                self.position[1] = boss_position[1] + self.boss_radius * boss_direction[1] / np.sqrt(boss_direction[0] ** 2 + boss_direction[1] ** 2)
            self.clamp_ip(pygame.Rect(self.position[0]-self.radius, self.position[1]-self.radius, self.width, self.height))
            self.color = (255, 0, 0)
        else:
            self.color = (0, 0, 0)

    def check_collision(self, rect):
        if self.colliderect(rect):
            return True
        return False