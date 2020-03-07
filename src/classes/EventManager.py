
import pygame

class EventManager():
    def __init__(self):
        self.event = None

    def getEvent(self,event):
        self.event = event
        self.resolveEvent(event)
        

    def resolveEvent(self,event):
        pass
    