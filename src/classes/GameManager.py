import pygame
from pygame.locals import *
import sys
from random import sample
import glob
from classes.EventManager import EventManager
from classes.Hero import Hero
from classes.Aim import Aim
from classes.Bullet import Bullet
import numpy as np
from numpy import linalg as LA
import time

class GameManager():
    def __init__(self):

        #Pygame initialization
        pygame.init()

        #Some needed stuff
        self._running = True
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.stage = 1
        self.count = 0
        self.clock = pygame.time.Clock()
        self.fullscreen = True

        #Instantiating hero and aim
        self.hero = Hero()
        self.aim = Aim(pygame.mouse.get_pos())

    def onInit(self):

        #Resizable resizes the display but game doesnt scale up nor down
        self.fullscreen = True
        self._running = True

    def onEvent(self):

        #Getting pressed buttons from keyboard and mouse
        pressed = pygame.key.get_pressed()
        mpressed = pygame.mouse.get_pressed()

        #Checking if the window was closed or ESC was pressed (quit game) or F10 was pressed (toggle fullscreen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
                self.toggleFullscreen()
            
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
        self.aim.updateToPosition(pygame.mouse.get_pos())
        for bullet in self.hero.bullet_list:
            bullet.update_position()
            if bullet.keep_on_screen == False:
                self.hero.bullet_list.remove(bullet)
        self.hero.time_last_shoot = self.hero.time_last_shoot + 1

        if self.hero.time_last_shoot > self.hero.shoot_interval:
            self.hero.can_shoot = True
        #Auxiliary counter
        self.count = (self.count + 1) % 30

    def toggleFullscreen(self):
            pygame.display.toggle_fullscreen()
            
    def onRender(self):
        #Render Background
        self.screen.fill((100,100,100))
        #pygame.draw.rect(self.screen, (155,155,155) , self.hero.getRect())
        
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
                self.screen.blit(temp, trail[1]) 
    
        #Make last timetrack position more darker
        if len(self.hero.timetrack) != 0:
            self.hero.timetrack[0][0].fill((0,0,255,255), special_flags = pygame.BLEND_RGBA_MULT)
            self.screen.blit(self.hero.timetrack[0][0], self.hero.timetrack[0][1])

        #Render hero
        self.screen.blit(self.hero.sprite, self.hero.get_correct_position_to_blit())
        
        #Render aim
        pygame.draw.circle(self.screen, self.aim.color, self.aim.position, self.aim.radius, self.aim.thick)

        #Render hero bullets
        for bullet in self.hero.bullet_list:
            pygame.draw.circle(self.screen, (255, 0, 255), (bullet.centerx, bullet.centery), 10, 10)

        #Display refresh
        pygame.display.flip()

    def onCleanup(self):

        #Quit game
        pygame.quit()
        sys.exit()

    def onExecute(self):

        #Start
        if self.onInit() == False:
            self._running = False
        
        #Infinite loop
        while(self._running):
            #Fps limit
            self.clock.tick(60)

            #Get keys presseds and mouse infos
            self.onEvent()

            #Act and update 
            self.onLoop()

            #Render
            self.onRender()
        
        #Finish all
        self.onCleanup()

