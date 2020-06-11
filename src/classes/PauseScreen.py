import pygame
from classes.Screen import *
from classes.Button import *


class PauseScreen(Screen):
    def __init__(self, gm):
        super().__init__()
        self.resume_button = Button(50, 100, 200, 50, "Resume", gm)
        self.mainmenu_button = Button(50, 200, 200, 50, "Main Menu", gm)
    
    def run(self, gm):

        click=False
        running = True
        
        while running:

            gm.clock.tick(60)
            gm.fake_screen.fill((0,0,0))
            self.draw_text('Pause Menu', gm.font, (255, 255, 255), gm.fake_screen, (960,20))
    
            mx, my = gm.mousepos

            #Seleciona botões
            if self.resume_button.contour.collidepoint((mx, my)):
                self.resume_button.draw(True, gm)
                if click:
                    gm.actual_screen = gm.game_screen
                    running = False 
            else:
                self.resume_button.draw(False, gm)

            if self.mainmenu_button.contour.collidepoint((mx, my)):
                self.mainmenu_button.draw(True, gm)
                if click:
                    gm.game_screen.new_game(gm)
                    gm.actual_screen = gm.menu_screen 
                    running = False
            else:
                self.mainmenu_button.draw(False, gm)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gm.game_screen.onCleanup()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            self.run_screen(gm)