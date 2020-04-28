import pygame
import sys
from classes.Button import *
from classes.Screen import *
from classes.Spritesheet import SpriteSheet


class MenuScreen(Screen):

    def __init__(self,gm, background = "sprites/menu/game_background_4.png"):
        super().__init__(background)
        self.play_button = Button(860, 100, 200, 50, 'Play Game', gm)
        self.options_button = Button(860, 200, 200, 50, 'Settings', gm)
        self.quit_button = Button(860, 300, 200, 50, 'Quit Game', gm)


    def run(self, gm):

        click = False
        can_play_sound=True
        running = True

        while running:
            gm.clock.tick(60)
            gm.fake_screen.blit(self.background,self.background.get_rect())
            self.draw_text('Main Menu', gm.font, (255, 255, 255), gm.fake_screen, (960,20))
            mx, my = gm.mousepos

            #Seleção dos botões
            if self.play_button.contour.collidepoint((mx, my)):
                self.play_button.draw(True, gm)
                if can_play_sound:
                    can_play_sound = False
                    self.play_button.sound(True, False)
                if click:
                    self.play_button.sound(False, True)
                    gm.game_screen.restartGame(gm)
                    gm.actual_screen = gm.game_screen
                    running = False
                
            else:
                self.play_button.draw(False, gm)
                can_play_sound = True

            if self.options_button.contour.collidepoint((mx, my)):
                self.options_button.draw(True, gm)
                #print ('fg')
                if click:
                    print ('oi')
                    gm.actual_screen = gm.options_screen
                    running = False
            else:
                self.options_button.draw(False, gm)

            if self.quit_button.contour.collidepoint((mx, my)):
                self.quit_button.draw(True,gm)
                if click:
                    gm.actual_screen = gm.quit_confirmation_screen
                    running = False
            else:
                self.quit_button.draw(False,gm)
     
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gm.game_screen.onCleanup(gm)
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    gm.actual_screen = gm.quit_confirmation_screen

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            self.run_screen(gm)