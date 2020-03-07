
import pygame
import glob

class EventManager():
    def __init__(self):
        self.event = None
        
    def getEvent(self,event):
        self.event = event
        self.resolveEvent(event)

    def resolveEvent(self,event):
        
        #Hero movement related events
        pass
    