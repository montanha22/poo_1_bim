import pygame
from pygame.locals import *
import sys
from random import sample
import glob
from classes.EventManager import EventManager
from classes.Hero import Hero
from classes.Aim import Aim
from classes.Bullet import Bullet
from classes.Boss_1 import Boss_1
import classes.Menu
import numpy as np
from numpy import linalg as LA
import time
import pygameMenu
import ast

class GameManager():
    def __init__(self):

        #Pygame initialization
        pygame.init()
        icon=pygame.image.load("sprites/icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Boss Slayer")

        #Some needed stuff
        self._running = True

        #Read config file

        f = open('src/config.txt', 'r')

        config = f.read()
        config = ast.literal_eval(config)

        f.close()

        #Window resolution
        self.window_resolution=config["resolution"]
        self.original_resolution=(1920,1080)
        self.monitor_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h) #Needs to be before screen and fake_screen declaration
        self.fullscreen = config["fullscreen"]

        #Text font
        self.font = pygame.font.Font("sprites/menu/kenvector_future.ttf", 20)
        
        self.screen = pygame.display.set_mode(self.original_resolution, pygame.NOFRAME)
        self.fake_screen=self.screen.copy()
        if self.fullscreen:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))
        else:
            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = self.window_resolution, w = self.window_resolution[0],h=self.window_resolution[1]))

        self.stage = 1
        self.count = 0
        self.clock = pygame.time.Clock()

        #Instantiating hero and aim
        self.hero = Hero(self.original_resolution)
        self.mousepos=pygame.mouse.get_pos()
        self.aim = Aim(self.mousepos)

        #Boss
        self.boss = Boss_1(self.original_resolution)

    def onInit(self):

        self._running = True

    def onEvent(self):

        #Getting pressed buttons from keyboard and mouse
        pressed = pygame.key.get_pressed()
        mpressed = pygame.mouse.get_pressed()

        #Checking if the window was closed or ESC was pressed (quit game) or F10 was pressed (toggle fullscreen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.onCleanup()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                classes.Menu.pause_menu(self)
                return
            
        #Creating booleans for hero actions keys
        up = (pressed[pygame.K_w] or pressed[pygame.K_UP])
        down = (pressed[pygame.K_s] or pressed[pygame.K_DOWN])
        left = (pressed[pygame.K_a] or pressed[pygame.K_LEFT])
        right = (pressed[pygame.K_d] or pressed[pygame.K_RIGHT])
        rewind = (pressed[pygame.K_r])
        mouse_right_click = (mpressed[0])

        #Start rewind if R is pressed and hero can rewind
        if rewind and self.hero.can_rewind:
            self.hero.is_rewinding = True
            self.hero.rewind(self.hero.timetrack[-1])
            self.hero.can_rewind = False
        
        #Stop the hero when nothing is pressed
        self.hero.stop()

        #Move if not rewinding
        if not self.hero.is_rewinding:
            self.hero.stop()
            if up:
                self.hero.moveUp()
            if down:
                self.hero.moveDown()
            
            if up and down:
                self.hero.stopUpDown()

            if left:
                self.hero.moveLeft()
            
            if right:
                self.hero.moveRight()

            if left and right:
                self.hero.stopLeftRigth()

            #Shoot if m1 is pressed (in mouse direction)
            if mouse_right_click and self.hero.can_shoot:
                self.hero.shoot()
                direction = np.array(self.aim.position) - np.array((self.hero.centerx , self.hero.centery))
                self.hero.bullet_list.append(Bullet(direction = direction, start_position = (self.hero.centerx, self.hero.centery)))
                


    
    def onLoop(self):

        #Update hero, aim and bullets positions
        self.hero.updatePosition()
        self.aim.updateToPosition(self.mousepos)
        for bullet_list in [self.hero.bullet_list, self.boss.bullet_list]:
            for bullet in bullet_list:

                bullet.update_position()

                if bullet.keep_on_screen == False:
                    bullet_list.remove(bullet)
        
        for boss_bullet in self.boss.bullet_list:
            if self.hero.check_collision(boss_bullet.getRect()) and not self.hero.is_rewinding:
                self.boss.bullet_list.remove(boss_bullet)
                #Player dies
                classes.Menu.game_over(self)
                return
        
        for hero_bullet in self.hero.bullet_list:
            if self.boss.check_collision(hero_bullet.getRect()):
                self.hero.bullet_list.remove(hero_bullet)
            elif self.boss.boss_eye.check_collision(hero_bullet.getRect()) and not self.boss.eye_got_hit:
                self.hero.bullet_list.remove(hero_bullet)
                self.boss.eye_got_hit = True
                self.boss.time_last_paralized = 0

            elif self.boss.weak_spots.check_collision(hero_bullet.getRect()):
                self.hero.bullet_list.remove(hero_bullet)
                self.boss.weak_spots.got_hit = True


            
        # for bullet in self.boss.bullet_list:
        #     bullet.update_position()
        #     if bullet.keep_on_screen == False:
        #         self.boss.bullet_list.remove(bullet)

        self.hero.time_last_shoot = self.hero.time_last_shoot + 1
        self.boss.time_last_attack = self.boss.time_last_attack + 1
        self.boss.time_last_paralized = self.boss.time_last_paralized + 1
        self.boss.updatePosition((self.hero.centerx, self.hero.centery))

        if self.boss.can_attack:
            self.boss.attack()

        if self.boss.time_paralized < self.boss.time_last_paralized:
                self.boss.eye_got_hit = False

        if self.boss.time_last_attack > self.boss.attack_interval:
            self.boss.can_attack = True

        if self.hero.time_last_shoot > self.hero.shoot_interval:
            self.hero.can_shoot = True
        #Auxiliary counter
        self.count = (self.count + 1) % 30

            
    def onRender(self):
        #Render Background
        self.fake_screen.fill((50,50,50))

        
        #Create and update timetrack
        if not self.hero.is_rewinding:
            if self.count%5 == 0:
                self.hero.timetrack.append((self.hero.sprite.copy(), self.hero.get_correct_position_to_blit(), self.hero.getRect()))
            if self.count%29 == 0 and len(self.hero.timetrack) == self.hero.timetracklen:
                self.hero.can_rewind = True
            if len(self.hero.timetrack) > self.hero.timetracklen :
                self.hero.timetrack.pop(0)
            
        #Render hero rewinding
        else:
            if len(self.hero.timetrack) > 0:
                self.hero.rewind(self.hero.timetrack[-1])
                self.hero.timetrack.pop(-1)
            else:
                self.hero.is_rewinding = False
                self.hero.rewind(None)

        #Render timetrack
        for trail in self.hero.timetrack:
            if trail[0] != None:
                temp = trail[0].copy()
                temp.fill((0,0,255, 100), special_flags = pygame.BLEND_RGBA_MULT)
                #print(temp.get_alpha())
                self.fake_screen.blit(temp, trail[1]) 
    
        #Make last timetrack position more darker
        if len(self.hero.timetrack) != 0:
            self.hero.timetrack[0][0].fill((0,0,255,255), special_flags = pygame.BLEND_RGBA_MULT)
            self.fake_screen.blit(self.hero.timetrack[0][0], self.hero.timetrack[0][1])

        #Render hero
        self.fake_screen.blit(self.hero.sprite, self.hero.get_correct_position_to_blit())
        #pygame.draw.rect(self.screen, (155,155,155) , self.hero.getRect())

        #Boss
        if not self.boss.weak_spots.got_hit:
            if not self.boss.weak_got_hit:
                pygame.draw.circle(self.fake_screen, (0,0,0), (self.boss.centerx, self.boss.centery), self.boss.radius, self.boss.radius)
                #pygame.draw.rect(self.screen, (155,155,155), self.boss.getRect())
                
                #Boss Eye
                pygame.draw.circle(self.fake_screen, self.boss.boss_eye.color, (int(self.boss.boss_eye.position[0]), int(self.boss.boss_eye.position[1])), self.boss.boss_eye.radius, self.boss.boss_eye.radius)
                #pygame.draw.rect(self.screen, (155,155,155), self.boss.boss_eye.getRect())
                
                #Boss Weak Points
                pygame.draw.circle(self.fake_screen, self.boss.weak_spots.color, (int(self.boss.weak_spots.position[0]), int(self.boss.weak_spots.position[1])), self.boss.weak_spots.radius, self.boss.boss_eye.radius)
        
        #Render aim
        pygame.draw.circle(self.fake_screen, self.aim.color, self.aim.position, self.aim.radius, self.aim.thick)

        #Render bullets
        for bullet_list, owner in zip([self.hero.bullet_list, self.boss.bullet_list], [self.hero, self.boss]):
            for bullet in bullet_list:
                pygame.draw.circle(self.fake_screen, owner.bullet_color, (bullet.centerx, bullet.centery), bullet.radius, bullet.radius)
                #pygame.draw.rect(self.screen, (0,0,0) , bullet.getRect())

        #Display refresh
        self.screen.blit(pygame.transform.scale(self.fake_screen, self.window_resolution), (0, 0))
        pygame.display.flip()

        #Fix mouse position because of resizing
        self.mousepos = list(pygame.mouse.get_pos())
        self.mousepos = [int(self.mousepos[0]*self.original_resolution[0]/self.window_resolution[0]),int(self.mousepos[1]*self.original_resolution[1]/self.window_resolution[1])]
        self.mousepos=tuple(self.mousepos)

    def onCleanup(self):
        #Write settings on configuration file
        config = {"fullscreen":self.fullscreen,"resolution":self.window_resolution}
        f = open('src/config.txt', 'w')
        f.write(str(config))
        f.close()

        #Quit game
        pygame.quit()
        sys.exit()

    def onExecute(self):

        #Start
        if self.onInit() == False:
            self._running = False
        
        #Infinite loopgm.restartGame()
        while(self._running):
            #Fps limit
            self.clock.tick(60)

            if(self._running):
                #Get keys pressed and mouse infos
                self.onEvent()

            if(self._running):
                #Act and update 
                self.onLoop()

            #This if is needed when the player dies, so it doesnt render the game when going though menus
            if(self._running):
                #Render
                self.onRender()
        
        #Finish all
        #self.onCleanup()

    def onMainMenu(self):

        #Adjust initial screen resolution
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                    self.fullscreen = False
                    self.window_resolution=event.size
                    self.screen = pygame.display.set_mode(event.size)
                    self.screen.blit(pygame.transform.scale(self.fake_screen, self.window_resolution), (0, 0))
                    pygame.display.flip()
                
            if event.type == pygame.USEREVENT + 1:
                self.fullscreen = True
                self.window_resolution = self.monitor_resolution
                self.screen = pygame.display.set_mode(self.window_resolution, pygame.FULLSCREEN)
                self.screen.blit(pygame.transform.scale(self.fake_screen, self.window_resolution), (0, 0))
                pygame.display.flip()

        classes.Menu.main_menu(self)

    def endGame(self):
        #Delete last session
        del self.hero
        del self.aim
        del self.boss

        self._running = False

    def restartGame(self):

        #Some needed stuff
        self._running = True
        
        self.stage = 1
        self.count = 0

        #Instantiating hero and aim
        self.hero = Hero(self.original_resolution)
        self.mousepos=pygame.mouse.get_pos()
        self.aim = Aim(self.mousepos)

        #Boss
        self.boss = Boss_1(self.original_resolution)
