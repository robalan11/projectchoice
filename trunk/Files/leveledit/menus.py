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
        
        towerbutton((self.x+1*32, 7*32), [6,'B'])
        towerbutton((self.x+2*32, 7*32), [6,'T'])
        towerbutton((self.x+3*32, 7*32), [6,'C'])
        towerbutton((self.x+4*32, 7*32), [6,'M'])
        towerbutton((self.x+5*32, 7*32), [6,'D'])
        towerbutton((self.x+6*32, 7*32), [6,'K'])
        towerbutton((self.x+7*32, 7*32), [6,'S'])
        towerbutton((self.x+8*32, 7*32), [6,'L'])
        
        towerbutton((self.x+1*32, 8*32), [5,'0'])
        towerbutton((self.x+2*32, 8*32), [5,'1'])
        towerbutton((self.x+3*32, 8*32), [5,'2'])
        towerbutton((self.x+4*32, 8*32), [5,'3'])
        towerbutton((self.x+5*32, 8*32), [8,'M'])
        towerbutton((self.x+6*32, 8*32), [8,'N'])
        towerbutton((self.x+7*32, 8*32), [8,'O'])
        towerbutton((self.x+8*32, 8*32), [8,'P'])
        
        towerbutton((self.x+1*32, 9*32), [8,'A'])
        towerbutton((self.x+2*32, 9*32), [8,'B'])
        towerbutton((self.x+3*32, 9*32), [8,'C'])
        towerbutton((self.x+4*32, 9*32), [8,'D'])
        towerbutton((self.x+5*32, 9*32), [8,'E'])
        towerbutton((self.x+6*32, 9*32), [8,'F'])
        towerbutton((self.x+7*32, 9*32), [8,'G'])
        towerbutton((self.x+8*32, 9*32), [8,'H'])
        
        towerbutton((self.x+1*32, 10*32), [8,'I'])
        towerbutton((self.x+2*32, 10*32), [8,'J'])
        towerbutton((self.x+3*32, 10*32), [8,'K'])
        towerbutton((self.x+4*32, 10*32), [8,'L'])
        towerbutton((self.x+5*32, 10*32), [7,'0'])
        towerbutton((self.x+6*32, 10*32), [7,'1'])
        towerbutton((self.x+7*32, 10*32), [7,'2'])
        towerbutton((self.x+8*32, 10*32), [7,'3'])
        
        
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
        towerbutton((self.x+5*32, 13*32), [12,'5'])
        towerbutton((self.x+6*32, 13*32), [12,'6'])
        towerbutton((self.x+7*32, 13*32), [12,'7'])
        towerbutton((self.x+8*32, 13*32), [12,'8'])
        
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
        if self.towertext!=None:
            i=0
            for line in self.towertext:
                screen.blit(self.text.render(line, True, (0,0,0)), (self.x+2, 350+i))
                i=i+self.text.get_linesize()+1
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
            self.towertext=="None?"
        elif(self.towertext==[0,'F']):
            self.towertext="ConcreteFloor"
        elif(self.towertext==[0,'u']):
            self.towertext="Stairs"
        elif(self.towertext==[0,'d']):
            self.towertext="Stairs"
        elif(self.towertext==[0,'l']):
            self.towertext="Stairs"
        elif(self.towertext==[0,'r']):
            self.towertext="Stairs"
        elif(self.towertext==[0,'g']):
            self.towertext="FloorTex2"
        
        elif(self.towertext==[0,'h']):
            self.towertext="FloorTex3"
        elif(self.towertext==[0,'a']):
            self.towertext="StairsDown"
        elif(self.towertext==[0,'b']):
            self.towertext="StairsDown"
        elif(self.towertext==[0,'c']):
            self.towertext="StairsDown"
        elif(self.towertext==[0,'e']):
            self.towertext="StairsDown"
        
        elif(self.towertext==[1,'W']):
            self.towertext="DefaultWallTex"
        elif(self.towertext==[1,'A']):
            self.towertext="WallTex2"
        elif(self.towertext==[1,'B']):
            self.towertext="WallTex3"
        elif(self.towertext==[1,'C']):
            self.towertext="WallTex4"
        
        elif(self.towertext==[2,'D']):
            self.towertext="Door"
        elif(self.towertext==[2,'S']):
            self.towertext="Sliding Door"
        
        elif(self.towertext==[3,'W']):
            self.towertext="DefaultWallTex"
        elif(self.towertext==[3,'A']):
            self.towertext="WallTex2"
        elif(self.towertext==[3,'B']):
            self.towertext="WallTex3"
        elif(self.towertext==[3,'C']):
            self.towertext="WallTex4"
        
        elif(self.towertext==[4,'D']):
            self.towertext="Door"
        elif(self.towertext==[4,'S']):
            self.towertext="SlidingDoor"
        
        elif(self.towertext==[5,'0']):
            self.towertext="InteriorFace"
        elif(self.towertext==[5,'1']):
            self.towertext="InteriorFace"
        elif(self.towertext==[5,'2']):
            self.towertext="InteriorFace"
        elif(self.towertext==[5,'3']):
            self.towertext="InteriorFace"
            
        elif(self.towertext==[6,'B']):
            self.towertext="Barricade"
        elif(self.towertext==[6,'T']):
            self.towertext="Round Table"
        elif(self.towertext==[6,'C']):
            self.towertext="Wooden Chair"
        elif(self.towertext==[6,'M']):
            self.towertext="Metal Chair"
        elif(self.towertext==[6,'D']):
            self.towertext="Desks"
        elif(self.towertext==[6,'K']):
            self.towertext="Kitchen Console"
        elif(self.towertext==[6,'S']):
            self.towertext="Security Console"
        elif(self.towertext==[6,'L']):
            self.towertext="Bookshelf"
        
        elif(self.towertext==[8,'A']):
            self.towertext="PrisonMelee"
        elif(self.towertext==[8,'B']):
            self.towertext="PrisonPistol"
        elif(self.towertext==[8,'C']):
            self.towertext="PrisonShotgun"
        elif(self.towertext==[8,'D']):
            self.towertext="PrisonAutomatic"
        elif(self.towertext==[8,'E']):
            self.towertext="GuardMelee"
        elif(self.towertext==[8,'F']):
            self.towertext="GuardPistol"
        elif(self.towertext==[8,'G']):
            self.towertext="GuardShotgun"
        elif(self.towertext==[8,'H']):
            self.towertext="GuardAutomatic"
        elif(self.towertext==[8,'I']):
            self.towertext="BeefyPrisonMelee"
        elif(self.towertext==[8,'J']):
            self.towertext="BeefyPrisonPistol"
        elif(self.towertext==[8,'K']):
            self.towertext="BeefyPrisonShotgun"
        elif(self.towertext==[8,'L']):
            self.towertext="BeefyPrisonAutomatic"
        elif(self.towertext==[8,'M']):
            self.towertext="BeefyGuardMelee"
        elif(self.towertext==[8,'N']):
            self.towertext="BeefyGuardPistol"
        elif(self.towertext==[8,'O']):
            self.towertext="BeefyGuardShotgun"
        elif(self.towertext==[8,'P']):
            self.towertext="BeefyGuardAutomatic"
        
        elif(self.towertext==[7,'0']):
            self.towertext="EnemyFace"
        elif(self.towertext==[7,'1']):
            self.towertext="EnemyFace"
        elif(self.towertext==[7,'2']):
            self.towertext="EnemyFace"
        elif(self.towertext==[7,'3']):
            self.towertext="EnemyFace"
        
        elif(self.towertext==[10,'A']):
            self.towertext="SmallPistol"
        elif(self.towertext==[10,'B']):
            self.towertext="SmallShotgun"
        elif(self.towertext==[10,'C']):
            self.towertext="SmallAutomatic"
        elif(self.towertext==[10,'D']):
            self.towertext="Health"
        elif(self.towertext==[10,'E']):
            self.towertext="Armor"
        elif(self.towertext==[10,'F']):
            self.towertext="BigPistol"
        elif(self.towertext==[10,'G']):
            self.towertext="BigShotgun"
        elif(self.towertext==[10,'H']):
            self.towertext="BigAutomatic"
        
        elif(self.towertext==[12,'1']):
            self.towertext="Cinematic1"
        elif(self.towertext==[12,'2']):
            self.towertext="Cinematic2"
        elif(self.towertext==[12,'3']):
            self.towertext="Cinematic3"
        elif(self.towertext==[12,'4']):
            self.towertext="Cinematic4"
        elif(self.towertext==[12,'5']):
            self.towertext="Cinematic5"
        elif(self.towertext==[12,'6']):
            self.towertext="Cinematic6"
        elif(self.towertext==[12,'7']):
            self.towertext="Cinematic7"
        elif(self.towertext==[12,'8']):
            self.towertext="Cinematic8"
        
        elif(self.towertext==[14,'P']):
            self.towertext="PrisonEnter"
        elif(self.towertext==[14,'G']):
            self.towertext="GuardEnter"
        elif(self.towertext==[14,'Q']):
            self.towertext="PrisonExit"
        elif(self.towertext==[14,'H']):
            self.towertext="GuardExit"
        
        elif(self.towertext==[13,'0']):
            self.towertext="EntranceFace"
        elif(self.towertext==[13,'1']):
            self.towertext="EntranceFace"
        elif(self.towertext==[13,'2']):
            self.towertext="EntranceFace"
        elif(self.towertext==[13,'3']):
            self.towertext="EntranceFace"
        else:
            self.towertext="Unknown"
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