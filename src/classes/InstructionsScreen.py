import pygame
from classes.Screen import *
from classes.Button import *

class InstructionsScreen(Screen):
    def __init__(self, gm):
        super().__init__()
        self.mainmenu_button = Button(50, 900, 200, 50, "Main Menu", gm)
        self.keys_image = pygame.image.load('imgs/teclas.png')
        self.mouse_image = pygame.image.load('imgs/mouse_click.png')
        self.esc_image = pygame.image.load('imgs/esc.png')

    def run(self, gm):
        
        running = True
        click = False
     
        while running:
            gm.clock.tick(60)
            gm.fake_screen.fill((0,0,0))
            self.draw_text('Instructions', gm.font, (255, 255, 255), gm.fake_screen, ((960,20)))
            gm.fake_screen.blit(self.keys_image, [100,150])
            self.draw_text('Movimentar jogador', gm.font_p, (255, 255, 255), gm.fake_screen, ((1100,200)))
            gm.fake_screen.blit(self.mouse_image, [200,380])
            self.draw_text('Atirar', gm.font_p, (255, 255, 255), gm.fake_screen, ((1100,480)))
            gm.fake_screen.blit(self.esc_image, [200,650])
            self.draw_text('Pausar', gm.font_p, (255, 255, 255), gm.fake_screen, ((1100,750)))

            mx, my = gm.mousepos
           
           #Selecionar botão
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