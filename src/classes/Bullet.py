from .GameObject import GameObject
import numpy as np
import pygame
class Bullet (GameObject):

    def __init__(self, direction = [1, 0], start_position = [500, 500]):
            GameObject.__init__(self, position = start_position, velocity = np.array(direction), width = 20, height = 20)
            self.limitx = pygame.display.Info().current_w
            self.limity = pygame.display.Info().current_h
            self.normalize_velocity()
            self.velocity = 30 * self.velocity
            self.keep_on_screen = True
    #1080, 720
    #screen_info = pygame.display.Info()
    #print(screen_info.current_w, screen_info.current_h)
    def update_position(self):
        self.move_ip(self.velocity[0], self.velocity[1])
        if self.centerx > self.limitx or self.centerx < 0 or self.centery > self.limity or self.centery < 0:
            self.keep_on_screen = False
    
    def normalize_velocity(self):
        self.velocity = self.velocity / np.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)