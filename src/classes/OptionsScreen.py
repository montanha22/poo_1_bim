import pygame
from classes.Screen import *
from classes.Button import *

class OptionsScreen(Screen):
    def __init__(self, gm):
        super().__init__()
        self.button_1 = Button(50, 100, 200, 50, "960 x 540", gm)
        self.button_2 = Button(50, 200, 200, 50, "1280 x 720", gm)
        self.button_3 = Button(50, 300, 200, 50, "1920 x 1080", gm)
        self.button_4 =Button(50, 400, 200, 50, "Fullscreen", gm)
        self.mainmenu_button = Button(50, 500, 200, 50, "Main Menu", gm)

    def run(self, gm):
    
        running = True
        click = False
       
        while running:
            gm.clock.tick(60)
            gm.fake_screen.fill((0,0,0))
            self.draw_text('Options', gm.font, (255, 255, 255), gm.fake_screen, ((960,20)))

            mx, my = gm.mousepos
           
           #Selecionar botão
            if self.button_1.contour.collidepoint((mx, my)):
                self.button_1.draw(True, gm)
                if click:
                    self.post_resize_event((960,540))
            else:
                self.button_1.draw(False, gm)

            if self.button_2.contour.collidepoint((mx, my)):
                self.button_2.draw(True, gm)
                if click:
                    self.post_resize_event((1280,720))
            else:
                self.button_2.draw(False, gm)

            if self.button_3.contour.collidepoint((mx, my)):
                self.button_3.draw(True, gm)
                if click:
                    self.post_resize_event((1920,1080))
            else:
                self.button_3.draw(False, gm)

            if self.button_4.contour.collidepoint((mx, my)):
                self.button_4.draw(True, gm)
                if click:
                    self.post_fullscreen()        
            else:
                self.button_4.draw(False, gm)

            if self.mainmenu_button.contour.collidepoint((mx, my)):
                self.mainmenu_button.draw(True, gm)
                if click:
                    gm.actual_screen =  gm.menu_screen
                    running = False
            else:
                self.mainmenu_button.draw(False, gm)


            click = False


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gm.game_screen.onCleanup(gm)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.type == pygame.VIDEORESIZE:
                    if gm.window_resolution != event.size:
                        gm.fullscreen = False
                        gm.window_resolution = event.size
                        gm.screen = pygame.display.set_mode(event.size)
                        gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
                        pygame.display.flip()
                
                if event.type == pygame.USEREVENT + 1:
                    if not gm.fullscreen:
                        gm.fullscreen = True
                        gm.window_resolution = gm.monitor_resolution
                        gm.screen = pygame.display.set_mode(gm.window_resolution, pygame.FULLSCREEN)
                        gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
                        pygame.display.flip()

            self.run_screen(gm)