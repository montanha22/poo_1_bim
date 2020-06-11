import pygame
from classes.Screen import *
from classes.Button import *
import sys

class WinScreen(Screen):
    def __init__(self, gm):
        super().__init__()
        self.mainmenu_button = Button(50, 100, 200, 50, "Main Menu", gm)
        self.quit_button = Button(300, 100, 200, 50, 'Quit Game', gm)

    def run(self,gm):

        click = False
        running = True
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("sounds/Win.ogg"))

        while running:
            gm.clock.tick(60)
            gm.fake_screen.blit(gm.game_screen.background,gm.game_screen.background.get_rect())
            gm.game_screen.hero.draw(gm)
            self.draw_text('You win', gm.font_big, (255, 255, 255), gm.fake_screen, (960,350))
            self.draw_text('Score: {}'.format(int(gm.game_screen.score)), gm.font_med, (255, 255, 255), gm.fake_screen, (960,550))
    
            mx, my = gm.mousepos

            #Avalia botão quit
            if self.quit_button.contour.collidepoint((mx, my)):
                self.quit_button.draw(True,gm)
                if click:
                    gm.actual_screen = gm.quit_confirmation_screen
                    running = False
            else:
                self.quit_button.draw(False,gm)
            
            #Avalia botão menu
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
                    gm.game_screen.onCleanup(gm)
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    gm.actual_screen = gm.quit_confirmation_screen
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                    
            self.run_screen(gm)