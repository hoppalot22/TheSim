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
        Objx, Objy, Objz = gameObject.position.vecList
        xLower, zLower, xUpper, zUpper = self.CalcShotBounds()
        
        if (xLower < Objx < xUpper) and (zLower < Objz < zUpper):        
            if not(gameObject in self.gameObjectsInShot):
                    self.gameObjectsInShot.append(gameObject)
        else:
            for i, _gameObject in enumerate(self.gameObjectsInShot):
                if _gameObject == gameObject:
                    self.gameObjectsInShot.remove(_gameObject)  

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
        self.requiredTileBounds = self.CalcShotBounds()
        requiredChunkBounds = [int(self.requiredTileBounds[0]/32) - 1, int(self.requiredTileBounds[1]/32) - 1, -int(self.requiredTileBounds[0]/32) + 1, -int(self.requiredTileBounds[1]/32) + 1]
        tileMap = self.terrain.BuildTileMap(requiredChunkBounds)
        
        #print(requiredTileBounds, requiredChunkBounds, tileMap.shape)
        
        return tileMap
        

  
    
    def GetShot(self):
        
        tileMap = self.MakeTileMap()
        tileMapx = tileMapy = tileMap.shape[0]
        
        resize = cv2.resize(tileMap, (self.resolution[1], self.resolution[0]), interpolation=cv2.INTER_NEAREST)
        img = GameTools.ArrayToSurf(resize)
        
        for gameObject in self.gameObjectsInShot:
            objectSprite = gameObject.sprite
            objectSize = gameObject.size
            spriteSizeX, spriteSizeY = objectSprite.img.get_size()
            scaleFactor = self.tile2pixRatio
            
            img = pygame.transform.scale(objectSprite.img, [spriteSizeX*scaleFactor, spriteSizeY*scaleFactor])

            objectPosition = gameObject.position
            
            xPos = self.resolution[0]*(objectPosition.x - self.requiredTileBounds[0])/(self.requiredTileBounds[2]-self.requiredTileBounds[0]) + self.requiredTileBounds[0]
            yPos = self.resolution[1]*(objectPosition.z - self.requiredTileBounds[1])/(self.requiredTileBounds[3]-self.requiredTileBounds[1]) + self.requiredTileBounds[1]
            
            img.blit(img, [xPos - spriteSizeX*scaleFactor, yPos - spriteSizeY*scaleFactor])
            
        return img

    def CalcShotBounds(self):
        self.tile2pixRatio = -math.tan(self.HFOV/2)
        self.boundsHalfWidth = self.tile2pixRatio*self.position.y
        return [self.position.x - self.boundsHalfWidth, self.position.z - self.boundsHalfWidth / self.aspectRatio, self.position.z + self.boundsHalfWidth, self.position.z + self.boundsHalfWidth / self.aspectRatio ]
        
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
                