import pygame
from classes.Screen import *
from classes.Button import *

class GameOverScreen(Screen):
    def __init__(self, gm):
        super().__init__()
        self.mainmenu_button = Button(50, 100, 200, 50, "Main Menu", gm)
        self.quit_button = Button(300, 100, 200, 50, 'Quit Game', gm)

    def run(self,gm):

        click = False
        running = True
        gm.game_screen.endGame(gm)
    
        while running:
            gm.clock.tick(60)
            gm.fake_screen.fill((0,0,0))
            self.draw_text('Game Over', gm.font, (255, 255, 255), gm.fake_screen, (960,20))
    
            mx, my = gm.mousepos

            if self.quit_button.contour.collidepoint((mx, my)):
                self.quit_button.draw(True,gm)
                if click:
                    gm.actual_screen = gm.quit_confirmation_screen
                    running = False
            else:
                self.quit_button.draw(False,gm)
            
            if self.mainmenu_button.contour.collidepoint((mx, my)):
                self.mainmenu_button.draw(True, gm)
                if click:
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