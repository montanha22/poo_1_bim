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
        if self.velocity[0] == 0 or self.velocity[1] == 0:
            scale_factor = 10
        else:
            scale_factor = 10 / np.sqrt(2)
        self.velocity = [i * scale_factor for i in self.velocity]
        self.move_ip(self.velocity[0], self.velocity[1])
    
    def stop(self):
        self.stopLeftRigth()
        self.stopUpDown()