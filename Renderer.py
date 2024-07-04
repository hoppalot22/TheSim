import pygame
import numpy as np
import math
import Camera
import GameTools
from GameTools import Vector2, Vector3


class Renderer:
    
    def __init__(self):

        self.w, self.h = 1600, 1000              
        self.screen = pygame.display.set_mode((self.w,self.h))
        self.gui = GUI()
        
        self.cameras = []  
        self.selectedCamera = None
        self.renderables = []
        
        self.renderObjects = []
        self.selectedRenderObject = None
        
        self.centerOffset = Vector2(int(self.w/2), int(self.h/2))        
        self.drawQueue = []
    
    def Update(self):        

        self.FillScreen()
        self.PrerenderTasks()
        self.RenderShots()
        self.RenderDrawables()
        self.RenderGUI()
        self.Flip()

    def FillScreen(self):
        self.screen.fill("grey")
    

    def PrerenderTasks(self):
        self.UpdateObjectsInCams()
    

    def RenderDrawables(self):
        for drawable in self.drawQueue:
            pass    
    
    def RenderShots(self):        
        for renderObject in self.renderObjects:
            if isinstance(renderObject.object, Camera.Camera):
                shot = renderObject.object.GetShot()
                self.screen.blit(shot, (renderObject.position.x, renderObject.position.y))

    def RenderGUI(self):
        pass
    
        
    def Flip(self):        
        pygame.display.flip()
      

    
    def NoiseRadii(self, signal):
        pygame.draw.circle(self.screen, (255,0,0,64), (signal.position.x, signal.position.z), signal.volume)


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
     
    def Select(self, renderObject):
        #print(f"Selected {renderObject}")
        self.selectedRenderObject = renderObject
    
            
    def MotionHandler(self,event):
        if pygame.mouse.get_pressed()[0]:
            if (self.selectedRenderObject is not None):
                bounds = self.selectedRenderObject.GetBounds()
                if(bounds[0] < event.pos[0] < bounds[2]) and (bounds[1] < event.pos[1] < bounds[3]):
                    self.Move(self.selectedRenderObject, event.rel)

    def Move(self, renderObject, distVec):

        if renderObject is None:
            return
            
        else:
            renderObject.position += Vector2(distVec[0], distVec[1])
        
        b = renderObject.GetBounds()
        
        if b[0] < 0:
            renderObject.position.x = 0
            
        if b[1] < 0:
            renderObject.position.y = 0          
            
        if b[2] > self.w:
            renderObject.position.x = self.w-renderObject.size[0]
            
        if b[3] > self.h:
            renderObject.position.y = self.h-renderObject.size[1]

        renderObject.bounds = b

    def PanSelectedCamera(self, key):
        if key in [pygame.K_w, pygame.K_UP]:
            self.selectedRenderObject.object.Pan(0,1)        
        if key in [pygame.K_s, pygame.K_DOWN]:
            self.selectedRenderObject.object.Pan(0,-1)        
        if key in [pygame.K_a, pygame.K_LEFT]:
            self.selectedRenderObject.object.Pan(-1,0)        
        if key in [pygame.K_d, pygame.K_RIGHT]:
            self.selectedRenderObject.object.Pan(1,0)        


        

    def ZoomSelectedCamera(self, amount):
        if amount%2 == 0:
            self.selectedRenderObject.object.Zoom(-amount/2)
        else:
            self.selectedRenderObject.object.Zoom(amount/2)
    
    def UpdateObjectsInCams(self):
        for camera in self.cameras:
            for gameObject in camera.world.gameObjectList:
                camera.CanSee(gameObject)
    
    def TileRenderObjects(self):
        positionList = []
        currentPos = Vector2(0,0)
        sortedObjects = sorted(self.renderObjects, key = lambda x:x.size[0])
        lastW = sortedObjects[0].size[0]
        for renderObject in sortedObjects:
            if GameTools.PointInRect(renderObject.size + currentPos, [Vector2(0,0), Vector2(self.w, self.h)]):
                renderObject.position = currentPos
                currentPos += Vector2(0,renderObject.size.y)
            elif GameTools.PointInRect(renderObject.size + Vector2(currentPos.x + lastW, 0), [Vector2(0,0), Vector2(self.w, self.h)]):
                renderObject.position = Vector2(currentPos.x + lastW, 0)
                lastW = renderObject.size.x
                currentPos = renderObject.position + Vector2(0,renderObject.size.y)
            else:
                renderObject.position = Vector2(0,0)
            
        
    
    def FindSpace(self, renderObject):
        points =  [Vector2(0,0), Vector2(0 ,renderObject.size[1]), Vector2(renderObject.size[0], 0), Vector2(renderObject.size[0], renderObject.size[1])]
        renderObjectRects = []
        
        for otherRenderObject in self.renderObjects:
            if not (otherRenderObject == renderObject):
                renderObjectRects.append([otherRenderObject.position, otherRenderObject.position + Vector2(otherRenderObject.size[0],otherRenderObject.size[1])])
        
        for col in range(self.w - renderObject.size[0]):
            for row in range(self.h - renderObject.size[1]):
                for point in points:
                    for rect in renderObjectRects:
                        if GameTools.PointInRect(point + Vector2(col,row), rect):
                            break
                    else:
                        return Vector2(col,row)
                    break
        
        return Vector2(0,0)
    
    def AddRenderObject(self, object, size, pos = Vector2(0,0)):
    
        newRenderObject = RenderObject(object, size, pos)
        freeSpot = self.FindSpace(newRenderObject)
        #print(freeSpot)
        if freeSpot is not None:
            newRenderObject.position = freeSpot        
        
        self.renderObjects.append(newRenderObject)
        self.selectedRenderObject = newRenderObject


class RenderObject:
    
    def __init__(self, object, size, pos = Vector2(0,0)):
    
        self.object = object
        self.position = pos
        if hasattr(object, "size"):
            size = object.size
        self.size = Vector2(size[0], size[1])
        self.bounds = self.GetBounds()
        
    def GetBounds(self):
        size = self.size
        self.bounds = [int(self.position.x), int(self.position.y) , int(self.position.x) + size[0], int(self.position.y) + size[1]]
        return self.bounds
        
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    
class GUI:
    
    def __init__(self):
        self.UIfeatures = []
        
    def AddLabel(self):
        pass

