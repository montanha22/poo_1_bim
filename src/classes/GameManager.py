import pygame
import sys
from random import sample
import glob
from classes.EventManager import EventManager

class GameManager():
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1080, 720
        self.background_list = []
        self.stage = 1
        self.count = 0
        self.current_background = None
        self.clock = pygame.time.Clock()
        self.fullscreen = True
        self.eventmanager = EventManager()

    def onInit(self):
        pygame.init()
        screen_info = pygame.display.Info()
        #print(screen_info.current_w, screen_info.current_h)
        #Resizable resizes the display but game doesnt scale up nor down
        self._display_surf = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.fullscreen = True
        self._running = True
        self.background_list = [pygame.image.load(i) for i in glob.glob("./sprites/stages/" + str(self.stage) + "/background/*.png")]
        print(len(self.background_list))
        print(glob.glob("./sprites/stages/" + str(self.stage) + "/background/*.png"))


    def onEvent(self, event):
        #Main system events
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
            self.toggleFullscreen()
        
        #In game events
        else:
            self.eventmanager.getEvent(event)
        
    def onLoop(self):
        pass

    def toggleFullscreen(self):
            pygame.display.toggle_fullscreen()
            


    def onRender(self):
        if self.count == 0 or self.current_background == None:
            self.current_background = sample(self.background_list, 1)[0]
        self._display_surf.blit(self.current_background, (0,0))
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
            # get events
            for event in pygame.event.get():
                self.onEvent(event)
            # act
            self.onLoop()
            # atualization and render
            self.onRender()
        
        self.onCleanup()

