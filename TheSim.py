import pygame
import numpy as np
import GameObject
import math
import Animal
import os
import Renderer
import Camera
import World
import GameTools
import time 
from GameTools import Vector2, Vector3

class Game:

    __name__ = "Game"
    moveKeys = [
    pygame.K_w,
    pygame.K_s,
    pygame.K_a,
    pygame.K_d,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_LEFT,
    pygame.K_RIGHT]

    def __init__(self):
        
        self.worlds = []
        self.currentWorld = None
        self.doubleClickActive = 0
        self.doubleClickWindow = 200
        self.InitSim()


    def InitSim(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.renderer = Renderer.Renderer()
        
        self.InitialConditions()

    def Update(self):
        #os.system('cls')
        self.HandleEvents()
        self.HandlePressed()
        self.Time()
        for world in self.worlds:
            world.Update()       
        
        self.renderer.Update()
        
        self.clock.tick(10)

    def HandlePressed(self):
        keyState = pygame.key.get_pressed()
        mouseState = pygame.mouse.get_pressed()
    
        for key in self.moveKeys:
            if keyState[key]:
                self.renderer.PanSelectedCamera(key)

    def MotionHandler(self, event):
        self.renderer.MotionHandler(event)
    
    def Time(self):
        #print(self.doubleClickActive)
        if not (self.doubleClickActive == 0):
            if abs(self.doubleClickActive)<self.doubleClickWindow:
                self.doubleClickActive = 0
            else:
                self.doubleClickActive -= 100*self.doubleClickActive/abs(self.doubleClickActive)
    

    def HandlePrimaryDoubleDown(self, event):
        self.renderer.HandlePrimaryDoubleDown(event)
        self.doubleClickActive = -500
        
    def HandlePrimaryDown(self, event):
        self.renderer.HandlePrimaryDown(event)
        if self.doubleClickActive>0:
            self.HandlePrimaryDoubleDown(event)
        else:
            self.doubleClickActive = self.doubleClickWindow + 1

    def HandleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.KeyHandler(event)
            elif(event.type == pygame.MOUSEBUTTONDOWN):
                #print(event)
                self.MouseDownHandler(event)             
            elif(event.type == pygame.MOUSEBUTTONUP):
                #print(event)
                self.MouseUpHandler(event)            
            elif(event.type == pygame.MOUSEMOTION):
                #print(event)
                self.MotionHandler(event)

    def MouseDownHandler(self,event):
        #print(event)
        if event.button == 1:
            self.HandlePrimaryDown(event)                   
        
        if event.button >= 4:
            self.renderer.ZoomSelectedCamera(event.button)    
            
    def MouseUpHandler(self,event):
        #print(event)
        if event.button == 1:
            self.renderer.HandlePrimaryUp(event)                   
        



    def KeyHandler(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False
            return
        
        if event.key in self.moveKeys:
            self.renderer.PanSelectedCamera(event.key)
        



    def Start(self):
        while (self.running):
            self.Update()
        pygame.quit()        
 

    def InitialConditions(self):
        self.myWorld = World.World()
        self.AddCamera(self.myWorld, [int(1280/2),int(720/2)])
        
        self.myCat = Animal.Cat(breed = "Black")
        self.myCat.name = "Charles"

        
        self.myDog = Animal.Dog(breed = "Great Dane")
        self.myDog.name = "Rex"

        
        self.myWorld.InstantiateGameObject(self.myCat)
        self.myWorld.InstantiateGameObject(self.myDog)
        
        self.AddCamera(self.myCat, resolution = [int(1280/2),int(720/2)])
        self.AddCamera(self.myDog, resolution = [int(1280/2),int(720/2)])
        
        self.AddWorld(self.myWorld)
        
    def AddWorld(self, world):
        self.worlds.append(world)
        world.parent = self
        
        self.currentWorld = world
        self.AddRenderables(world.gameObjectList)
        
    def AddRenderables(self, renderables):
        self.renderer.renderables.extend(renderables)
        
    def HandleDraw(self, drawFunc, params):          
        self.renderer.drawQueue.append([drawFunc, params])
    
    def AddCamera(self, onto, resolution = [1280, 720]):
        newCam = Camera.Camera(onto, resolution)        
        self.renderer.selectedCamera = newCam
        self.renderer.AddRenderObject(newCam, resolution)
        self.renderer.cameras.append(newCam)

def Main():
    myGame = Game()
    myGame.Start()
        
if __name__ == "__main__":
    Main()
