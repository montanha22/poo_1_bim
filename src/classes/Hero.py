import pygame
import glob
#import definitions
from .GameObject import GameObject
import numpy as np
import cv2
from .Spritesheet import SpriteSheet
class Hero(GameObject):

    def __init__(self):
        GameObject.__init__(self)
        #Load all Hero sprites
        self.spritesheetUp = pygame.image.load('sprites/TopDownCharacter/Character/Character_Up.png')
        self.spritesheetDown = pygame.image.load('sprites/TopDownCharacter/Character/Character_Down.png')
        self.spritesheetLeft = pygame.image.load('sprites/TopDownCharacter/Character/Character_Left.png')
        self.spritesheetRight = pygame.image.load('sprites/TopDownCharacter/Character/Character_Right.png')

        self.spritesheetDownLeft = pygame.image.load('sprites/TopDownCharacter/Character/Character_DownLeft.png')
        self.spritesheetDownRight = pygame.image.load('sprites/TopDownCharacter/Character/Character_DownRight.png')
        self.spritesheetUpLeft = pygame.image.load('sprites/TopDownCharacter/Character/Character_UpLeft.png')
        self.spritesheetUpRight = pygame.image.load('sprites/TopDownCharacter/Character/Character_UpRight.png')
        
        #self.ss = SpriteSheet('sprites/TopDownCharacter/Character/Character_Down.png')
        self.ss = self.spritesheetDown
        #self.spriteIdle = self.spriteDown
        #print(self.spriteDown_list)
        #Hero actual sprite
        self.sprite = pygame.transform.scale(self.ss.subsurface(pygame.Rect(0,0,32,32)), (100,100))

        self.current_sprite_number = 0
    

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

    def updateSprite(self):

        if self.velocity[0] == 1:
            if self.velocity[1] == 1:
                self.sprite = self.spritesheetDownRight
            elif self.velocity[1] == -1:
                self.sprite = self.spritesheetUpRight
            else:
                self.sprite = self.spritesheetRight

        elif self.velocity[0] == -1:

            if self.velocity[1] == 1:
                self.sprite = self.spritesheetDownLeft
            elif self.velocity[1] == -1:
                self.sprite = self.spritesheetUpLeft
            else:
                self.sprite = self.spritesheetLeft
        else:
            if self.velocity[1] == 1:
                self.sprite = self.spritesheetDown
            elif self.velocity[1] == -1:
                self.sprite = self.spritesheetUp
            else:
                self.sprite = pygame.transform.scale(self.spritesheetDown.subsurface(pygame.Rect(0,0,32,32)), (100, 100))
                return None
        self.current_sprite_number = (self.current_sprite_number + 1) % 4
        self.sprite = pygame.transform.scale(self.sprite.subsurface(pygame.Rect(32*self.current_sprite_number, 0, 32, 32)), (100,100))


    def updatePosition(self):
        self.updateSprite()
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


