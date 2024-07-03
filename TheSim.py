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
from GameTools import Vector2, Vector3

class Game:

    __name__ = "Game"

    def __init__(self):
        
        self.worlds = []
        self.currentWorld = None
        self.InitSim()


    def InitSim(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.renderer = Renderer.Renderer()
        
        self.InitialConditions()

    def Update(self):
        #os.system('cls')
        self.HandleEvents()
            
        for world in self.worlds:
            world.Update()       
        
        self.renderer.Update()
        
        self.clock.tick(10)

    def HandlePressed(self):
        keyState = pygame.key.get_pressed()
        mouseState = pygame.mouse.get_pressed()        
        if mouseState[0]:
            self.HandlePrimaryClick()

    def MotionHandler(self, event):
        self.renderer.MotionHandler(event)
     

    def HandlePrimaryDown(self):
        pass

    def HandleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.KeyHandler(event)
            elif(event.type == pygame.MOUSEBUTTONDOWN):
                #print(event)
                self.MouseHandler(event)            
            elif(event.type == pygame.MOUSEMOTION):
                #print(event)
                self.MotionHandler(event)

    def MouseHandler(self,event):
        #print(event)
        if event.button == 1:
            self.renderer.HandlePrimaryDown(event)
        if event.button >= 4:
            self.renderer.ZoomSelectedCamera(event.button)



    def KeyHandler(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False



    def Start(self):
        while (self.running):
            self.Update()
        pygame.quit()        
 

    def InitialConditions(self):
        self.myWorld = World.World()
        self.AddCamera(self.myWorld, Vector3(0,10,0), [int(1280/2),int(720/2)])
        
        self.myCat = Animal.Cat(breed = "Black")
        self.myCat.name = "Charles"
        self.myDog = Animal.Dog(breed = "Great Dane")
        self.myDog.name = "Rex"
        
        self.myWorld.InstantiateGameObject(self.myCat)
        self.myWorld.InstantiateGameObject(self.myDog)
        
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
    
    def AddCamera(self, world, position, resolution = [1280, 720]):
        newCam = Camera.Camera(world, position, resolution)
        newCam.world = world
        #self.renderer.cameras.append([newCam, Vector2(0,0)])
        self.renderer.selectedCamera = newCam
        self.renderer.AddClickable(newCam, resolution)

def Main():
    myGame = Game()
    myGame.Start()
        
if __name__ == "__main__":
    Main()
