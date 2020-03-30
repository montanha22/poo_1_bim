import pygame
import numpy as np
class GameObject(pygame.Rect):
    def __init__ (self, position = [0, 0], width = 100, height = 100, velocity = [0.0, 0.0], scalar_velocity = 30):
        
        self.position = np.array(position)
        left = self.position[0]
        top = self.position[1] 
        
        pygame.Rect.__init__(self, left, top, width, height)
        
        self.velocity = velocity
        
        self.moving = False
        self.moveCount = 0
        self.attacking = False
        self.attackCount = 0
        self.scalar_velocity = scalar_velocity

    def getRect(self):
        return self.copy()

    def velocity_norm(self):
        return np.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

    def fix_velocity_scale(self):
        if not ( self.velocity[0] == 0 and self.velocity[1] == 0 ):

            self.abs_speed = np.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

            print(self.velocity/self.abs_speed)
            print(float(1.0 * self.scalar_velocity * self.velocity[0] / self.abs_speed))
            self.velocity[0] = float(1.0 * self.scalar_velocity * self.velocity[0] / self.abs_speed)
            self.velocity[1] = float(1.0 * self.scalar_velocity * self.velocity[1] / self.abs_speed)





