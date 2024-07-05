import pygame
import numpy as np
import GameObject
import math
import Animal
import Camera
import Terrain
from GameTools import Vector2, Vector3

class World:
    
    def __init__(self, name = None):
    
        self.name = name
        
        self.time = 0
        self.parent = None
        self.gameObjectList = []
        self.IDcount = int(0)        

        self.terrain = Terrain.Terrain()

    def Update(self):
        self.time += 1
        #print(f"World has existed for {self.time} seconds")
        for gameObject in self.gameObjectList:
            gameObject.Update()



    def InstantiateGameObject(self, gameObject, position = Vector3(0,0,0), forward = Vector3(1,0,0)):
        self.gameObjectList.append(gameObject)
        gameObject.world = self
        
        self.GenObjectID(gameObject)
        
        if not (self.parent is None):
            self.parent.AddRenderables(gameObject)
        
        gameObject.position = position
        gameObject.forward = forward

    
    def GenObjectID(self, gameObject):
        self.IDcount += 1
        gameObject.id = self.IDcount