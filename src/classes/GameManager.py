import pygame
import sys
from random import sample
import glob

class GameManager():
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1080, 720
        self.background_list = []
        self.stage = 1
        self.count = 0
        self.current_background = None
        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.init()
        screen_info = pygame.display.Info()
        #print(screen_info.current_w, screen_info.current_h)
        self._display_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self._running = True
        self.background_list = [pygame.image.load(i) for i in glob.glob("./sprites/stages/" + str(self.stage) + "/background/*.png")]
        print(len(self.background_list))
        print(glob.glob("./sprites/stages/" + str(self.stage) + "/background/*.png"))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._running = False
    
    def on_loop(self):
        pass

    def on_render(self):
        if self.count == 0 or self.current_background == None:
            self.current_background = sample(self.background_list, 1)[0]
        self._display_surf.blit(self.current_background, (0,0))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
    
        while(self._running):
            self.clock.tick(60)
            self.count = (self.count + 1) % 30
            # get events
            for event in pygame.event.get():
                self.on_event(event)
            # act
            self.on_loop()
            # atualization and render
            self.on_render()
        
        self.on_cleanup()
