import pygame
import ast

class Screen():

    def __init__(self,background = "imgs/black_screen.png"):
        self.background = pygame.image.load(background).convert()

    def run_screen(self, gm):

        #Display refresh
        gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
        pygame.display.flip()

        #Fix mouse position because of resizing
        gm.mousepos = list(pygame.mouse.get_pos())
        gm.mousepos = [int(gm.mousepos[0]*gm.original_resolution[0]/gm.window_resolution[0]),int(gm.mousepos[1]*gm.original_resolution[1]/gm.window_resolution[1])]
        gm.mousepos=tuple(gm.mousepos)

    def draw_text(self, text, font, color, surface, pos):
            textobj = font.render(text, True, color)
            textrect = textobj.get_rect()
            textrect.center = (pos[0]-5,pos[1])
            surface.blit(textobj, textrect)

    def post_resize_event(self,resolution):
        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = resolution, w = resolution[0],h=resolution[1]))

    def post_fullscreen(self):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))