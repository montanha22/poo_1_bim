import pygame
from pygame.locals import *
import sys
from random import sample
import glob
from classes.EventManager import EventManager
from classes.Hero import Hero

class GameManager():
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.width, self.height = 1080, 720
        self.background_list = []
        self.stage = 1
        self.count = 0
        self.current_background = None
        self.clock = pygame.time.Clock()
        self.fullscreen = True
        self.eventmanager = EventManager()
        self.hero = Hero()

    def onInit(self):
        pygame.init()
        screen_info = pygame.display.Info()
        #print(screen_info.current_w, screen_info.current_h)
        #Resizable resizes the display but game doesnt scale up nor down
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.fullscreen = True
        self._running = True
        self.background_list = [pygame.image.load(i) for i in glob.glob("./sprites/stages/" + str(self.stage) + "/background/*.png")]
      #  print(len(self.background_list))
      #  print(glob.glob("./sprites/stages/" + str(self.stage) + "/background/*.png"))


    def onEvent(self):
        pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
                self.toggleFullscreen()
            
        up = (pressed[pygame.K_w] or pressed[pygame.K_UP])
        down = (pressed[pygame.K_s] or pressed[pygame.K_DOWN])
        left = (pressed[pygame.K_a] or pressed[pygame.K_LEFT])
        right = (pressed[pygame.K_d] or pressed[pygame.K_RIGHT])

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

    def onLoop(self):
        self.hero.updatePosition()

    def toggleFullscreen(self):
            pygame.display.toggle_fullscreen()
            


    def onRender(self):
        #Render Background
        self.screen.fill((255,255,255))
        if self.count == 0 or self.current_background == None:
            self.current_background = sample(self.background_list, 1)[0]
        self.screen.blit(self.current_background, (0,0))

        #Render Hero
        self.screen.blit(self.hero.sprite, (self.hero.x, self.hero.y))



        pygame.display.flip()

    def onCleanup(self):
        pygame.quit()
        sys.exit()

    def onExecute(self):
        if self.onInit() == False:
            self._running = False
        
        while(self._running):
            self.clock.tick(60)
            self.count = (self.count + 1) % 30

            # get keys presseds and mouse infos
            self.onEvent()


            # act and update 
            self.onLoop()
            
            # render
            self.onRender()
        
        self.onCleanup()

