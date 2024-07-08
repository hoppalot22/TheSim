import pygame
import numpy as np
import Colors
import GameTools
import math
import os
import Sprite
from GameTools import Vector2, Vector3

class SpriteEditor:
    colors = Colors.THECOLORS 
    def __init__(self, w = 1280, h = 720):

        self.running = True
        
        self.position = Vector2(0,0)

        self.w, self.h = w, h
        self.centerOffset = Vector2(int(self.w/2), int(self.h/2))        
        self.screen = pygame.display.set_mode((w,h))
        
        self.selected = []
        self.selectedPixels = []
        self.children = []

        self.pixelMap = PixelMap(self, Vector2(16,16), Vector2(h,h))
        self.previewWindow = EditorObject(self, position = Vector2(720, 720-240), resolution = Vector2(240,240))
        self.previewWindow.colour = (255,255,255)
        self.previewWindow.UpdateDisplay = lambda: None     
        self.buttons = self.MakeInitialButtons()
        self.palette = ColourPalette(self, resolution = Vector2(250, 400))       
        
        self.UpdateScreen()   
    
    def MakeInitialButtons(self):
        exportSpriteLambda = lambda x :self.previewWindow.MakeDisplay(pygame.transform.scale(Button.ExportSprite(x,self.pixelMap).img, [*Vector2(240,240)]))
        makeNamedSectionLambda = lambda x: Button.MakeNamedSection(x,self.selected)
        buttons = [Button(self, Vector2(self.w-300, self.h-60), Vector2(200, 60), exportSpriteLambda, text = "Export Sprite"), Button(self, Vector2(self.w-300, self.h-120),Vector2(200, 60), makeNamedSectionLambda, text = "Make Named Section")]
        return buttons
    
    def Update(self):
        os.system("cls")
        t = dict()
        print(dir(t))
        for child in self.children:
            for subChild in child.GetChildren():
                k = subChild.__class__.__name__
                if k in t.keys():
                    t[k] += 1
                else:
                    t[k] = 1
        self.HandleEvents()
        print(t)        
        
    def UpdateScreen(self):
        self.Render()
    
    def Render(self):
        self.screen.fill("grey")
        for child in self.children:
            if not (child is self.palette and self.palette.hidden):
                self.screen.blit(child.GetDisplay(), [*child.position])                     
        pygame.display.flip()      
      
    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return           
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.HandlePrimaryDown(event)                
                if event.button == 2:
                    self.HandleMiddleDown(event)
                if event.button == 3:
                    self.HandleSecondaryDown(event)
            if event.type == pygame.MOUSEMOTION:
                self.MotionHandler(event)            
        self.UpdateScreen()        

    def HandlePrimaryDown(self, event): 
        self.Select(self, event)

    def HandleMiddleDown(self, event):
        self.UnSelectAll()
    
    def HandleSecondaryDown(self, event):
        self.TogglePalette(Vector2(*event.pos))
    
    def MotionHandler(self,event):
        if pygame.mouse.get_pressed()[0]:
            self.Select(self,event)      
     
    def Select(self, top, event):
        for child in reversed(top.children):
            bounds = child.GetBounds()
            if (bounds[0].x < event.pos[0] < bounds[1].x) and (bounds[0].y < event.pos[1] < bounds[1].y):
                return self.Select(child, event)
        #print(top)
        
        if isinstance(top, Pixel):
            if not(event.type == pygame.MOUSEMOTION):
                if top in self.selected:
                    self.UnSelect(top)
                else:
                    self.selected.append(top)
                    self.selectedPixels.append(top)
                    top.highLighted = True                    
            else:
                if not(top in self.selected):
                    self.selected.append(top)
                    self.selectedPixels.append(top)
                    top.highLighted = True               
   
        if isinstance(top, ColourBar):
            top.Selected(top.resolution[1] - event.pos[1] + top.AbsPosition()[1])
        
        if any([top == x for x in self.palette.tileList]):
            self.palette.colour = top.colour
            self.ChangePixelColours()
        
        if top is self.palette.colourPreview:
            self.ChangePixelColours()
            
        if isinstance(top, Button):
            top.Clicked()                  
        return
            
            
    def ChangePixelColours(self):
        for pixel in self.selectedPixels:
            pixel.ChangeColour(self.palette.colour)

    def UnSelect(self, child):
        child.highLighted = False
        self.selected.remove(child)
        self.selectedPixels.remove(child)
    
    def UnSelectAll(self):
        for child in self.selected:
            child.highLighted = False
        self.selected = []
        self.selectedPixels = []
        

    def TogglePalette(self, position):
        if self.palette.hidden:
            self.palette.extraTiles = self.GetColours()
            self.palette.hidden = False
            self.palette.position = position            
            self.children.append(self.palette)
        else:
            self.palette.hidden = True
            self.children.remove(self.palette)        
    
    def GetColours(self):
        colours = []
        for col in self.pixelMap.map:
            for pixel in col:
                for colour in colours:
                    if pixel.colour == colour:
                        break
                else:
                    colours.append(pixel.colour)
        return colours   

class EditorObject:
    
    def __init__(self, parent, position = Vector2(0,0), resolution = Vector2(50,50)):
        self.parent = parent
        parent.children.append(self)
        self.position = position
        self.resolution = resolution
        self.colour = (0,0,0,0)
        self.display = pygame.Surface([*self.resolution])      
        self.highLighted = False
        self.children = []
    
    def MakeDisplay(self, surf):
        self.display = surf
    
    def UpdateDisplay(self):
        disp = pygame.Surface([*self.resolution])
        disp.fill(self.colour)
        self.display = disp
        
    def GetDisplay(self):
        self.UpdateDisplay()
        disp = self.display.copy()
        for child in self.children:
            disp.blit(child.GetDisplay(), [*(child.position)])
        if self.highLighted:
            disp.blit(self.HighLight(), [*Vector2(0,0)])
        return disp
    
    def HighLight(self, tk = 2, colour = [255,0,0]):
        w, h = self.resolution
        highLightColour = self.display.copy().convert_alpha()
        highLightColour.fill(colour)
        highLightArray = pygame.PixelArray(highLightColour)
        highLightArray[tk:w-tk, tk: h-tk] = (0,0,0,0)
        highLightSurf = highLightArray.make_surface()
        return highLightSurf        
    
    def AbsPosition(self):
        pos = self.position
        if isinstance(self.parent, SpriteEditor):
            return pos
        else:
            result = pos + self.parent.AbsPosition()
            return result
            
    
    def GetBounds(self):        
        resolution = Vector2(*self.resolution)
        pos = Vector2(*self.AbsPosition())
        return [Vector2(int(pos.x), int(pos.y)) , Vector2(int(pos.x) + resolution.x, int(pos.y) + resolution.y)]
        
    def GetChildren(self):
        result = [self]
        for child in self.children:
            subChildren = child.GetChildren()
            if subChildren is not None:
                result.extend(subChildren)
        return result
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class ColourPalette(EditorObject):    
    def __init__(self, parent, position = Vector2(0,0), resolution = Vector2(10,10)):
        super().__init__(parent, resolution = resolution)
        self.hidden = True
        self.colour = [255,255,255,255]
        self.gap = 4
        self.wBar = int(resolution[0]/8-self.gap)
        self.halfRes = int(self.resolution[0]/2)
        self.bars = []
        for i, colour in enumerate(self.colour): 
            bar = ColourBar(self, Vector2(self.halfRes + (self.wBar+self.gap)*i,10), i, resolution = Vector2(self.wBar, 255))
        self.colourPreview = EditorObject(self, Vector2(self.halfRes, 255 + 10 + self.gap), Vector2(self.halfRes - self.gap, 60))
        self.commonColours = [(0,0,0,255),(255,255,255,255), (100,100,100,100),(255,0,0,255),(0,255,0,255),(0,0,255,255),(255,255,0,255),(0,255,255,255),(255,0,255,255),(160,32,255,255),(160,128,96,255),(255,96,208,255),(96,255,128,255),(204,102,0,255),(0,204,204,255),(153,153,0,255),(0,0,102,255),(0,102,0,255)]
        self.extraTiles = []
        self.tileList = []        
        self.UpdateDisplay()
     
    def UpdateDisplay(self): 
        surf = pygame.Surface([*self.resolution], pygame.SRCALPHA, 32)
        surf.fill((0,0,0,255))
        surf.fill("grey", [[*Vector2(1,1)], [*(self.resolution - Vector2(2,2))]])
        self.colour = [x.intensity for x in self.children if isinstance(x, ColourBar)]
        self.colourPreview.colour = self.colour
        self.colourPreview.UpdateDisplay()
        for child in self.children:
            child.highLighted = False
        self.UpdateTileList()    
        self.display = surf
    
    def UpdateTileList(self):        
        
        for i, colour in enumerate(self.extraTiles):
            if not(colour in [tile.colour for tile in self.tileList]):                
                spacing = int((self.halfRes - self.gap)/4 - self.gap)
                tile = EditorObject(self, Vector2(10 + i%4*spacing,10 + math.floor(i/4)*spacing), Vector2(spacing-self.gap, spacing - self.gap))
                tile.colour = colour
                self.tileList.append(tile)
                tile.UpdateDisplay()      
            
        for i, colour in enumerate(self.commonColours):
            if not(colour in [tile.colour for tile in self.tileList]):
                spacing = int((self.halfRes - self.gap)/4 - self.gap)
                tile = EditorObject(self, Vector2(10 + i%9*spacing, self.resolution[1] - self.gap - spacing - self.gap - math.floor(i/9)*spacing), Vector2(spacing-self.gap, spacing - self.gap))
                tile.colour = colour
                self.tileList.append(tile)
                tile.UpdateDisplay()

    
class ColourBar(EditorObject):
    
    def __init__(self, parent, position, colour, resolution = Vector2(32,255)):
        super().__init__(parent, position, resolution)
        self.intensity = 255
        self.colour = colour # Integer value (0,1,2,3) ---> (R,G,B,A)
        self.UpdateDisplay()   
    
    def UpdateDisplay(self):    
        gradMat = np.transpose(np.matmul(np.diag(np.linspace(self.resolution[1], 0 ,num = self.resolution[1])), np.ones([self.resolution[1],self.resolution[0]])))
        fullColour = np.zeros((self.resolution[0],self.resolution[1], 3))
        for RGB in range(3):
            if RGB == self.colour:
                fullColour[:,:,RGB] = gradMat
            else:
                fullColour[:,:,RGB] = self.parent.colour[RGB] * np.ones([self.resolution[0],self.resolution[1]])
        
        self.display = pygame.surfarray.make_surface(fullColour)
        
    def Selected(self, intensity):
        self.intensity = intensity
    
class Pixel(EditorObject):
    def __init__(self, parent, position, resolution = None, colour = (255,255,255,255), coords = None):
        super().__init__(parent, position = position, resolution = resolution)           
        self.colour = colour
        self.coords = coords
        self.ChangeColour(colour)
        

    def ChangeColour(self, colour):
        self.colour = colour
        self.UpdateDisplay()
    
    def UpdateDisplay(self):
        surf = pygame.Surface([*self.resolution])
        surf.fill("black")
        pixArr = pygame.PixelArray(surf)
        pixArr[1:self.resolution[0]-1,1:self.resolution[1]-1] = tuple(self.colour)
        newSurf = pixArr.make_surface()
        self.display = newSurf

class PixelMap(EditorObject):    
    def __init__(self, parent, size, resolution):
        super().__init__(parent, resolution = resolution)
        # size is pixels in map, resoultion is on screen
        self.resolution = resolution
        self.size = size
        self.map = self.BuildNewMap(size)
        self.zoom = 1
        self.UpdateDisplay()
    
    def UpdateDisplay(self):
        blankSurf = pygame.Surface([*self.resolution])
        blankSurf.fill((100,100,100))
        pixArr = pygame.PixelArray(blankSurf)
        pixArr[::2,:] = (120,120,120)
        surf = pixArr.make_surface()
        self.display = surf
    
    def BuildNewMap(self, size):
        newMap = [[(Pixel(self, position = Vector2(i*int(self.resolution[0]/size[0]),j*int(self.resolution[1]/size[1])), resolution = (int(self.resolution[0]/size[0]), int(self.resolution[0]/size[0])), coords = [i,j])) for j in range(size[1])]for i in range(size[0])]
        return newMap

    
    def ChangeMapSize(self, newSize):
        oldMap = self.map
        oldMapSize = self.size
        map = self.BuildNewMap(newSize)
        for col in range(oldMapSize[0]):
            for row in range(oldMapSize[1]):
                map[col][row] = oldMap[col][row]
        self.map = map

class Button(EditorObject):
    
    def __init__(self, parent, position, resolution, command, backGround = (60,60,60), text = "Dummy", textColour = (0,0,0)):
        super().__init__(parent, position = position, resolution = resolution)
        self.command = command
        self.backGround = backGround
        self.bounds = self.GetBounds()
        self.text = text
        self.textSize = 24
        self.textColour = textColour
        self.namedSections = []        
        self.UpdateDisplay()
    
    def UpdateDisplay(self):
        surf = pygame.Surface([*self.resolution])
        surf.fill("black")
        surf.fill(self.backGround, rect = [[*Vector2(1,1)], [*(self.resolution - Vector2(2,2))]])
        font = pygame.font.SysFont(None, self.textSize)
        fontSize = Vector2(*font.size(self.text))
        surf.blit(font.render(self.text, True, (0,0,0)), [*(self.resolution/2 - fontSize/2)])
        self.display = surf
    
    def Clicked(self):
        self.command(self)      
        
    def ExportSprite(self, pixelMap):
        map = pixelMap.map
        spriteArray = np.zeros((len(map), len(map[0]), 3))
        for i, col in enumerate(map):
            for j, pixel in enumerate(col):
                spriteArray[i,j,:] = pixel.colour[0:3]
        img = pygame.surfarray.make_surface(spriteArray).convert_alpha()
        sprite = Sprite.Sprite(img = img)
        for section in self.namedSections:
            sprite.namedSections.append(section)
        return sprite
        
    def MakeNamedSection(self, selected):
        coords = []
        colour = selected[0].colou
        for pixel in selected:
            coords.append(pixel.coords)
        return Sprite.NamedSection(self.name, coords, colour = colour)        
        

def Main():
    pygame.init()   
    clock = pygame.time.Clock()    
    editor = SpriteEditor()
    running = True

    while(running):
        
        if editor.running:        
            editor.Update()        
            clock.tick(30)
        else:
            pygame.quit()
            running = False
        
if __name__ == "__main__":
    Main()