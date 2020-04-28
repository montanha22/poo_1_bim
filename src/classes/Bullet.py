from .GameObject import GameObject
import numpy as np
import pygame
from math import atan2
class Bullet (GameObject):

    def __init__(self, direction = [1, 0], start_position = [500, 500], width = 20, height = 20, scalar_velocity = 20):
            GameObject.__init__(self, position = start_position, velocity = np.array(direction), width = width, height = height, scalar_velocity = scalar_velocity)
            self.limitx = 1920
            self.limity = 1080

            self.position = np.array(start_position)
            self.radius = 10
            self.abs_speed = np.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

            self.velocity[0] = self.scalar_velocity * self.velocity[0] / self.abs_speed
            self.velocity[1] = self.scalar_velocity * self.velocity[1] / self.abs_speed

            self.keep_on_screen = True

    def update_position(self):
        
        self.position = self.position + self.velocity
        self.clamp_ip(pygame.Rect(self.position[0], self.position[1], self.width, self.height))
        
        if self.centerx > self.limitx or self.centerx < 0 or self.centery > self.limity or self.centery < 0:
            self.keep_on_screen = False
    
    def draw(self, gm, owner):
        pygame.draw.circle(gm.fake_screen, owner.bullet_color, (self.centerx, self.centery), self.radius, self.radius)
        #pygame.draw.rect(game_screen.screen, (0,0,0) , self.getRect())

    def check_collision(self, is_hero, game_screen, gm):
        if is_hero:
            if game_screen.boss.check_collision(self.getRect()):
                game_screen.hero.bullet_list.remove(self)
            elif game_screen.boss.boss_eye.check_collision(self.getRect()) and not gm.game_screen.boss.eye_got_hit:
                game_screen.hero.bullet_list.remove(self)
                game_screen.boss.eye_got_hit = True
                game_screen.boss.time_last_paralized = 0
            elif game_screen.boss.weak_spots.check_collision(self.getRect()):
                game_screen.hero.bullet_list.remove(self)
                fame_screen.boss.weak_spots.got_hit = True

        else: 
            if game_screen.hero.check_collision(self.getRect()) and not gm.game_screen.hero.is_rewinding:
                game_screen.boss.bullet_list.remove(self)
                #Player dies
                gm.actual_screen = gm.game_over_screen
                game_screen._running = False
        
        
            
        
        
