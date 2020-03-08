import pygame
import glob
#import definitions
from .GameObject import GameObject
import numpy as np

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
        self.velocity[1] = -1

    def moveDown(self):
        self.velocity[1] = 1

    def moveLeft(self):
        self.velocity[0] = -1

    def moveRight(self):
        self.velocity[0] = 1

    def stopLeftRigth(self):
        self.velocity[0] = 0

    def stopUpDown(self):
        self.velocity[1] = 0

    def updatePosition(self):
        #print(self.velocity)
        self.move_ip(10*self.velocity[0], 10*self.velocity[1])
    
    def stop(self):
        self.stopLeftRigth()
        self.stopUpDown()