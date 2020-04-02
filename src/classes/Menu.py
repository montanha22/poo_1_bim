import pygame
import pygame_gui


class Menu ():
    def __init__(self,window_resolution,clock,buttonfunc,game_manager):
        self.manager = pygame_gui.UIManager(window_resolution,"../sprites/menu/theme.json")
        self.time_delta = clock.tick(60)/1000.0
        self.buttonfunc = buttonfunc
        self.game_manager = game_manager
        

    def mainloop(self,surface):
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu=False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        self.buttonfunc(event)
                self.manager.process_events(event)

            self.manager.update(self.time_delta)
            
            self.manager.draw_ui(surface)
            pygame.display.update()
        


