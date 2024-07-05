import pygame
import numpy as np
import math
import GameTools
from GameTools import Vector2, Vector3


class Renderer:
    
    def __init__(self):

        self.w, self.h = 1280, 720             
        self.screen = pygame.display.set_mode((self.w,self.h))
        self.gui = GUI()
        
        self.renderObjects = []
        self.dormantRenderObjects = []
        self.selectedRenderObject = None
        self.fullScreenObject = None
        self.highLightSurf = None
        
        self.centerOffset = Vector2(int(self.w/2), int(self.h/2))        
        self.drawables = []
    
    def Update(self):        

        self.FillScreen()
        self.PrerenderTasks()
        self.RenderRenderObjects()
        #self.RenderDrawables()
        self.RenderGUI()
        self.Flip()

    def FillScreen(self):
        self.screen.fill("grey")
    

    def PrerenderTasks(self):
        self.UpdateDisplays()
    
    def RenderRenderObjects(self):
        if self.fullScreenObject == None:
            for renderObject in self.renderObjects:
                disp = renderObject.display
                self.screen.blit(disp, (renderObject.rPosition.x, renderObject.rPosition.y))
        else:
            disp = self.fullScreenObject[0].display
            self.screen.blit(disp, (0, 0))

    def RenderDrawables(self):
    
        for drawable in self.drawables:
            drawable[0](self.screen, *drawable[1])     
    
    def RenderGUI(self):
        pass
    
        
    def Flip(self):        
        pygame.display.flip()
      

    def UpdateDisplays(self):
        for renderObject in self.renderObjects:
            renderObject.UpdateDisplay()
        if self.selectedRenderObject is not None:
            self.selectedRenderObject.display.blit(self.highLightSurf, (0,0))


    def HandlePrimaryDown(self, event):        
        for renderObject in self.renderObjects:
            bounds = renderObject.GetBounds()
            if (bounds[0] < event.pos[0] < bounds[2]) and (bounds[1] < event.pos[1] < bounds[3]):
                self.Select(renderObject)
                break
     
    def HandlePrimaryDoubleDown(self, event):
        print("Double Click")
        self.TileRenderObjects()
    
    
    def HandlePrimaryUp(self, event):
        pass
        
    
    def HandleSecondaryDown(self, event):
        if self.selectedRenderObject is not None:
            self.ToggleFullScreen(self.selectedRenderObject)
    
    def MotionHandler(self,event):
        if pygame.mouse.get_pressed()[0]:
            if (self.selectedRenderObject is not None):
                bounds = self.selectedRenderObject.GetBounds()
                if(bounds[0] < event.pos[0] < bounds[2]) and (bounds[1] < event.pos[1] < bounds[3]):
                    self.Move(self.selectedRenderObject, event.rel)
        
     
    def Select(self, renderObject):
        #print(f"Selected {renderObject}")
        self.selectedRenderObject = renderObject
        self.HighLightSelected()
    
    def HighLightSelected(self):
        if (self.selectedRenderObject is not None):
            thickness = 4
            renderObject = self.selectedRenderObject
            w,h = renderObject.resolution
            #print(w,h)
            highLightColour = renderObject.display.copy()
            highLightColour.fill('red')
            highLightArray = pygame.PixelArray(highLightColour)
            highLightArray[thickness:w-thickness, thickness: h-thickness] = (0,0,0,0)
            self.highLightSurf = highLightArray.make_surface()
    
    def ToggleFullScreen(self, renderObject):        
        
        if self.fullScreenObject == None:        
            for _renderObject in self.renderObjects:
                if not(renderObject == _renderObject):
                    self.dormantRenderObjects.append(_renderObject)
            self.renderObjects = [renderObject]
            origRes = renderObject.resolution
            self.fullScreenObject = [renderObject, origRes]
            renderObject.resolution = [self.w, self.h]         
            
        else:
            self.fullScreenObject[0].resolution = self.fullScreenObject[1]
            self.fullScreenObject = None
            for _renderObject in self.dormantRenderObjects:
                self.AddRenderObject(_renderObject)
            self.dormantRenderObjects = []            
        renderObject.UpdateDisplay()
        self.HighLightSelected()
        

    def Move(self, renderObject, distVec):

        if renderObject is None:
            return
            
        else:
            renderObject.rPosition += Vector2(distVec[0], distVec[1])
        
        bounds = renderObject.GetBounds()
        
        if bounds[0] < 0:
            renderObject.rPosition.x = 0
            
        if bounds[1] < 0:
            renderObject.rPosition.y = 0          
            
        if bounds[2] > self.w:
            renderObject.rPosition.x = self.w-renderObject.resolution[0]
            
        if bounds[3] > self.h:
            renderObject.rPosition.y = self.h-renderObject.resolution[1]

        renderObject.bounds = bounds

    def PanSelectedCamera(self, key):
        if self.selectedRenderObject is not None:
            if key in [pygame.K_w, pygame.K_UP]:
                self.selectedRenderObject.Pan(0,1)        
            if key in [pygame.K_s, pygame.K_DOWN]:
                self.selectedRenderObject.Pan(0,-1)        
            if key in [pygame.K_a, pygame.K_LEFT]:
                self.selectedRenderObject.Pan(-1,0)        
            if key in [pygame.K_d, pygame.K_RIGHT]:
                self.selectedRenderObject.Pan(1,0)
        

    def ZoomSelectedCamera(self, amount):
        if self.selectedRenderObject is not None:
            if amount%2 == 0:
                self.selectedRenderObject.Zoom(-amount/2)
            else:
                self.selectedRenderObject.Zoom(amount/2)   

    
    def TileRenderObjects(self):
        currentPos = Vector2(0,0)
        sortedObjects = sorted(self.renderObjects, key = lambda x:x.resolution[0])        
        self.Select(sortedObjects[0])
        topW = sortedObjects[0].resolution[0]
        for renderObject in sortedObjects:
            if GameTools.PointInRect(renderObject.resolution + currentPos - Vector2(1,1), [Vector2(0,0), Vector2(self.w, self.h)]):
                renderObject.rPosition = currentPos
                currentPos += Vector2(0,renderObject.resolution.y)
            elif GameTools.PointInRect(renderObject.resolution - Vector2(1,1) + Vector2(currentPos.x + topW, 0), [Vector2(0,0), Vector2(self.w, self.h)]):
                renderObject.rPosition = Vector2(currentPos.x + topW, 0)
                topW = renderObject.resolution.x
                currentPos = renderObject.rPosition + Vector2(0,renderObject.resolution.y)
            else:
                renderObject.rPosition = Vector2(0,0)        
    
    def FindSpace(self, renderObject):
        points =  [Vector2(0,0), Vector2(0 ,renderObject.resolution[1]), Vector2(renderObject.resolution[0], 0), Vector2(renderObject.resolution[0], renderObject.resolution[1])]
        renderObjectRects = []
        
        for otherRenderObject in self.renderObjects:
            if not (otherRenderObject == renderObject):
                renderObjectRects.append([otherRenderObject.rPosition, otherRenderObject.rPosition + Vector2(otherRenderObject.resolution[0],otherRenderObject.resolution[1])])
        
        for col in range(self.w - renderObject.resolution[0] + 1):
            for row in range(self.h - renderObject.resolution[1] + 1):
                for point in points:
                    for rect in renderObjectRects:
                        if GameTools.PointInRect(point + Vector2(col,row), rect):
                            break
                    else:
                        return Vector2(col,row)
                    break
        
        return Vector2(0,0)
    
    def AddRenderObject(self, renderObject):
    
        renderObject.UpdateDisplay()
        #freeSpot = self.FindSpace(renderObject) 
        #renderObject.rPosition = freeSpot if freeSpot is not None else Vector2(0,0)
        self.renderObjects.append(renderObject)
        self.TileRenderObjects()


class RenderObject:
    
    def __init__(self, parent, rPosition = Vector2(0,0), resolution = None):
    
        self.parent = parent
        self.rPosition = rPosition
        self.resolution = resolution if resolution is not None else Vector2(int(parent.resolution[0]/2), int(parent.resolution[1]/2))
        self.display = None        
        self.labels = []
    
    def UpdateDisplay(self):
        self.display = self.GetDisplay()
        for label in self.labels:
            self.display.blit(label.textSurf, [*label.position])
    
    def GetBounds(self):
        resolution = self.resolution
        return [int(self.rPosition.x), int(self.rPosition.y) , int(self.rPosition.x) + resolution[0], int(self.rPosition.y) + resolution[1]]
        
    def AddLabel(self, label):
        label.MakeText()
        self.labels.append(label)
        
   
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    
class GUI:
    
    def __init__(self):
        self.UIfeatures = []
        self.labels = []
        
    def AddLabel(self, font, rPosition, backGround = None):
        pass

class RenderObjectLabel:
    
    def __init__(self, text, textSize = 12, position = Vector2(0,0), backGround = None, font = None):
        self.position = position
        self.textSize = textSize
        self.fontPath = None
        self.font = pygame.font.SysFont(None, textSize)
        self.text = text
        self.backGround = backGround
        self.textSurf = None

        self.bounds = self.font.size(text)
    
    def AdjustSizeToFont():
        self.bounds = self.font.size()
        
    def ChangeFont(self, path, size):  
        #args are [path to font, size of font]
        self.font = pygame.font.SysFont(path, size)
        
    def MakeText(self, colour = [255,255,255]):
        self.textSurf = self.font.render(self.text, True, colour, self.backGround)