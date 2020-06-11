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
            self.radius = 15
            self.abs_speed = np.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

            self.velocity[0] = self.scalar_velocity * self.velocity[0] / self.abs_speed
            self.velocity[1] = self.scalar_velocity * self.velocity[1] / self.abs_speed

            self.keep_on_screen = True

            self.image = self.image = pygame.image.load('imgs/bullet3.png')

            self.sound_hit = "sounds/Hitl.ogg"

    def update_position(self):
        
        self.position = self.position + self.velocity
        self.clamp_ip(pygame.Rect(self.position[0], self.position[1], self.width, self.height))
        
        if self.centerx > self.limitx or self.centerx < 0 or self.centery > self.limity or self.centery < 0:
            self.keep_on_screen = False
    
    def draw(self, gm, owner):

        pygame.draw.circle(gm.fake_screen, owner.bullet_color, (self.centerx, self.centery), self.radius, self.radius)
        gm.fake_screen.blit(self.image, self.position)
       

    def check_collision(self, is_hero, gm):

        #Bala do herói
        if is_hero:
            if gm.game_screen.boss.check_collision_bullet(self):
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.sound_hit))
                gm.game_screen.hero.bullet_list.remove(self)
                
            elif gm.game_screen.boss.boss_eye.check_collision(self.getRect()) and not gm.game_screen.boss.eye_got_hit:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.sound_hit))
                gm.game_screen.score += 100
                gm.game_screen.hero.bullet_list.remove(self)
                gm.game_screen.boss.eye_got_hit = True
                gm.game_screen.boss.furius = True
                gm.game_screen.boss.bullet_list = []
                gm.game_screen.boss.time_last_paralized = 0
                
            elif gm.game_screen.boss.weak_spots.check_collision(self.getRect()):
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.sound_hit))
                gm.game_screen.hero.bullet_list.remove(self)
                gm.game_screen.boss.weak_spots.got_hit = True
                gm.actual_screen = gm.win_screen
                gm.game_screen._running = False
        
        #Bala do boss
        else: 
            if gm.game_screen.hero.check_collision(self.getRect()) and not gm.game_screen.hero.is_rewinding:
                if self in gm.game_screen.boss.bullet_list:
                    gm.game_screen.boss.bullet_list.remove(self)
                #Player dies
                gm.actual_screen = gm.game_over_screen
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.sound_hit))
                gm.game_screen._running = False
    
    def check_collision_bullet(self, op_bullet, gm):
        if(self.colliderect(op_bullet)):
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.sound_hit))
            gm.game_screen.hero.bullet_list.remove(self)
            gm.game_screen.boss.bullet_list.remove(op_bullet)