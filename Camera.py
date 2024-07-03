import math
import numpy as np
import pygame
import GameTools
import cv2
from GameTools import Vector2, Vector3

class Camera:   
    
    def __init__(self, world, position, resolution):    
        
        self.world = world
        self.resolution = resolution
        self.position = position
        self.forward = Vector3(0,-1,0)        
        self.aspectRatio = resolution[1]/resolution[0]
        self.HFOV = 60     
        self.height2HalfWidthRatio = -math.tan(self.HFOV/2)
        #x1, y1, x2, y2
        self.shotBounds = self.CalcShotBounds()
        self.pixInTile = self.resolution[0]/(self.shotBounds[2]-self.shotBounds[0])
        self.boundsHalfWidth = self.height2HalfWidthRatio*self.position.y
        
        self.terrain = self.world.terrain
        self.chunksToRender = []
        self.gameObjectsInShot = []        

        
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

    # def VisibleChunks(self):
        # maxSize = self.terrain.maxSize
        # camTileRange = [int(self.boundsHalfWidth) + 2, int(self.boundsHalfWidth)*self.aspectRatio + 2]
        # camChunkRange = [int(camTileRange[0]/32), int(camTileRange[1]/32)]
        
        
        # for i in range(maxSize):
            # if self.position.x - camTileRange[0] < i - self.terrain.maxSize/2 < self.position.x + camTileRange[0]:
                # for j in range(maxSize):                
                    # if self.position.z - camTileRange[1] < j - self.terrain.maxSize/2 < self.position.z + camTileRange[1]:
                        # pass

    def MakeTileMap(self):
        self.requiredTileBounds = self.shotBounds
        requiredChunkBounds = [int(self.requiredTileBounds[0]/32) - 1, int(self.requiredTileBounds[1]/32) - 1, -int(self.requiredTileBounds[0]/32) + 1, -int(self.requiredTileBounds[1]/32) + 1]
        tileMap = self.terrain.BuildTileMap(requiredChunkBounds)
        
        return tileMap
        

    def GetShot(self):
        terrainShot = self.MakeTerrainShot()
        objectShot = self.MakeObjectShot(terrainShot)
        return objectShot
    
    def MakeTerrainShot(self):
        
        tileMap = self.MakeTileMap()
        tileMapX, tileMapY = tileMap.width, tileMap.height
        wX,wY = self.boundsHalfWidth, self.boundsHalfWidth*self.aspectRatio
        camMapRelPos = tileMap.origin - self.position
        
        #camera vision is defined by the width of the shot from the center of the current tile map, however the camera will not always be at the origin of the tile map
        # so we add the relative position of the camera from the position in space of the map to get our vision. 1 tile has a width of 1 unit in real space
        x1, x2, y1, y2 = [int(tileMapX/2 -wX - camMapRelPos.x), int(tileMapX/2 + wX + camMapRelPos.x), int(tileMapY/2 - wY - camMapRelPos.z), int(tileMapY/2 + wY + camMapRelPos.z)]
        
        visionMap = tileMap.map[x1:x2, y1:y2]
        
        #print(x1, x2, y1, y2, tileMapX, tileMapY, camMapRelPos)
        
        resize = cv2.resize(visionMap, (self.resolution[1], self.resolution[0]), interpolation=cv2.INTER_NEAREST)
        vision = GameTools.ArrayToSurf(resize)
            
        return vision

    def MakeObjectShot(self, terrainShot):
    
        scaleFactor = self.pixInTile/1000 #convet mm to m
    
        for gameObject in self.gameObjectsInShot:
            objectSprite = gameObject.sprite
            objectSize = gameObject.size
            spriteSizeX, spriteSizeY = objectSprite.img.get_size()
            
            spriteImg = pygame.transform.scale(objectSprite.img, [objectSize*scaleFactor, objectSize*scaleFactor])

            objectPosition = gameObject.position
            
            xPos = (objectPosition.x - self.position.x) * self.pixInTile + self.resolution[0]/2
            zPos = (objectPosition.z - self.position.z) * self.pixInTile + self.resolution[1]/2
            
            #xPos = self.resolution[0]*(objectPosition.x - self.requiredTileBounds[0])/(self.requiredTileBounds[2]-self.requiredTileBounds[0]) + self.requiredTileBounds[0]
            #yPos = self.resolution[1]*(objectPosition.z - self.requiredTileBounds[1])/(self.requiredTileBounds[3]-self.requiredTileBounds[1]) + self.requiredTileBounds[1]
            
            terrainShot.blit(spriteImg, [xPos - spriteSizeX*scaleFactor/2, zPos - spriteSizeY*scaleFactor/2])
            
        return terrainShot

    def CalcShotBounds(self):
        
        self.boundsHalfWidth = self.height2HalfWidthRatio*self.position.y
        return [self.position.x - self.boundsHalfWidth, self.position.z - self.boundsHalfWidth * self.aspectRatio, self.position.x + self.boundsHalfWidth, self.position.z + self.boundsHalfWidth * self.aspectRatio ]
        
    def Pan(x,z):    

        camera.position += Vector3(x, 0, z)*self.position.y
        self.shotBounds = self.CalcShotBounds()
        
    def Zoom(self, y):
    
        zoomAmount = y * (self.position.y)/50
    
        self.position += Vector3(0,zoomAmount,0)
        if self.position.y<=0:
            self.position.y = 0.1
        self.height2HalfWidthRatio = -math.tan(self.HFOV/2)
        self.shotBounds = self.CalcShotBounds()
        self.pixInTile = self.resolution[0]/(self.shotBounds[2]-self.shotBounds[0])
        
        
                # for renderable in self.renderables:        
        
            # sprite = renderable.sprite         
            # pos = renderable.position
            # forward = renderable.forward            
            # offset = sprite.offset + self.cameraOffset
            
            # angle = renderable.angle * 180/math.pi
                