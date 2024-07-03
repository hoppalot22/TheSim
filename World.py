import pygame
import numpy as np
import GameObject
import math
import Animal
import Camera
import Terrain
from GameTools import Vector2, Vector3

class World:
    
    def __init__(self):
        self.time = 0
        self.parent = None
        self.gameObjectList = []
        self.IDcount = int(0)
        self.cameras = []
        self.selectedCamera = None
        self.terrain = Terrain.Terrain()

    def Update(self):
        self.time += 1
        #print(f"World has existed for {self.time} seconds")
        for gameObject in self.gameObjectList:
            gameObject.Update()
            for camera in self.cameras:
                #All cameras check to see if they can see the object and update their internal lists
                camera.CanSee(gameObject)


    def InstantiateGameObject(self, gameObject, position = Vector3(0,0,0), forward = Vector3(1,0,0)):
        self.gameObjectList.append(gameObject)
        gameObject.parent = self
        
        self.GenObjectID(gameObject)
        
        if not (self.parent is None):
            self.parent.AddRenderables(gameObject)
        
        gameObject.position = position
        gameObject.forward = forward
            
        
    
    def AddCamera(self, position, resolution = [1280, 720]):
        self.cameras.append(Camera.Camera(self, position, resolution))
        self.selectedCamera = self.cameras[-1]
        
    def GetShots(self):
        return [camera.GetShot() for camera in self.cameras]
            
    
    def GenObjectID(self, gameObject):
        self.IDcount += 1
        gameObject.id = self.IDcount