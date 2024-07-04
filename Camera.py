import math
import numpy as np
import pygame
import GameTools
import cv2
import GameObject
from GameTools import Vector2, Vector3

class Camera:   
    
    def __init__(self, onto, resolution):    
        
        if isinstance(onto, GameObject.GameObject):
            self.gameObject = onto
            self.world = onto.world
        else:
            self.gameObject = None
            self.world = onto
            
        self.resolution = resolution
        self.position = Vector3(0,10,0)
        self.forward = Vector3(0,-1,0)        
        self.aspectRatio = resolution[1]/resolution[0]
        self.HFOV = 60     
        self.height2HalfWidthRatio = -math.tan(self.HFOV/2)
        self.zoom = 90
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
        
        tileMap = self.terrain.BuildTileMap(self.shotBounds)
        
        return tileMap
        

    def GetShot(self):
    
        if self.gameObject is not None:
            self.position.x = self.gameObject.position.x
            self.position.z = self.gameObject.position.z
            
        terrainShot = self.MakeTerrainShot()
        objectShot = self.MakeObjectShot(terrainShot)
        return objectShot
    
    def MakeTerrainShot(self):
        
        tileMap = self.MakeTileMap()
        tileMapX, tileMapY = tileMap.width, tileMap.height
        wX,wY = [max(x,1) for x in [self.boundsHalfWidth, self.boundsHalfWidth*self.aspectRatio]]
        camMapRelPos = self.position - tileMap.origin
        
        #camera vision is defined by the width of the shot from the center of the current tile map, however the camera will not always be at the origin of the tile map
        # so we add the relative position of the camera from the position in space of the map to get our vision. 1 tile has a width of 1 unit in real space
        x1, x2, y1, y2 = [int(tileMapX/2 -wX + camMapRelPos.x), int(tileMapX/2 + wX + camMapRelPos.x), int(tileMapY/2 - wY + camMapRelPos.z), int(tileMapY/2 + wY + camMapRelPos.z)]
        
        visionMap = tileMap.map[x1:x2, y1:y2]
        
        #print(x1, x2, y1, y2, tileMapX, tileMapY, camMapRelPos, tileMap.origin)
        try:
            resize = cv2.resize(visionMap, (self.resolution[1], self.resolution[0]), interpolation=cv2.INTER_NEAREST)
        except Exception as e:
            print(e,"\n",f"tileMapX: {tileMapX}, tileMapY: {tileMapY}, wX: {wX}, wY: {wY}, camMapRelPos: {camMapRelPos} x1: {x1} x2: {x2} y1: {y1} y2: {y2}")
            visionMap = tileMap.map[-4:4, -4:4]
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
            
            #print(f"blit {gameObject.name} sprite at location {xPos} {zPos}")
            
        return terrainShot

    def CalcShotBounds(self):
        
        self.boundsHalfWidth = self.height2HalfWidthRatio*self.position.y
        return [self.position.x - self.boundsHalfWidth, self.position.z - self.boundsHalfWidth * self.aspectRatio, self.position.x + self.boundsHalfWidth, self.position.z + self.boundsHalfWidth * self.aspectRatio ]
        
    def Pan(self,x,z):    

        self.position += Vector3(x, 0, -z)*self.position.y
        self.shotBounds = self.CalcShotBounds()
        #print(self.shotBounds)
        
    def Zoom(self, y):
    
        zoomAmount = y * (self.position.y)/50
    
        self.position += Vector3(0,zoomAmount,0)
        
        if self.position.y<=.1:
            self.position.y = .1
        if self.position.y>100:
            self.position.y = 100
            
        self.height2HalfWidthRatio = -math.tan(self.HFOV/2)
        self.shotBounds = self.CalcShotBounds()
        self.pixInTile = self.resolution[0]/(self.shotBounds[2]-self.shotBounds[0])
        
        
                # for renderable in self.renderables:        
        
            # sprite = renderable.sprite         
            # pos = renderable.position
            # forward = renderable.forward            
            # offset = sprite.offset + self.cameraOffset
            
            # angle = renderable.angle * 180/math.pi
                