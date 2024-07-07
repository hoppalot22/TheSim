import pygame
import numpy as np
import Colors
import GameTools
import math
import os
from GameTools import Vector2, Vector3

class SpriteEditor:
    
    def __init__(self, w = 1280, h = 720):

        self.w, self.h = w, h            
        self.screen = pygame.display.set_mode((w,h))
        self.running = True
        
        self.editorObjects = []
        self.topEditorObjects = []
        self.selectedEditorObjects = []
        self.highLightSurf = None
        self.selectedPixels = []
        self.coloursInMap = []
        
        self.centerOffset = Vector2(int(self.w/2), int(self.h/2))
        self.pixelMap = self.AddEditorObject(PixelMap(Vector2(16,16), Vector2(h,h)))
        self.colourPalette = ColourPalette(position = Vector2(0,0), resolution = Vector2(250, 400))
        
        self.UpdateScreen()

        colors = Colors.THECOLORS     
    
    def Update(self):
        
        self.HandleEvents()
        
        
    def UpdateScreen(self):
        self.FillScreen()
        #print(self.pixelMap.map[0][0].colour)
        #self.PrerenderTasks()
        
        self.Render()
        

    def FillScreen(self):
        self.screen.fill("grey")
    

    def PrerenderTasks(self):
        pass
        
    
    def Render(self):
        #print(self.topEditorObjects)
        for editorObject in self.topEditorObjects:
            #print (editorObject)
            self.screen.blit(editorObject.GetDisplay(), [*editorObject.position])              
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
                os.system('cls')
                if event.button == 1:
                    self.HandlePrimaryDown(event)
                if event.button == 3:
                    self.HandleSecondaryDown(event)
                #self.UpdateScreen()
            if event.type == pygame.MOUSEMOTION:
                self.MotionHandler(event)            
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        self.UpdateScreen()
        

    def HandlePrimaryDown(self, event): 
        #print(self.editorObjects)
        for editorObject in reversed(self.editorObjects):
            bounds = editorObject.GetBounds()
            #print(editorObject, bounds, event.pos)
            if (bounds[0].x < event.pos[0] < bounds[1].x) and (bounds[0].y < event.pos[1] < bounds[1].y):
                relPos = Vector2(event.pos[0] - bounds[0].x, event.pos[1] - bounds[0].y)
                self.Select(editorObject, relPos)
                break
        else:
            self.UnSelectAll()
        
     
    def HandlePrimaryDoubleDown(self, event):
        print("Double Click")
        #self.TileEditorObjects()
    
    
    def HandlePrimaryUp(self, event):
        pass
        
    
    def HandleSecondaryDown(self, event):
        self.TogglePalette(Vector2(*event.pos))
    
    def MotionHandler(self,event):
        if pygame.mouse.get_pressed()[0]:
            for editorObject in reversed(self.editorObjects):
                bounds = editorObject.GetBounds()
                if (bounds[0].x < event.pos[0] < bounds[1].x) and (bounds[0].y < event.pos[1] < bounds[1].y) and (editorObject not in self.selectedEditorObjects):
                    relPos = None
                    self.Select(editorObject, relPos)
                    #self.UpdateScreen()
                    break
        
     
    def Select(self, editorObject, relPos):
        #print(f"Selected {editorObject}")
        self.selectedEditorObjects.append(editorObject)
        #print(editorObject)
        if isinstance(editorObject, Pixel):
            #print(editorObject, editorObject.colour)
            if editorObject.highLighted:
                self.UnSelect(editorObject)
            else:
                self.selectedPixels.append(editorObject)
                editorObject.highLighted = True
        if relPos is not None:        
            if isinstance(editorObject, ColourBar):
                editorObject.intensity = editorObject.resolution[1] - relPos[1]
                self.colourPalette.UpdateDisplay()
            
            if editorObject in self.colourPalette.tileList:
                self.colourPalette.colour = editorObject.colour
                self.ChangePixelColours()
            
            if editorObject is self.colourPalette.colourPreview:
                self.ChangePixelColours()
            
    def ChangePixelColours(self):
        for pixel in self.selectedPixels:
            pixel.ChangeColour(self.colourPalette.colour)

    def UnSelect(self, editorObject):
        editorObject.highLighted = False
        self.selectedEditorObjects.remove(editorObject)
        self.selectedPixels.remove(editorObject)
    
    def UnSelectAll(self):
        print("Unselect")
        for editorObject in self.selectedEditorObjects:
            editorObject.highLighted = False
        del(self.selectedEditorObjects)
        del(self.selectedPixels)
        self.selectedEditorObjects = []
        self.selectedPixels = []
        

    def TogglePalette(self, position):
        if self.colourPalette.hidden:
            self.GetColours()
            self.colourPalette.hidden = False
            self.colourPalette.position = position
            self.colourPalette.UpdateChildPositions()
            self.AddEditorObject(self.colourPalette)
        else:
            self.colourPalette.hidden = True
            self.RemoveEditorObject(self.colourPalette)
        

    
    
    def GetColours(self):
        self.coloursInMap = []
        
        for col in self.pixelMap.map:
            for pixel in col:

                for colour in self.coloursInMap:
                    if all(pixel.colour[x] == colour[x] for x in range(len(colour))):
                        #print(pixel.colour, colour)
                        break
                else:
                    self.coloursInMap.append(pixel.colour)
        self.colourPalette.usedColours = self.coloursInMap
        self.colourPalette.UpdateUsedColours()
    
    def Move(self, editorObject, distVec):

        if editorObject is None:
            return
            
        else:
            editorObject.position += Vector2(distVec[0], distVec[1])
        
        bounds = editorObject.GetBounds()
        
        if bounds[0] < 0:
            editorObject.position.x = 0
            
        if bounds[1] < 0:
            editorObject.position.y = 0          
            
        if bounds[2] > self.w:
            editorObject.position.x = self.w-editorObject.resolution[0]
            
        if bounds[3] > self.h:
            editorObject.position.y = self.h-editorObject.resolution[1]

        editorObject.bounds = bounds

    def RemoveEditorObject(self, editorObject):
        for top in self.topEditorObjects:
            if editorObject == top:
                self.topEditorObjects.remove(editorObject)
        for _editorObject in self.editorObjects:
            if editorObject == _editorObject:
                for subObject in editorObject.GetChildEditorObjects():                    
                    self.editorObjects.remove(subObject)
    
    def AddEditorObject(self, editorObject):
        #print("call")
        editorObject.UpdateDisplay()
        #print(editorObject.GetChildEditorObjects())
        self.topEditorObjects.append(editorObject)
        self.editorObjects.extend(editorObject.GetChildEditorObjects())
        return editorObject

class EditorObject:
    
    def __init__(self, position = Vector2(0,0), resolution = Vector2(50,50)):
        self.position = position
        self.resolution = resolution
        self.colour = (0,0,0,0)
        self.display = pygame.Surface([*self.resolution])      
        self.labels = []
        self.highLighted = False
        self.childEditorObjects = []
    
    def UpdateDisplay(self, colour = (0,0,0,0)):
        print(f"called on {self}")
        self.colour = colour
        defaultDisp = pygame.Surface([*self.resolution])
        defaultDisp.fill(colour)
        self.display = defaultDisp
        
    def GetDisplay(self):
        disp = self.display.copy()
        for child in self.childEditorObjects:
            disp.blit(child.GetDisplay(), [*(child.position - self.position)])
        if self.highLighted:
            disp.blit(self.HighLight(), [*Vector2(0,0)])
        return disp
    
    def HighLight(self, tk = 2, colour = [255,0,0]):
        #print(f"Highlighting {self} at {self.GetBounds()}")

        w, h = self.resolution
        highLightColour = self.display.copy().convert_alpha()
        highLightColour.fill(colour)
        highLightArray = pygame.PixelArray(highLightColour)
        highLightArray[tk:w-tk, tk: h-tk] = (0,0,0,0)
        highLightSurf = highLightArray.make_surface()
        return highLightSurf
        
    
    def GetBounds(self):
        resolution = self.resolution
        return [Vector2(int(self.position.x), int(self.position.y)) , Vector2(int(self.position.x) + resolution[0], int(self.position.y) + resolution[1])]
        
    def AddLabel(self, label):
        label.MakeText()
        self.labels.append(label)
    
    def AddChildEditorObject(self, child):
        self.childEditorObjects.append(child)
        child.relPosition = child.position
        child.position += self.position
        return child
        
    def RemoveChildEditorObject(self, child):
        self.childEditorObjects.remove(child)
        
    def GetChildEditorObjects(self):
        result = [self]
        for child in self.childEditorObjects:
            subEditorObjects = child.GetChildEditorObjects()
            if subEditorObjects is not None:
                result.extend(subEditorObjects)
        return result
    
    def UpdateChildPositions(self):
        for child in self.childEditorObjects:
            child.position = self.position + child.relPosition

    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class ColourPalette(EditorObject):
    
    def __init__(self, position = Vector2(0,0), resolution = None):
        super().__init__(position, resolution)
        self.hidden = True
        self.colour = [255,255,255,255]
        self.R, self.G, self.B, self.A = self.colour
        self.colourBarGap = 4
        self.colourBarSize = Vector2(int(resolution[0]/8-self.colourBarGap),255)
        self.halfRes = Vector2(int(self.resolution[0]/2),0)
        for i, colour in enumerate(self.colour):            
            self.AddColourBar(Vector2(int(self.colourBarSize[0]+self.colourBarGap)*i,10) + self.halfRes, i)
        self.colourPreview = self.AddChildEditorObject(EditorObject(Vector2(self.halfRes[0], self.colourBarSize[1] + 10 + self.colourBarGap), Vector2(self.halfRes[0] - self.colourBarGap, 60)))
        self.commonColours = [(0,0,0,255),(255,255,255,255), (100,100,100,100),(255,0,0,255),(0,255,0,255),(0,0,255,255),(255,255,0,255),(0,255,255,255),(255,0,255,255),(160,32,255,255),(160,128,96,255),(255,96,208,255),(96,255,128,255),(204,102,0,255),(0,204,204,255),(153,153,0,255),(0,0,102,255),(0,102,0,255)]
        self.usedColours = []
        self.tileList = []
        
        self.display = self.UpdateDisplay()
     
    def UpdateDisplay(self):
    
        surf = pygame.Surface([*self.resolution])
        surf.fill("black")
        surf.fill("grey", [[*Vector2(1,1)], [*(self.resolution - Vector2(2,2))]])
        self.colour = self.GetBarInfo()
        self.UpdateBars()
        self.colourPreview.UpdateDisplay(self.colour)
        for child in self.childEditorObjects:
            child.highLighted = False
       
        return surf
     
    def AddColourBar(self, position, colour):
        self.AddChildEditorObject(ColourBar(position, colour, resolution = self.colourBarSize))
    
    def GetBarInfo(self):
        colour = [0,0,0,0]
        for bar in self.childEditorObjects:
            if isinstance(bar, ColourBar):
                colour[bar.colour] = bar.intensity
                pass
        return colour
        
    def UpdateBars(self):
        for bar in self.childEditorObjects:
            if isinstance(bar, ColourBar):
                bar.UpdateDisplay(self.colour)
    
    def UpdateUsedColours(self):        
        for tile in self.tileList:
            if tile in self.childEditorObjects:
                self.RemoveChildEditorObject(tile)
        self.tileList = []
                
        for i, colour in enumerate(self.usedColours):
            spacing = int((self.halfRes[0] - self.colourBarGap)/4 - self.colourBarGap)
            tile = EditorObject(Vector2(10 + i%4*spacing,10 + math.floor(i/4)*spacing), Vector2(spacing-self.colourBarGap, spacing - self.colourBarGap))
            tile.UpdateDisplay(colour)
            self.AddChildEditorObject(tile)
            self.tileList.append(tile)        
            
        for i, colour in enumerate(self.commonColours):
            spacing = int((self.halfRes[0] - self.colourBarGap)/4 - self.colourBarGap)
            tile = EditorObject(Vector2(10 + i%9*spacing, self.resolution[1] - self.colourBarGap - spacing - self.colourBarGap - math.floor(i/9)*spacing), Vector2(spacing-self.colourBarGap, spacing - self.colourBarGap))
            tile.UpdateDisplay(colour)
            self.AddChildEditorObject(tile)
            self.tileList.append(tile)

    
class ColourBar(EditorObject):
    
    def __init__(self, position, colour, resolution = Vector2(32,255)):
        super().__init__(position, resolution)
        self.intensity = 255
        self.colour = colour # Integer value (0,1,2,3) ---> (R,G,B,A)
        self.UpdateDisplay([0,0,0,0])   
    
    def UpdateDisplay(self, colour):
    
        gradMat = np.transpose(np.matmul(np.diag(np.linspace(self.resolution[1], 0 ,num = self.resolution[1])), np.ones([self.resolution[1],self.resolution[0]])))
        fullColour = np.zeros((self.resolution[0],self.resolution[1], 3))
        for RGB in range(3):
            if RGB == self.colour:
                fullColour[:,:,RGB] = gradMat
            else:
                fullColour[:,:,RGB] = colour[RGB] * np.ones([self.resolution[0],self.resolution[1]])
        
        self.display = pygame.surfarray.make_surface(fullColour)
    


    
class Pixel(EditorObject):
    def __init__(self, position, resolution = None, colour = (255,255,255,255), coords = None):
        super().__init__(position = position, resolution = resolution)           
        self.colour = colour
        self.coords = coords
        self.ChangeColour(colour)
    

    def ChangeColour(self, colour):
        self.colour = colour
        self.UpdateDisplay()
    
    def UpdateDisplay(self):
        #print("Called")
        surf = pygame.Surface([*self.resolution])
        surf.fill("black")
        pixArr = pygame.PixelArray(surf)
        #print(self.colour, ([self.colour[x] for x in range(3)]))
        #print(self, self.coords, self.colour)
        pixArr[1:self.resolution[0]-1,1:self.resolution[1]-1] = tuple(self.colour)
        newSurf = pixArr.make_surface()
        self.display = newSurf

class PixelMap(EditorObject):    
    def __init__(self, size, resolution):
        super().__init__(position = Vector2(0,0), resolution = resolution)
        # size is pixels in map, resoultion is on screen
        self.resolution = resolution
        self.size = size
        self.map = self.BuildNewMap(size)
        self.zoom = 1
        self.xPos, self.yPos = Vector2(0,0), Vector2(0,0)
        self.UpdateDisplay()
        
    
    # def UpdateDisplay(self):
        # blankSurf = self.MakeBackGround()
        # pos = Vector2(0,0)
        # for pixelCol in self.map:
            # for pixel in pixelCol:
                # blankSurf.blit(pixel.display, [*pos])
                # pos += Vector2(0,pixel.resolution[1])
            # pos = Vector2(pos.x+pixel.resolution[0],0)
        # self.display = blankSurf
        # self.baseDisplay = self.display
    
    def UpdateDisplay(self):
        blankSurf = pygame.Surface([*self.resolution])
        blankSurf.fill((100,100,100))
        pixArr = pygame.PixelArray(blankSurf)
        pixArr[::2,:] = (120,120,120)
        surf = pixArr.make_surface()
        self.display = surf
    
    def BuildNewMap(self, size):

        newMap = [[self.AddChildEditorObject(Pixel(position = Vector2(i*int(self.resolution[0]/size[0]),j*int(self.resolution[1]/size[1])), resolution = (int(self.resolution[0]/size[0]), int(self.resolution[0]/size[0])), coords = [i,j])) for j in range(size[1])]for i in range(size[0])]
        #print(newMap)
        return newMap

    
    def ChangeMapSize(self, newSize):
        oldMap = self.map
        oldMapSize = self.size
        map = self.BuildNewMap(newSize)
        for col in range(oldMapSize[0]):
            for row in range(oldMapSize[1]):
                map[col][row] = oldMap[col][row]
        self.map = map


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