import pygame
import glob
#import definitions
from .GameObject import GameObject


class Hero(GameObject):

    def __init__(self):
        GameObject.__init__(self)
        #Load all Hero sprites
        self.spriteUp_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Up/*.png")]
        self.spriteDown_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Down/*.png")]
        self.spriteLeft_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Left/*.png")]
        self.spriteRight_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Right/*.png")]
        self.spriteIdle_list = [pygame.image.load(i) for i in glob.glob("./sprites/hero/Idle/*.png")]
        
        #Hero actual sprite
        self.sprite = self.spriteIdle_list[0]


    

    def draw(self, screen):
        pass




    def moveUp(self):

        self.sprite = self.spriteUp_list[0]
        self.position[1]-=self.object.speed

    def moveDown(self):

        self.sprite = self.spriteUp_list[0]
        self.position[1]+=self.object.speed

    def moveLeft(self):

        self.sprite = self.spriteUp_list[0]
        self.position[0]-=self.object.speed

    def moveRight(self):

        self.sprite = self.spriteUp_list[0]
        self.position[0]+=self.object.speed