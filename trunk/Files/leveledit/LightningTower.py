import pygame, sys,os, menus
from pygame.locals import * 
from math import *
import AnimatedSprite
import DisasterEngine
import Towers

def load_image(name):
    """
    Given the name of an image file located inside the data directory, load
    the image. If loading fails, display an error message.
    """
    fullname = os.path.join('data\images', name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    return image

class Tile(Towers.Towers):
    def __init__(self, pos, type):
        self.standard_img=load_image( "%d%s%s" %( type[0] , type[1] , ".png") )
        Towers.Towers.__init__(self, pos)
        self.type=type[1]
        
       
    def update(self):
        Towers.Towers.update(self)