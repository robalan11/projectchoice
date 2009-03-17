import pygame

import AnimatedSprite
import DisasterEngine

pygame.init()

class Towers(AnimatedSprite.AnimatedSprite):
    """Define the tower variables"""
    
    def __init__(self, pos):
        AnimatedSprite.AnimatedSprite.__init__(self, pos)
        #initialize the int variables
        
        self.mixer = pygame.mixer.Sound("data/audio/Tornado.wav");
        self.towertype=type
       
    def update(self):
        AnimatedSprite.AnimatedSprite.update(self)
    
    
    
