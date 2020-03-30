from .GameObject import GameObject
import pygame
import numpy as np
from .Bullet import Bullet
from math import atan2
class Boss_1 (GameObject):
    def __init__(self):
        GameObject.__init__(self, position = [float(pygame.display.Info().current_w/2), float(pygame.display.Info().current_h/2)], width = 200, height = 200)
        
        self.scalar_velocity = 3

        self.bullet_list = []
        self.n_bullets_to_shoot = np.random.randint(3,40)
        self.bullet_initial_dist = 100
        self.time_last_attack = 301
        self.attack_interval = np.random.randint(10,30)
        self.can_attack = True


        self.fixed_in_the_middle = False

        self.bullet_color = (255, 0, 0)
        self.direction = np.array([0.0, 0.0])

    def updatePosition(self, player_position):
        self.direction = np.array((player_position[0] , player_position[1])) -  np.array((self.centerx, self.centery))

        #print(direction)
        self.velocity = self.direction.copy()

        if self.fixed_in_the_middle:
            self.velocity = np.array([0, 0])

        print(self.velocity)

        self.fix_velocity_scale()
        self.position = self.position + self.velocity

        print(self.velocity)
        print(self.position)
        self.clamp_ip(pygame.Rect(self.position[0], self.position[1], self.width, self.height))

    def attack(self):
        self.attack_interval = np.random.randint(30,50)
        self.time_last_attack = 0
        self.can_attack = False

        self.n_bullets_to_shoot = np.random.randint(3,20)
        #angles = 2 * np.pi  * np.array(range(1, self.n_bullets_to_shoot + 1)) / self.n_bullets_to_shoot
        angles = atan2(self.direction[1], self.direction[0]) + np.array(np.linspace(-10,11,10)) * np.pi/10
        #print(angles)
        for angle in angles:
            coso = np.cos(angle)
            sino = np.sin(angle)

            self.bullet_list.append(
                Bullet(
                    direction = [coso, sino],
                    start_position = [self.centerx + self.bullet_initial_dist * coso, self.centery + self.bullet_initial_dist * sino],
                    scalar_velocity = 3
                )
            )
