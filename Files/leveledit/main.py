import pygame, sys,os 
from pygame.locals import *
import DisasterEngine

def main(): 
    #function Main
    resolution = (1200, 896)
    fullscreen = False
    
    if fullscreen:
        screen = pygame.display.set_mode((resolution[0], resolution[1]), pygame.FULLSCREEN) 
    else:
        screen = pygame.display.set_mode((resolution[0], resolution[1]))
    # Set up the title screen
    title=pygame.image.load("data/images/Game_with_Options.png")
    screen.blit(title,(152,0))
    pygame.display.flip()
    run="no" #set a variable to run so I can consolidate code below when you click
    while 1:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0,0,1200,896))
        if run=="no":
            screen.blit(title,(152,0))
        
            x,y=pygame.mouse.get_pos()
            
            pygame.display.flip()
            for event in pygame.event.get():  #choose difficulty
            #650, 200 ->750, 232 easy; 632, 263 -> 760, 300 normal; 610, 335->790, 370 ridiculous; offset 152
                run="yes" #set to yes so exits the while
        else: #if run =yes, run the game....
            title=pygame.image.load("data/images/Instructions.png")
            screen.blit(title,(152,0))
            pygame.display.flip()
            for event in pygame.event.get(): #wait for a button to get hit
                if event.type == MOUSEBUTTONDOWN:
                    engine = DisasterEngine.DisasterEngine(screen, resolution)
                    engine.run()
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                        return
                
#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
