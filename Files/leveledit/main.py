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
            if x>802 and y >200 and x<902 and y<232: #mouse over easy, change pic
                easy=pygame.image.load("data/images/Difficulty_Easy.png")
                screen.blit(easy,(802,200))
            else:
                easy=pygame.image.load("data/images/Difficulty_Easy_No.png")
                screen.blit(easy,(802,200))
            if x>784 and y >263 and x<912 and y<300: #mouse over normal, change pic
                easy=pygame.image.load("data/images/Difficulty_Normal.png")
                screen.blit(easy,(784,263))
            else:
                easy=pygame.image.load("data/images/Difficulty_Normal_No.png")
                screen.blit(easy,(784,263))
            if x>762 and y >335 and x<942 and y<370: #mouse over hard, change pic
                easy=pygame.image.load("data/images/Difficulty_Ridiculous.png")
                screen.blit(easy,(762,335))
            else:
                easy=pygame.image.load("data/images/Difficulty_Ridiculous_No.png")
                screen.blit(easy,(762,335))
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
