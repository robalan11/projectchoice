import pygame
import DisasterEngine

class startscreen:
    def __init__(self, screen):
        self.bg=pygame.image.load('data/images/Game_with_Options.png')
        self.alive=True
        screen.fill((237, 237, 215))
        screen.blit(self.bg, (152,0))
        pygame.display.flip()
    def mouseclick(self, mousepos):
        if mousepos[0]>650+152 and mousepos[1]>190 and mousepos[0]<750+152 and mousepos[1]<240:
            self.alive=False
            return 0.5
        if mousepos[0]>620+152 and mousepos[1]>260 and mousepos[0]<780+152 and mousepos[1]<310:
            self.alive=False
            return 1.0
        if mousepos[0]>595+152 and mousepos[1]>325 and mousepos[0]<805+152 and mousepos[1]<380:
            self.alive=False
            return 2.0
class GUI:
    def __init__(self):
        self.x=896
        self.width=304
        self.towertype='None'
        self.towertext=None
        pygame.font.init()
        self.text=pygame.font.SysFont('Arial', 18, False, False)
        self.bigtext=pygame.font.SysFont('Arial Black', 30, False, False)
        #Create the towerbuttons
        towerbutton((self.x+1*32, 1*32), [0,'F'])
        towerbutton((self.x+1*32, 3*32), [1,'W'])
        towerbutton((self.x+2*32, 3*32), [1,'D'])
        towerbutton((self.x+1*32, 5*32), [2,'W'])
        towerbutton((self.x+2*32, 5*32), [2,'D'])
    def draw(self, screen):
        for button in towerbutton.towerbuttons:
            button.draw(screen, self.towertype)
    def getbuttoninfo(self):
        type=None
        for button in towerbutton.towerbuttons:
            if button.mouse_on():
                type=button.type
                if pygame.mouse.get_pressed()[0]:    
                    self.towertype=button.type
        return type
    def settower(self):
        for button in towerbutton.towerbuttons:
            if button.mouse_on():
                self.towertype=button.type
        return type
    def update(self,):
        self.towertext=self.getbuttoninfo()
        if self.towertext==None:
            self.towertext=self.towertype
        else:
            self.towertext=''
    def shutdown(self):
        pygame.font.quit()


class towerbutton(pygame.sprite.Sprite):
    towerbuttons=pygame.sprite.Group()
    greyedout=pygame.surface.Surface((64,64))
    greyedout.fill((100,100,100))
    greyedout.set_alpha(125)
    def __init__(self, pos, type):
        self.type=type
        self.pos=pos
        pygame.sprite.Sprite.__init__(self)
        #pygame.sprite.Sprite.__init__()
        if type==[2,'W']:
            self.image=pygame.image.load('data/images/BuildTop.png')
        elif type==[2,'D']:
            self.image=pygame.image.load('data/images/BuildDoorTop.png')
        elif type==[1,'D']:
            self.image=pygame.image.load('data/images/BuildDoorLeft.png')
        elif type==[1,'W']:
            self.image=pygame.image.load('data/images/BuildLeft.png')
        elif type==[0,'F']:
            self.image=pygame.image.load('data/images/Floor.png')
        towerbutton.towerbuttons.add(self)
        self.rect=pygame.rect.Rect(pos, (32,32))
    def mouse_on(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def draw(self, screen, towertype):
        if self.type==towertype:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 6)
        if self.mouse_on():
            # draw a highlight if the button is selected
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 6)
        screen.blit(self.image, self.pos)