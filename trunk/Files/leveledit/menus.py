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
        towerbutton((self.x+2*32, 1*32), [0,'u'])
        towerbutton((self.x+3*32, 1*32), [0,'d'])
        towerbutton((self.x+4*32, 1*32), [0,'l'])
        towerbutton((self.x+5*32, 1*32), [0,'r'])
        towerbutton((self.x+6*32, 1*32), [0,'g'])
        
        towerbutton((self.x+1*32, 2*32), [0,'h'])
        towerbutton((self.x+2*32, 2*32), [0,'a'])
        towerbutton((self.x+3*32, 2*32), [0,'b'])
        towerbutton((self.x+4*32, 2*32), [0,'c'])
        towerbutton((self.x+5*32, 2*32), [0,'e'])
        
        towerbutton((self.x+1*32, 3*32), [1,'W'])
        towerbutton((self.x+2*32, 3*32), [1,'A'])
        towerbutton((self.x+3*32, 3*32), [1,'B'])
        towerbutton((self.x+4*32, 3*32), [1,'C'])
        
        towerbutton((self.x+1*32, 4*32), [2,'D'])
        towerbutton((self.x+2*32, 4*32), [2,'S'])
        
        towerbutton((self.x+1*32, 5*32), [3,'W'])
        towerbutton((self.x+2*32, 5*32), [3,'A'])
        towerbutton((self.x+3*32, 5*32), [3,'B'])
        towerbutton((self.x+4*32, 5*32), [3,'C'])
        
        towerbutton((self.x+1*32, 6*32), [4,'D'])
        towerbutton((self.x+2*32, 6*32), [4,'S'])
        
        towerbutton((self.x+1*32, 8*32), [5,'0'])
        towerbutton((self.x+2*32, 8*32), [5,'1'])
        towerbutton((self.x+3*32, 8*32), [5,'2'])
        towerbutton((self.x+4*32, 8*32), [5,'3'])
        
        towerbutton((self.x+1*32, 9*32), [8,'A'])
        towerbutton((self.x+2*32, 9*32), [8,'B'])
        towerbutton((self.x+3*32, 9*32), [8,'C'])
        towerbutton((self.x+4*32, 9*32), [8,'D'])
        towerbutton((self.x+5*32, 9*32), [8,'E'])
        towerbutton((self.x+6*32, 9*32), [8,'F'])
        towerbutton((self.x+7*32, 9*32), [8,'G'])
        towerbutton((self.x+8*32, 9*32), [8,'H'])
        
        towerbutton((self.x+1*32, 10*32), [7,'0'])
        towerbutton((self.x+2*32, 10*32), [7,'1'])
        towerbutton((self.x+3*32, 10*32), [7,'2'])
        towerbutton((self.x+4*32, 10*32), [7,'3'])
        
        towerbutton((self.x+1*32, 11*32), [10,'A'])
        towerbutton((self.x+2*32, 11*32), [10,'B'])
        towerbutton((self.x+3*32, 11*32), [10,'C'])
        towerbutton((self.x+4*32, 11*32), [10,'D'])
        towerbutton((self.x+5*32, 11*32), [10,'E'])
        towerbutton((self.x+6*32, 11*32), [10,'F'])
        towerbutton((self.x+7*32, 11*32), [10,'G'])
        towerbutton((self.x+8*32, 11*32), [10,'H'])
        
        towerbutton((self.x+1*32, 13*32), [12,'1'])
        towerbutton((self.x+2*32, 13*32), [12,'2'])
        towerbutton((self.x+3*32, 13*32), [12,'3'])
        towerbutton((self.x+4*32, 13*32), [12,'4'])
        
        towerbutton((self.x+1*32, 15*32), [14,'P'])
        towerbutton((self.x+2*32, 15*32), [14,'G'])
        towerbutton((self.x+3*32, 15*32), [14,'Q'])
        towerbutton((self.x+4*32, 15*32), [14,'H'])
        
        towerbutton((self.x+1*32, 16*32), [13,'0'])
        towerbutton((self.x+2*32, 16*32), [13,'1'])
        towerbutton((self.x+3*32, 16*32), [13,'2'])
        towerbutton((self.x+4*32, 16*32), [13,'3'])
        
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
        self.image=pygame.image.load( "./data/images/%d%s%s" %( type[0] , type[1] , ".png") )
        
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