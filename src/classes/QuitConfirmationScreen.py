import pygame
from classes.Screen import *
from classes.Button import *

class QuitConfirmationScreen(Screen):
    def __init__(self, gm):
        super().__init__()
        self.button_1 = Button(50, 100, 200, 50, "Cancel", gm)
        self.button_2 = Button(350, 100, 200, 50, "Quit", gm)
       

    def run(self, gm):
        
        running = True
        click=False
        while running:
            gm.clock.tick(60)
            gm.fake_screen.fill((0,0,0))
            self.draw_text('Do you really want to quit?', gm.font, (255, 255, 255), gm.fake_screen, (960,20))
    
            mx, my = gm.mousepos
    
            if self.button_1.contour.collidepoint((mx, my)):
                self.button_1.draw(True, gm)
                if click:
                    running = False
                    gm.actual_screen = gm.menu_screen

            else:
                self.button_1.draw(False, gm)

            if self.button_2.contour.collidepoint((mx, my)):
                self.button_2.draw(True, gm)
                if click:
                    gm.game_screen.onCleanup(gm)

            else:
                self.button_2.draw(False, gm)
    
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gm.game_screen.onCleanup(gm)
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    gm.actual_screen = gm.menu_screen

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            self.run_screen(gm)