from .GameObject import GameObject
import pygame
import os
import numpy as np
from .Bullet import Bullet
from .BossEye import BossEye
from math import atan2
from math import sqrt
from .WeakPoint import WeakPoint


class Boss_1 (GameObject):
    def __init__(self,resolution):
        GameObject.__init__(self, position = [4*float(resolution[0]/5), float(resolution[1]/2)], width = 282, height = 282)
        self.scalar_velocity = 3
        self.bullet_list = []
        self.n_bullets_to_shoot = np.random.randint(3,40)
        self.bullet_initial_dist = 100
        self.time_last_attack = 301
        self.attack_interval = np.random.randint(6,30)
        self.can_attack = True
        self.furius = False
        self.fixed_in_the_middle = False
        self.bullet_color = (255, 0, 0)
        self.direction = np.array([0.0, 0.0])
        self.weak_got_hit = False
        self.time_paralized = 300
        self.time_last_paralized = 310
        self.eye_got_hit = False
        self.radius = 141
        self.boss_eye = BossEye(self.position, self.radius, self.direction, 25)
        self.weak_spots = WeakPoint(self.position, self.radius, self.direction, 25)
        self.image = pygame.image.load('imgs/boss_1.png')
    
    def new_boss(self, resolution):

        self.position = [4*float(resolution[0]/5), float(resolution[1]/2)]
        self.width = 282
        self.height = 282
        self.velocity = [0.0, 0.0]
        self.scalar_velocity = 3
        self.position = np.array(self.position)
        self.left = self.position[0]
        self.top = self.position[1] 
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.moving = False
        self.moveCount = 0
        self.attacking = False
        self.attackCount = 0       
        self.bullet_list.clear()
        self.n_bullets_to_shoot = np.random.randint(3,40)
        self.bullet_initial_dist = 100
        self.time_last_attack = 301
        self.attack_interval = np.random.randint(10,30)
        self.can_attack = True
        self.furius = False
        self.fixed_in_the_middle = False
        self.direction = np.array([0.0, 0.0])
        self.weak_got_hit = False
        self.time_paralized = 300
        self.time_last_paralized = 310
        self.eye_got_hit = False
        self.radius = 141
        self.boss_eye = BossEye(self.position, self.radius, self.direction, 25)
        self.weak_spots = WeakPoint(self.position, self.radius, self.direction, 25)
        

    def updatePosition(self, player_position):

        if not self.eye_got_hit:
            self.direction = np.array((player_position[0] , player_position[1])) -  np.array((self.centerx, self.centery))

            self.velocity = self.direction.copy()

            if self.fixed_in_the_middle:
                self.velocity = np.array([0, 0])

            self.fix_velocity_scale()
            self.position = self.position + self.velocity

            self.clamp_ip(pygame.Rect(self.position[0], self.position[1], self.width, self.height))

            self.weak_spots.update_position( np.array((self.centerx, self.centery)), self.direction, self.eye_got_hit)
            self.boss_eye.update_position( np.array((self.centerx, self.centery)), self.direction, self.eye_got_hit)
    

    def attack(self):
        if not self.eye_got_hit and not self.weak_spots.got_hit:
            self.attack_interval = np.random.randint(10,15)
            self.time_last_attack = 0
            self.can_attack = False
            self.n_bullets_to_shoot = np.random.randint(3,20)
       
            angles = atan2(self.direction[1], self.direction[0]) + np.array(np.linspace(-10,11,10)) * np.pi/10
          
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
    

    def check_collision_hero(self, gm):   
        if(sqrt((gm.game_screen.hero.left+24 - self.centerx)**2 + (gm.game_screen.hero.top+24 - self.centery)**2) < self.radius+24*sqrt(2)):
            if(not gm.game_screen.hero.is_rewinding):    
                gm.actual_screen = gm.game_over_screen
                gm.game_screen._running = False
        

    def check_collision_bullet(self, bullet):
        if sqrt((self.centerx - bullet.left)**2 +(self.centery-bullet.top)**2) < 141+1*sqrt(25):
            return True
        return False
    

    def draw(self, gm):

        pygame.draw.circle(gm.fake_screen, (0,0,0), (self.centerx, self.centery), self.radius, self.radius)
        gm.fake_screen.blit(self.image, self.position)
        
        #Boss Eye
        if(not self.eye_got_hit):
            pygame.draw.circle(gm.fake_screen, self.boss_eye.color, (int(self.boss_eye.position[0]), int(self.boss_eye.position[1])), self.boss_eye.radius, self.boss_eye.radius)
            gm.fake_screen.blit(self.boss_eye.image,  (int(self.boss_eye.position[0])-self.boss_eye.radius, int(self.boss_eye.position[1])- self.boss_eye.radius))
                    
        #Boss Weak Points
        pygame.draw.circle(gm.fake_screen, self.weak_spots.color, (int(self.weak_spots.position[0]), int(self.weak_spots.position[1])), self.weak_spots.radius, self.boss_eye.radius)
        gm.fake_screen.blit(self.weak_spots.image,  (int(self.weak_spots.position[0])-self.weak_spots.radius, int(self.weak_spots.position[1])- self.weak_spots.radius))

  
    def do_attack(self, game_screen):
        self.time_last_attack = self.time_last_attack + 1
        self.time_last_paralized = self.time_last_paralized + 1
        self.updatePosition((game_screen.hero.centerx, game_screen.hero.centery))

        if self.can_attack:
            self.attack()

        if self.time_paralized < self.time_last_paralized:
                self.eye_got_hit = False

        if self.time_last_attack > self.attack_interval:
            self.can_attack = True
    
