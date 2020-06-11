from classes.GameOverScreen import *
from classes.MenuScreen import *
from classes.OptionsScreen import *
from classes.QuitConfirmationScreen import *
from classes.PauseScreen import *
from classes.GameScreen import *
import pygame 
import pygameMenu

from pygame.locals import *
import sys
from random import sample
import glob

import numpy as np
from numpy import linalg as LA
import time

import ast


class GameManager():
    def __init__(self):

        pygame.init()
        self.mousepos = pygame.mouse.get_pos()
        self.clock = pygame.time.Clock()

        #Read config file
        f = open('src/config.txt', 'r')
        config = f.read()
        config = ast.literal_eval(config)
        f.close()

        #Window resolution
        self.window_resolution=config["resolution"]
        self.original_resolution = (1920,1080)
        self.monitor_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h) #Needs to be before screen and fake_screen declaration
        self.fullscreen = config["fullscreen"]

        #Text font
        self.font = pygame.font.Font("sprites/menu/kenvector_future.ttf", 20)
        
        self.screen = pygame.display.set_mode(self.original_resolution, pygame.NOFRAME)
        self.fake_screen=self.screen.copy()
        
        if self.fullscreen:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))
        else:
            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = self.window_resolution, w = self.window_resolution[0],h=self.window_resolution[1]))


        #Inicializando telas
        self.game_screen = GameScreen(self)
        self.game_over_screen = GameOverScreen(self)
        self.menu_screen = MenuScreen(self)
        self.options_screen = OptionsScreen(self)
        self.pause_screen = PauseScreen(self)
        self.quit_confirmation_screen = QuitConfirmationScreen(self)
        
        self.actual_screen = self.menu_screen
        self.running = True

    def run(self):
            while self.running:
                self.actual_screen.run(self)

    def play(self):
        
        #Adjust initial screen resolution
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.fullscreen = False
                self.window_resolution=event.size
                self.screen = pygame.display.set_mode(event.size)
                self.screen.blit(pygame.transform.scale(self.fake_screen, self.window_resolution), (0, 0))
                pygame.display.flip()
                
            if event.type == pygame.USEREVENT + 1:
                self.fullscreen = True
                self.window_resolution = self.monitor_resolution
                self.screen = pygame.display.set_mode(self.window_resolution, pygame.FULLSCREEN)
                self.screen.blit(pygame.transform.scale(self.fake_screen, self.window_resolution), (0, 0))
                pygame.display.flip()
