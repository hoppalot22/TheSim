import math
import numpy as np
import pygame
import GameTools
import cv2
import GameObject
import Renderer
from GameTools import Vector2, Vector3

class Camera(Renderer.RenderObject):   
    
    def __init__(self, parent, onto, resolution):   
        
        super().__init__(parent, resolution = resolution)
        
        if isinstance(onto, GameObject.GameObject):
            self.gameObject = onto
            self.world = onto.world
        else:
            self.gameObject = None
            self.world = onto

        self.position = Vector3(0,10,0)
        self.forward = Vector3(0,-1,0)        
        self.aspectRatio = resolution[1]/resolution[0]
        self.HFOV = 60     
        self.height2HalfWidth = -math.tan(self.HFOV/2)
        self.zoom = 90
        #x1, y1, x2, y2
        self.shotBounds = self.CalcShotBounds()
        self.pixInTile = self.resolution[0]/(self.shotBounds[2]-self.shotBounds[0])
        self.boundsHalfWidth = self.height2HalfWidth*self.position.y
        
        self.terrain = self.world.terrain
        self.chunksToRender = []
        self.gameObjectsInShot = []        

        
    def CanSee(self, gameObject):
        Objx, Objy, Objz = gameObject.position
        xLower, zLower, xUpper, zUpper = self.CalcShotBounds()
        
        if (xLower < Objx < xUpper) and (zLower < Objz < zUpper):        
            if not(gameObject in self.gameObjectsInShot):
                    self.gameObjectsInShot.append(gameObject)
        else:
            for i, _gameObject in enumerate(self.gameObjectsInShot):
                if _gameObject == gameObject:
                    self.gameObjectsInShot.remove(_gameObject)  

    def UpdateObjectsInCam(self):
        for gameObject in self.world.gameObjectList:
            self.CanSee(gameObject)        

    def GetDisplay(self):
    
        if self.gameObject is not None:
            self.position.x = self.gameObject.position.x
            self.position.z = self.gameObject.position.z
        
        self.UpdateObjectsInCam()
        
        terrainShot = self.MakeTerrainShot()
        objectShot = self.MakeObjectShot(terrainShot)
        return objectShot
    
    def MakeTerrainShot(self):
        
        tileMap = self.MakeTileMap()
        mapX, mapZ = tileMap.width, tileMap.height
        wX,wZ = [max(x,1) for x in [self.boundsHalfWidth, self.boundsHalfWidth*self.aspectRatio]]
        relPos = self.position - tileMap.origin
        
        #camera vision is defined by the width of the shot from the center of the current tile map, however the camera will not always be at the origin of the tile map
        # so we add the relative position of the camera from the position in space of the map to get our vision. 1 tile has a width of 1 unit in real space
        x1 = int(mapX/2 -wX + relPos.x)
        x2 = int(mapX/2 + wX + relPos.x)
        z1 = int(mapZ/2 - wZ + relPos.z)
        z2 = int(mapZ/2 + wZ + relPos.z)
        
        visionMap = tileMap.map[x1:x2, z1:z2]
        
        #print(x1, x2, z1, z2, tileMapX, tileMapY, relPos, tileMap.origin)

        resize = cv2.resize(visionMap, (self.resolution[1], self.resolution[0]), interpolation=cv2.INTER_NEAREST)
        vision = GameTools.ArrayToSurf(resize)
            
        return vision
        
    def MakeTileMap(self):        
        tileMap = self.terrain.BuildTileMap(self.shotBounds)        
        return tileMap
        
        

    def MakeObjectShot(self, terrainShot):
    
        scaleFactor = self.pixInTile/1000 #convet mm to m
    
        for gameObject in self.gameObjectsInShot:
            sprite = gameObject.sprite
            gSize = gameObject.size
            w, h = sprite.img.get_size()
            
            spriteImg = pygame.transform.scale(sprite.img, [gSize*scaleFactor, gSize*scaleFactor])

            gPos = gameObject.position
            cPos = self.position
            
            xPos = (gPos.x - cPos.x) * self.pixInTile + self.resolution[0]/2
            zPos = (gPos.z - cPos.z) * self.pixInTile + self.resolution[1]/2
                  
            terrainShot.blit(spriteImg, [xPos - w*scaleFactor/2, zPos - h*scaleFactor/2])
            
            #print(f"blit {gameObject.name} sprite at location {xPos} {zPos}")
            
        return terrainShot

    def CalcShotBounds(self):
        
        self.boundsHalfWidth = self.height2HalfWidth*self.position.y
        return [self.position.x - self.boundsHalfWidth, self.position.z - self.boundsHalfWidth * self.aspectRatio, self.position.x + self.boundsHalfWidth, self.position.z + self.boundsHalfWidth * self.aspectRatio ]
        
    def Pan(self,x,z):
        self.position += Vector3(x, 0, -z)*self.position.y
        self.shotBounds = self.CalcShotBounds()
        
    def Zoom(self, y):    
        zoomAmount = y * (self.position.y)/50    
        self.position += Vector3(0,zoomAmount,0)
        
        if self.position.y<=.1:
            self.position.y = .1
        if self.position.y>100:
            self.position.y = 100
            
        self.height2HalfWidth = -math.tan(self.HFOV/2)
        self.shotBounds = self.CalcShotBounds()
        self.pixInTile = self.resolution[0]/(self.shotBounds[2]-self.shotBounds[0])
        