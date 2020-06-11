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
from classes.Screen import *
import numpy as np
from numpy import linalg as LA
import time
import ast

class GameScreen(Screen):
    def __init__(self, gm):
        super().__init__()

        #Some needed stuff
        self._running = True

        self.stage = 1
        self.count = 0
    
        #Instantiating hero and aim an boss
        self.hero = Hero(gm.original_resolution)
        self.aim = Aim(gm.mousepos)
        self.boss = Boss_1(gm.original_resolution)

    def onInit(self):

        self._running = True

    def onEvent(self,gm):

        #Getting pressed buttons from keyboard and mouse
        pressed = pygame.key.get_pressed()
        mpressed = pygame.mouse.get_pressed()

        #Checking if the window was closed or ESC was pressed (quit game) or F10 was pressed (toggle fullscreen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.onCleanup(gm)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                gm.actual_screen = gm.pause_screen
                self._running = False
            
        #Creating booleans for hero actions keys
        up = (pressed[pygame.K_w] or pressed[pygame.K_UP])
        down = (pressed[pygame.K_s] or pressed[pygame.K_DOWN])
        left = (pressed[pygame.K_a] or pressed[pygame.K_LEFT])
        right = (pressed[pygame.K_d] or pressed[pygame.K_RIGHT])
        rewind = (pressed[pygame.K_r])
        mouse_right_click = (mpressed[0])

        #Start rewind if R is pressed and hero can rewind
        if rewind:
            self.hero.rewinding()
        
        #Stop the hero when nothing is pressed
        self.hero.stop()

        #Move if not rewinding
        if not self.hero.is_rewinding:
            self.hero.stop()
            self.hero.moviment(up, down, left, right)

            #Shoot if m1 is pressed (in mouse direction)
            if mouse_right_click and self.hero.can_shoot:
                self.hero.shoot()
                direction = np.array(self.aim.position) - np.array((self.hero.centerx , self.hero.centery))
                self.hero.bullet_list.append(Bullet(direction = direction, start_position = (self.hero.centerx, self.hero.centery)))
                

    def onLoop(self, gm):

        #Update hero, aim and bullets positions
        self.hero.updatePosition()
        self.aim.updateToPosition(gm.mousepos)


        #check collision
        is_hero = True
        for bullet_list in [self.hero.bullet_list, self.boss.bullet_list]:
            for bullet in bullet_list:
                bullet.update_position()
                if bullet.keep_on_screen == False:
                    bullet_list.remove(bullet)
                bullet.check_collision(is_hero, self, gm)
            is_hero = False
        
        # for bullet in self.boss.bullet_list:
        #     bullet.update_position()
        #     if bullet.keep_on_screen == False:
        #         self.boss.bullet_list.remove(bullet)

        
        self.boss.do_attack(self)
        self.hero.attack(self)

        #Auxiliary counter
        self.count = (self.count + 1) % 30

     
    def onRender(self,gm):

        #Render Background
        gm.fake_screen.fill((50,50,50))

        #Create and update timetrack
        if not self.hero.is_rewinding:
            self.hero.update_timetrack(self.count)
            
        #Render hero rewinding
        else:
            self.hero.draw_rewind()

        #Render timetrack
        self.hero.render_timetrack(gm)

        #Render hero
        self.hero.draw(gm)

        #Render Boss
        if not self.boss.weak_spots.got_hit:
            if not self.boss.weak_got_hit:
                self.boss.draw(gm)

        #Render aim
        self.aim.draw(gm)

        #Render bullets
        for bullet_list, owner in zip([self.hero.bullet_list, self.boss.bullet_list], [self.hero, self.boss]):
            for bullet in bullet_list:
                bullet.draw(gm, owner)

        self.run_screen(gm)

    def onCleanup(self, gm):
        #Write settings on configuration file
        config = {"fullscreen":gm.fullscreen,"resolution":gm.window_resolution}
        f = open('src/config.txt', 'w')
        f.write(str(config))
        f.close()

        #Quit game
        pygame.quit()
        sys.exit()

    def run(self, gm):

        #Start
        if self.onInit() == False:
            self._running = False
        
        #Infinite loopgm.restartGame()
        while(self._running):
            #Fps limit
            gm.clock.tick(60)

            if(self._running):
                #Get keys pressed and mouse infos
                self.onEvent(gm)

            if(self._running):
                #Act and update 
                self.onLoop(gm)

            #This if is needed when the player dies, so it doesnt render the game when going though menus
            if(self._running):
                #Render
                self.onRender(gm)
        
        #Finish all
        #self.onCleanup()


    def endGame(self, gm):
        #Delete last session
        del self.hero
        del self.aim
        del self.boss

        self._running = False
   

    def restartGame(self,gm):

        #Some needed stuff
        self._running = True
        
        self.stage = 1
        self.count = 0

        #Instantiating hero and aim
        self.hero = Hero(gm.original_resolution)
        gm.mousepos=pygame.mouse.get_pos()
        self.aim = Aim(gm.mousepos)

        #Boss
        self.boss = Boss_1(gm.original_resolution)