import pygame
from classes.GameObject import *
from classes.GameScreen import *
import math

class Laser(pygame.Rect):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.angle = 90
        self.color1 = ( 128,   0,   0)
        self.color2 = ( 218,   165,   32)
        self.x1 = 1000
        self.x2 = 0
        self.y1 = 1000
        self.y2 = 0
        self.interval = True
    
    def new_laser(self):
        self.angle = 90
        self.x1 = 1000
        self.x2 = 0
        self.y1 = 1000
        self.y2 = 0
        self.interval = True

    def laserDraw(self,x_origen,y_origen,radius,gm):
        
        self.y1 = y_origen - radius*math.sin(self.angle*math.pi/180)
        self.x1 = x_origen - radius*math.cos(self.angle*math.pi/180)
        self.x2 = self.x1 - 3000*math.cos(self.angle*math.pi/180)
        self.y2 = self.y1 - 3000*math.sin(self.angle*math.pi/180)
      
        pygame.draw.line(gm.fake_screen, self.color1, (self.x1, self.y1), (self.x2,self.y2), 30)
        pygame.draw.line(gm.fake_screen, self.color2, (self.x1, self.y1), (self.x2,self.y2), 10)
 


    def collideLineLine(self, l1_p1, l1_p2, l2_p1, l2_p2):
    
        # normalized direction of the lines and start of the lines
        P  = pygame.math.Vector2(*l1_p1)
        line1_vec = pygame.math.Vector2(*l1_p2) - P
        R = line1_vec.normalize()
        Q  = pygame.math.Vector2(*l2_p1)
        line2_vec = pygame.math.Vector2(*l2_p2) - Q
        S = line2_vec.normalize()

        # normal vectors to the lines
        RNV = pygame.math.Vector2(R[1], -R[0])
        SNV = pygame.math.Vector2(S[1], -S[0])

        # distance to the intersection point
        QP  = Q - P
        if R.dot(SNV) == 0:
            t = 1
            u = 10000
        else:
            t = QP.dot(SNV) / R.dot(SNV)
            u = QP.dot(RNV) / R.dot(SNV)

        return t > 0 and u > 0 and t*t < line1_vec.magnitude_squared() and u*u < line2_vec.magnitude_squared()
    
    def collisionLaser(self, gm):
        
        if  self.collideLineLine((self.x1, self.y1), (self.x2,self.y2), (gm.game_screen.hero.left,gm.game_screen.hero.bottom-48), (gm.game_screen.hero.left,gm.game_screen.hero.bottom)) or self.collideLineLine((self.x1, self.y1), (self.x2,self.y2),  (gm.game_screen.hero.left,gm.game_screen.hero.bottom),  (gm.game_screen.hero.left+48,gm.game_screen.hero.bottom)) or self.collideLineLine((self.x1, self.y1), (self.x2,self.y2),  (gm.game_screen.hero.left+48,gm.game_screen.hero.bottom),  (gm.game_screen.hero.left+48,gm.game_screen.hero.bottom-48)) or self.collideLineLine((self.x1, self.y1), (self.x2,self.y2), (gm.game_screen.hero.left+48,gm.game_screen.hero.bottom-48),  (gm.game_screen.hero.left,gm.game_screen.hero.bottom-48)):
            if(not gm.game_screen.hero.is_rewinding): 
                gm.actual_screen = gm.game_over_screen
                gm.game_screen._running = False
 

  
           
