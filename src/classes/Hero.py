import pygame
import glob
#import definitions
from .GameObject import GameObject
import numpy as np
from .Spritesheet import SpriteSheet
class Hero(GameObject):

    def __init__(self,resolution):
        self.screen_width = resolution[0]
        self.screen_height = resolution[1]
        GameObject.__init__(self, width=48, height=48, position = [self.screen_width/2, self.screen_height/1.2])
        self.scalar_velocity = 5
        #Load all Hero sprites
        self.spritesheetUp = pygame.image.load('sprites/TopDownCharacter/Character/Character_Up.png')
        self.spritesheetDown = pygame.image.load('sprites/TopDownCharacter/Character/Character_Down.png')
        self.spritesheetLeft = pygame.image.load('sprites/TopDownCharacter/Character/Character_Left.png')
        self.spritesheetRight = pygame.image.load('sprites/TopDownCharacter/Character/Character_Right.png')

        self.spritesheetDownLeft = pygame.image.load('sprites/TopDownCharacter/Character/Character_DownLeft.png')
        self.spritesheetDownRight = pygame.image.load('sprites/TopDownCharacter/Character/Character_DownRight.png')
        self.spritesheetUpLeft = pygame.image.load('sprites/TopDownCharacter/Character/Character_UpLeft.png')
        self.spritesheetUpRight = pygame.image.load('sprites/TopDownCharacter/Character/Character_UpRight.png')
        
        self.shoot_interval = 10
        self.time_last_shoot = 300
        self.bullet_list = []
        self.bullet_color = (0, 0, 255)
        self.timetrack = []
        self.timetracklen = 30
        #self.ss = SpriteSheet('sprites/TopDownCharacter/Character/Character_Down.png')
        self.ss = self.spritesheetDown
        #self.spriteIdle = self.spriteDown
        #print(self.spriteDown_list)
        #Hero actual sprite
        self.sprite_size = (100,100)
        self.sprite = pygame.transform.scale(self.ss.subsurface(pygame.Rect(0,0,32,32)), self.sprite_size)
        self.is_rewinding = False
        self.current_sprite_number = 0
        self.can_shoot = True
        self.can_rewind = False
    

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
                self.sprite = pygame.transform.scale(self.spritesheetDown.subsurface(pygame.Rect(0,0,32,32)), self.sprite_size)
                return None
        self.current_sprite_number = (self.current_sprite_number + 1) % 4
        self.sprite = pygame.transform.scale(self.sprite.subsurface(pygame.Rect(32*self.current_sprite_number, 0, 32, 32)), self.sprite_size)


    def updatePosition(self):
        self.updateSprite()
        #print(self.velocity)
        if self.velocity[0] == 0 or self.velocity[1] == 0:
            self.scalar_velocity = 10
        else:
            self.scalar_velocity = 10 / np.sqrt(2)
        self.velocity = [i * self.scalar_velocity for i in self.velocity]
        #print(self.velocity)
        if self.bottom + self.velocity[1] > self.screen_height or self.top + self.velocity[1] < 0:
            self.velocity[1] = 0
        if self.left + self.velocity[0] < 0 or self.right + self.velocity[0] > self.screen_width:
            self.velocity[0] = 0
        self.move_ip(self.velocity[0], self.velocity[1])
    
    def get_correct_position_to_blit(self):
        return (self.getRect()[0] - 27, self.getRect()[1] - 32)

    def stop(self):
        self.velocity = [0, 0]
        self.stopLeftRigth()
        self.stopUpDown()

    def rewind(self, chronosinfo):
        if chronosinfo == None:
            self.is_rewinding == False
            self.clamp_ip(self.getRect())
        else:
            self.sprite = chronosinfo[0]
            self.clamp_ip(chronosinfo[2])
    
    def shoot(self):
        self.time_last_shoot = 0
        self.can_shoot = False

    def check_collision(self, rect):
        if self.colliderect(rect):
            return True
        return False



