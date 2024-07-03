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

    def HandleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.KeyHandler(event)
            elif(event.type == pygame.MOUSEBUTTONDOWN):
                self.MouseHandler(event)

    def MouseHandler(self,event):
        #print(event)
        if event.button == 0:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.Zoom(event)

    def Zoom(self, event):
        if event.button%2 == 0:
            self.currentWorld.selectedCamera.position.y -= event.button/2
        else:
            self.currentWorld.selectedCamera.position.y += event.button/2


    def KeyHandler(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False

    def Update(self):
        #os.system('cls')
        self.HandleEvents()
            
        for world in self.worlds:
            world.Update()       
        
        self.renderer.FillScreen()
        self.renderer.RenderShots(self.GetShots(self.worlds[0]))
        self.renderer.Flip()
        
        self.clock.tick(10)

    def Start(self):
        while (self.running):
            self.Update()
        pygame.quit()        
 

    def InitialConditions(self):
        self.myWorld = World.World()
        self.myWorld.AddCamera(Vector3(0,10,0), [int(1280/2),int(720/2)])
        
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
    
    
    def GetShots(self, world):
        shots = []
        for world in self.worlds:
            shots.extend(world.GetShots())
        return shots
    

def Main():
    myGame = Game()
    myGame.Start()
        
if __name__ == "__main__":
    Main()
