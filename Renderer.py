import pygame
import numpy as np
import math
import Camera
from GameTools import Vector2, Vector3


class Renderer:
    
    def __init__(self):

        self.w, self.h = 1280, 720               
        self.screen = pygame.display.set_mode((self.w,self.h))
        self.gui = GUI()
        
        self.cameras = []  
        self.selectedCamera = None
        self.renderables = []
        
        self.clickableObjects = []
        self.selectedClickable = None
        
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
        self.screen.fill("black")
    

    def PrerenderTasks(self):
        self.UpdateObjectsInCams()
    

    def RenderDrawables(self):
        for drawable in self.drawQueue:
            pass    
    
    def RenderShots(self):        
        for clickable in self.clickableObjects:
            if isinstance(clickable.object, Camera.Camera):
                shot = clickable.object.GetShot()
                self.screen.blit(shot, (clickable.position.x, clickable.position.y))

    def RenderGUI(self):
        pass
    
        
    def Flip(self):        
        pygame.display.flip()
      

    
    def NoiseRadii(self, signal):
        pygame.draw.circle(self.screen, (255,0,0,64), (signal.position.x, signal.position.z), signal.volume)


    def HandlePrimaryDown(self, event):
        print("Click")
        for clickable in self.clickableObjects:
            bounds = clickable.bounds
            if (bounds[0] < event.pos[0] < bounds[2]) and (bounds[1] < event.pos[1] < bounds[3]):
                self.Select(clickable)
                break
     
    def HandlePrimaryUp(self, event):
        self.Select(None)
     
    def Select(self, clickable):
        print(f"Selected {clickable}")
        self.selectedClickable = clickable
    
            
    def MotionHandler(self,event):
        if pygame.mouse.get_pressed()[0]:
            if self.selectedClickable is not None:
                self.Move(self.selectedClickable, event.rel)

    def Move(self, clickable, distVec):
        b = clickable.bounds
        if clickable is None:
            return
        else:
            clickable.position += Vector2(distVec[0], distVec[1])
            
        if b[0] < 0:
            clickable.x = 0
            
        if b[1] < 0:
            clickable.y = 0          
            
        if b[2] > self.w:
            clickable.x = w-clickable.size[0]
            
        if b[3] > self.h:
            clickable.y = h-clickable.size[1]  

    def PanSelectedCamera(self, event):
        if event.button == 0:
            self.selectedCamera.Zoom(-event.button/2)
        else:
            self.selectedCamera.Zoom(event.button/2)
        

    def ZoomSelectedCamera(self, amount):
        if amount%2 == 0:
            self.selectedCamera.Zoom(-amount/2)
        else:
            self.selectedCamera.Zoom(amount/2)
    
    def UpdateObjectsInCams(self):
        for camera in self.cameras:
            for gameObject in camera[0].world.gameObjectList:
                camera[0].CanSee(gameObject)
    
    def AddClickable(self, clickable, size, pos = Vector2(0,0)):
    
        self.clickableObjects.append(Clickable(clickable, size))      


class Clickable:
    
    def __init__(self, object, size, pos = Vector2(0,0)):
    
        self.object = object
        self.position = pos
        self.size = size
        if hasattr(object, "size"):
            size = object.size
        self.bounds = self.GetBounds()
        
    def GetBounds(self):
        size = self.size
        return [int(self.position.x), int(self.position.y) , int(self.position.x) + size[0], int(self.position.y) + size[1]]
        
           
class GUI:
    
    def __init__(self):
        self.UIfeatures = []
        
    def AddLabel(self):
        pass

