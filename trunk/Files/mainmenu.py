from pandac.PandaModules import *
from direct.gui.DirectGui import *
import sys

class MainMenu(object):
    def __init__(self, engine):
        
        self.engine = engine
        
        self.background = self.createGuiLabel("Art/Menu/MenuTip.png", 800, 600, 0, 0)
        
        self.startButton = self.createGuiButton("Begin Game", -90, 250, 100, engine.initMainGame)
        self.instructionButton = self.createGuiButton("Instructions", -90, 300, 100, self.displayInstructions)
        self.quitButton = self.createGuiButton("Exit", -90, 350, 100, sys.exit)
        
    def __del__(self):
        self.background.destroy()
        self.startButton.destroy()
        self.instructionButton.destroy()
        self.quitButton.destroy()
        
    def createGuiButton(self, text, posX, posY, size, function):
        posX -= 400.0 - size / 2.0
        posY = 300.0 - size / 2.0 - posY
        posX /= 400.0
        posY /= 300.0
        guiObject = DirectButton(text = (text), scale = size / 1000.0, command = function, pos = Vec3(posX, 0.0, posY))
        
        return guiObject
        
    def createGuiLabel(self, image, sizeX, sizeY, posX, posY):
        posX -= 400.0 - sizeX / 2.0
        posY = 300.0 - sizeY / 2.0 - posY
        posX /= 400.0
        posY /= 300.0
        guiObject = DirectLabel()
        guiObject['image'] = image
        guiObject.setTransparency(1)
        guiObject['image_pos'] = (posX,0.0,posY)
        guiObject['image_scale'] = (sizeX / 600.0, 1.0, sizeY / 600.0)

        return guiObject
        
    def displayInstructions(self):
        self.background.destroy()
        self.startButton.destroy()
        self.instructionButton.destroy()
        self.quitButton.destroy()
        
        self.instructions = self.createGuiLabel("Art/Menu/Instructions.png", 800, 600, 0, 0)
        self.mainMenuButton = self.createGuiButton("Main Menu", 0, 525, 100, self.returnToMenu)
        
    def returnToMenu(self):
        self.instructions.destroy()
        self.mainMenuButton.destroy()
        self.__init__(self.engine)


class YouWin(object):
    def __init__(self):
        props.setCursorHidden(False)
        self.background = self.createGuiLabel("Art/Menu/YouWin.png", 800, 600, 0, 0)
        
        self.quitButton = self.createGuiButton("Exit", -90, 350, 100, sys.exit)
        
    def createGuiButton(self, text, posX, posY, size, function):
        posX -= 400.0 - size / 2.0
        posY = 300.0 - size / 2.0 - posY
        posX /= 400.0
        posY /= 300.0
        guiObject = DirectButton(text = (text), scale = size / 1000.0, command = function, pos = Vec3(posX, 0.0, posY))
        
        return guiObject
        
    def createGuiLabel(self, image, sizeX, sizeY, posX, posY):
        posX -= 400.0 - sizeX / 2.0
        posY = 300.0 - sizeY / 2.0 - posY
        posX /= 400.0
        posY /= 300.0
        guiObject = DirectLabel()
        guiObject['image'] = image
        guiObject.setTransparency(1)
        guiObject['image_pos'] = (posX,0.0,posY)
        guiObject['image_scale'] = (sizeX / 600.0, 1.0, sizeY / 600.0)

        return guiObject