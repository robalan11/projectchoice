import pygame, sys,os, menus
from pygame.locals import * 
from math import *
import random
import AnimatedSprite
from LightningTower import *
import time

START_X = 79
START_Y = 15
def load_image(name):
    """
    Given the name of an image file located inside the data directory, load
    the image. If loading fails, display an error message.
    """
    fullname = os.path.join('data/images', name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    return image
    
class DisasterEngine:
    towerList = None
    bulletList = None
    surface = None
    lives=50
    level=0
    money=100
    grid= None
    myPath=None
    def __init__(self, screen, resolution):
        pygame.init()
        #load images
        
        Tile.standard_img = load_image("Floor.png")
        self.border = load_image("border.png")
        self.mapImage = load_image("Game.png")
        self.useImage = self.mapImage
        self.GridImage = load_image("Game_Grid.png")
	self.placespeed=20
        
        #musac
        pygame.mixer.init()
        
        self.screen = screen #pygame screen passed in from main
        self.resolution = resolution #resolution of the game passed in from main
        self.mode="normal"
       
       
        self.difficulty = 1.0 #type in the difficulty multiplier for health
        self.gui=menus.GUI()
        surface = screen
        """[Floor,Leftwall,Topwall,Inner,Enemies,Items,Cinimatic]"""
        DisasterEngine.grid=[
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           [['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.'],['.','.','.','.','.','.','.']],
           ]
        # Set up the background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((237, 237, 215))
        
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        
        #Internal clock is not the time to calculate occurences in the game use getRealTime for that
        self.internalTime = pygame.time.Clock()
        
        #This is the time in millis of paused time 
        self.deadTime = 0
        self.updateCount = 0
        self.placingUnits = False
        self.placeCount = 0;
        
        #TowerLists
        DisasterEngine.towerList = pygame.sprite.Group()
        
        self.shiftHeld = True
        
        #This is the fonts section for the HUD
        self.alertText ="Game Begin"
        self.alertFont = pygame.font.Font(pygame.font.match_font("Arial"), 70)
        
        self.gameover = False
    def getRealTime(self):
        return self.internalTime - self.deadTime
        
    def update(self):
                
        if self.mode =="normal":
            self.useImage = self.mapImage
        else:
            self.useImage = self.GridImage
        DisasterEngine.towerList.update()
        self.gui.update()
        
    def render(self):
        #print "rendering"
        self.screen.fill((237, 237, 215))
        self.screen.blit(self.useImage, (0,0))
        self.screen.blit(self.border, (0,0))
        if self.gui.towertype!='None' and self.getZone()[0]< (self.resolution[1]/32 -2) and self.getZone()[0] >= 1 and self.getZone()[1] < (self.resolution[1]/32 -2) and self.getZone()[1] >= 1:  #Only draw the highlight on the game field
            self.highlightZone(self.getZone())
        alertLiteral = self.alertFont.render(str(self.alertText), 1, (255, 120, 87))
        self.screen.blit(alertLiteral, (1000-(15*len(self.alertText)),525-70))
        DisasterEngine.towerList.draw(self.screen)
        
        self.gui.draw(self.screen)
        
        #for x in range(28):
        #    for y in range(28):
        #        if self.grid[x][y]== 1:
        #            pygame.draw.rect(self.screen,(255,255,255),pygame.Rect((x*32),(y*32),32,32))
        pygame.display.flip()
        
    def sendAlert(self, alertText, alertLengthMillis):
        self.alertText=alertText
        currenttime = pygame.time.get_ticks();
        alerttime = currenttime + alertLengthMillis
        
        while pygame.time.get_ticks() < alerttime:
            alertLiteral = self.alertFont.render(str(self.alertText), 1, (255, 255, 255))
            self.screen.blit(alertLiteral, (700-(15*len(self.alertText)),525-70))
            pygame.display.flip()
            
    def getZone(self):
        mousepos = pygame.mouse.get_pos()
        zone = (mousepos[0]/32, mousepos[1]/32)
        return zone
        
    def highlightZone(self, zone):
        #pygame.draw.rect(self.screen, Color.black, rect, 2)
        #self.background.fill((255,255,255), zone)
        if self.mode=="grid":
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(zone[0]*32,zone[1]*32,64,64) )
    def saveMap(self, filename):
        f=open(filename,'w')
        for y in range(len(self.grid)):
            temp=""
            for x in range(len(self.grid[y])):
                for i in range(7):
                    temp=temp+self.grid[y][x][i]
                if x<len(self.grid[y])-1 :
                    temp= temp+","
            print >>f, temp
                                
    def run(self):
        while not self.gameover and self.lives>0 and self.level<12:
            self.update()
            self.render()
            
            self.sendAlert(self.getZone(), 0)
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_LSHIFT:
                    if self.shiftHeld:
                        self.shiftHeld = False
                if event.type == KEYUP and event.key == K_LSHIFT:
                    if not self.shiftHeld:
                        self.shiftHeld = True
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
                if event.type == KEYDOWN and event.key == K_s:
                    self.saveMap("ExportedMap.txt")
                if event.type == MOUSEBUTTONDOWN and event.button==1: #Clicked left button
                    if event.pos[0]>self.resolution[1]-32: #Clicked in the GUI
                        self.mode="grid"
                        self.gui.settower() #update the gui
                        if self.gui.towertype == 'None':
                            self.mode = "normal"
                    elif self.gui.towertype!='None' and self.mode == "grid" and self.getZone()[0]< (self.resolution[1]/32 -2) and self.getZone()[0] >= 1 and self.getZone()[1] < (self.resolution[1]/32 -2) and self.getZone()[1] >= 1:
                        tempPos = event.pos
                        towerPos = ((tempPos[0]-(tempPos[0]%32))+32,(tempPos[1]-(tempPos[1]%32))+32)
                        
                        myPos=[(towerPos[0]-32)/32,(towerPos[1]-32)/32]
                        """tower1 = Tile(towerPos,self.gui.towertype)"""
                        tower1 = Tile(towerPos,self.gui.towertype)
                        if not DisasterEngine.grid[myPos[0]][myPos[1]][self.gui.towertype[0]]==self.gui.towertype[1]:
                            self.towerList.add(tower1)
                            
                            DisasterEngine.grid[myPos[0]][myPos[1]][self.gui.towertype[0]]=self.gui.towertype[1]
                            if not DisasterEngine.myPath==None:
                                self.mixer = pygame.mixer.Sound("data/audio/Place.wav");
                                self.mixer.play()
                        if not self.shiftHeld:
                            self.mode="normal"
                if event.type == MOUSEBUTTONDOWN and event.button==3: #Clicked right button
                    on_tower=False
                    for tower in DisasterEngine.towerList:
                        if tower.rect.collidepoint(event.pos):
                            self.mixer = pygame.mixer.Sound("data/audio/SellTower.wav");
                            self.mixer.play()
                            on_tower=True
                            myPos=[tower.centerx/32-1,tower.centery/32-1]
                            DisasterEngine.grid[myPos[0]][myPos[1]]=['.','.','.','.','.','.','.']
                            tower.kill()
                    if not on_tower: #Cancel Tower placement
                        self.gui.towertype='None'
	while self.level>1:
	    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0,0,1200,896))
            win=pygame.image.load("data/images/Win_Screen.png")
            self.screen.blit(win,(152,0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    return;