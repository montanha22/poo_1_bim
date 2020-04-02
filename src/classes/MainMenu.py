from .Menu import Menu
import pygame_gui
import pygame

class MainMenu(Menu):

    def __init__(self,window_resolution,clock,game_manager):
        Menu.__init__(self,window_resolution,clock,self.main_menu_buttons,game_manager)
        (x,y)=window_resolution

        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(int(x/2),int(y/2),100,20),text='Start Game',manager=self.manager,anchors={"left":"left","right":"right","top":"top","bottom":"bottom"})
        self.title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(int(x/2),int(y/30),200,40),text="Boss Slayer",manager=self.manager)


    def main_menu_buttons(self,event):
        if event.ui_element == self.play_button:
            self.game_manager.onExecute()



