from .GameObject import GameObject
import pygame
import numpy as np
from .Bullet import Bullet
from math import atan2
from .WeakPoint import WeakPoint
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
        self.weak_got_hit = False
        self.time_paralized = 750
        self.time_last_paralized = 760
        self.eye_got_hit = False
        self.radius = 141
        self.boss_eye = BossEye(self.position, self.radius, self.direction, 20)
        self.weak_spots = WeakPoint(self.position, self.radius, self.direction, 20)
        

    def updatePosition(self, player_position):

        if not self.eye_got_hit:
            self.direction = np.array((player_position[0] , player_position[1])) -  np.array((self.centerx, self.centery))

            #print(direction)
            self.velocity = self.direction.copy()

            if self.fixed_in_the_middle:
                self.velocity = np.array([0, 0])

            #print(self.velocity)

            self.fix_velocity_scale()
            self.position = self.position + self.velocity

            #print(self.velocity)
            #print(self.position)
            self.clamp_ip(pygame.Rect(self.position[0], self.position[1], self.width, self.height))

            self.weak_spots.update_position( np.array((self.centerx, self.centery)), self.direction, self.eye_got_hit)
            self.boss_eye.update_position( np.array((self.centerx, self.centery)), self.direction, self.eye_got_hit)
    



    def attack(self):
        if not self.eye_got_hit and not self.weak_spots.got_hit:
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
    
    def rotate_center(self, angle):
        """rotate an image while keeping its center"""
        pass

    def check_collision(self, rect):
        if self.colliderect(rect):
            return True
        return False
    
    
    
class BossEye (GameObject):
    def __init__(self, boss_position = [0, 0], boss_radius = 10, boss_direction = [1, 0], radius = 10, color = (255, 0, 0)):
        GameObject.__init__(self, position = boss_position, velocity = np.array([1, 0]), width = 2*radius, height = 2*radius, scalar_velocity = 0)
        
        self.limitx = pygame.display.Info().current_w
        self.limity = pygame.display.Info().current_h
        self.radius = radius
        self.boss_radius = boss_radius
        self.color = color

    def update_position(self, boss_position, boss_direction, eye_got_hit):

        if not eye_got_hit:
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