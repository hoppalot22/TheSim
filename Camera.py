import math
import numpy as np
import pygame
import GameTools
import cv2
from GameTools import Vector2, Vector3

class Camera:   
    
    def __init__(self, parent, position, resolution):    
        
        self.parent = parent
        self.resolution = resolution
        self.position = position
        self.forward = Vector3(0,-1,0)        
        self.aspectRatio = resolution[0]/resolution[1]
        self.HFOV = 60     
        #x1, y1, x2, y2
        self.shotBounds = self.CalcShotBounds()
        self.boundsHalfWidth = 1
        
        self.terrain = self.parent.terrain
        self.chunksToRender = []
        self.gameObjectsInShot = []        
        
        self.shotArray = self.MakeTileMap()
        self.shotSurf = GameTools.ArrayToSurf(self.shotArray)
        
    def CanSee(self, gameObject):
        Objx, Objy, Obz = gameObject.position.vecList
        xLower, zlower, xUpper, zUpper = self.CalcShotBounds()
        
        if (xLower < Objx < xUpper) and (yLower < Objy < yUpper):        
            if not(gameObject in self.gameObjectsInShot):
                    self.gameObjectsInShot.append(gameObject)
        else:
            for i, _gameObject in enumerate(self.gameObjectsInShot):
                if _gameObject == gameObject:
                    del self.gameObjectsInShot[i]  

    def VisibleChunks(self):
        maxSize = self.terrain.maxSize
        camTileRange = [int(self.boundsHalfWidth) + 2, int(self.boundsHalfWidth)*self.aspectRatio + 2]
        camChunkRange = [int(camTileRange[0]/32), int(camTileRange[1]/32)]
        
        
        for i in range(maxSize):
            if self.position.x - camTileRange[0] < i - self.terrain.maxSize/2 < self.position.x + camTileRange[0]:
                for j in range(maxSize):                
                    if self.position.z - camTileRange[1] < j - self.terrain.maxSize/2 < self.position.z + camTileRange[1]:
                        pass

    def MakeTileMap(self):
        requiredTileBounds = self.CalcShotBounds()
        requiredChunkBounds = [int(requiredTileBounds[0]) - 1, int(requiredTileBounds[1]) - 1, int(requiredTileBounds[0]) + 1, int(requiredTileBounds[1]) + 1]
        tileMap = self.terrain.BuildTileMap(requiredChunkBounds)
        self.tileMap = tileMap
        tileMapx = tileMapy = self.tileMap.shape[0]
        
        return cv2.resize(self.tileMap, (self.resolution[1], self.resolution[0]),interpolation=cv2.INTER_NEAREST)
    
    def GetShot(self):
        
        for attribute, value in self.__dict__.items():
            print(attribute, value)      
 
        return GameTools.ArrayToSurf(self.shotArray)

    def CalcShotBounds(self):
        self.boundsHalfWidth = math.tan(self.HFOV/2)*self.position.y
        return [self.position.x - self.boundsHalfWidth, self.position.z - self.boundsHalfWidth * self.aspectRatio, self.position.z + self.boundsHalfWidth, self.position.z + self.boundsHalfWidth * self.aspectRatio ]
        
    def Pan(x,z):
        camera.position += Vector3(x, 0, z)*self.zoom/1000
        
    def Zoom(y):
        camera.position += Vector3(0,y,0)
        
        
                # for renderable in self.renderables:        
        
            # sprite = renderable.sprite         
            # pos = renderable.position
            # forward = renderable.forward            
            # offset = sprite.offset + self.cameraOffset
            
            # angle = renderable.angle * 180/math.pi
                