import pygame
import glob
#import definitions
from classes.GameObject import GameObject


class Hero():

    def __init__(self):

        #Load all Hero sprites
        self.spriteUp_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Up/*.png")]
        self.spriteDown_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Down/*.png")]
        self.spriteLeft_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Left/*.png")]
        self.spriteRight_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Right/*.png")]
        self.spriteIdle_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Idle/*.png")]
        
        #Hero actual sprite
        self.sprite = self.spriteIdle_list[0]

        #Hero object
        self.object = GameObject(2,(0,0))


    def moveUp(self):

        self.sprite = self.spriteUp_list[0]
        self.object.y+=self.object.speed
