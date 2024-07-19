import math
import numpy as np
import pygame
import os
import pickle
import random
import Sprite
from GameTools import Vector3

class Terrain:

    terrainFolder = "C:\\Users\\alexm\\OneDrive\\Documents\\python scripts\\TheSim\\maps"

    def __init__(self, maxSize=256, chunkSize = 32):
        
        initialChunkNum = 4
        self.maxSize = maxSize
        self.chunkSize = chunkSize
        self.originIndicies = [int(maxSize/2), int(maxSize/2)]        
        self.offset = int((maxSize - initialChunkNum)/2)

        with open(self.terrainFolder + "\\heightMap.pickle", "rb") as file:
            self.heightMap = pickle.load(file)        

        with open(self.terrainFolder + "\\biomeMap.pickle", "rb") as file:
            self.biomeMap = pickle.load(file)

        self.chunkArray = self.heightMap
        self.chunkMap = [[None for j in range(maxSize)]for i in range(maxSize)]
        
        for i in range(initialChunkNum):
            for j in range(initialChunkNum):
                self.AddChunk(self.offset+i,self.offset+j)
    
    def __repr__(self):
        return str(self.chunkMap)               
    
    def AddChunk(self, x, y):
    
        #heights, self, up, down, left, right
        if (0<x<self.maxSize-1)and(0<y<self.maxSize-1):
            heights = [self.chunkArray[x,y], self.chunkArray[x,y+1], self.chunkArray[x,y-1], self.chunkArray[x+1,y], self.chunkArray[x-1,y]]
        else:
            heights = [self.chunkArray[x,y], self.chunkArray[x,y], self.chunkArray[x,y], self.chunkArray[x,y], self.chunkArray[x,y]]
        #List of Columns
        self.chunkMap[x][y] = Chunk(self, [x,y], self.chunkSize, heights)
        #print("Added chunks") 
        
    
    def BuildTileMap(self, shotBounds):

        #print(chunkBounds)
        chunkBounds = [int(shotBounds[0]/self.chunkSize) - 2, int(shotBounds[1]/self.chunkSize) - 2, int(shotBounds[2]/self.chunkSize) + 2, int(shotBounds[3]/self.chunkSize) + 2]
        
        origin = Vector3((chunkBounds[2] + chunkBounds[0])*self.chunkSize/2, 0, (chunkBounds[3] + chunkBounds[1])*self.chunkSize/2)
        
        xRange, zRange = chunkBounds[2] - chunkBounds[0], chunkBounds[3] - chunkBounds[1]
        
        #print(f"rendering chunks \nx: {chunkBounds[0]} to {chunkBounds[2]} \ny:{chunkBounds[1]} to {chunkBounds[3]} at location {origin}")
        
        startChunkX = self.originIndicies[0] + chunkBounds[0]
        startChunkZ = self.originIndicies[1] + chunkBounds[1]
        
        size = self.maxSize
        
        colourMapsX = []
        innerMapsX = []
        for col in range(xRange):        
            colourMapsY = []
            innerMapsY = []
            for row in range(zRange):
                if (self.chunkMap[(startChunkZ + row)%size][(startChunkX + col)%size] == None):
                    self.AddChunk((startChunkZ + row)%size, (startChunkX + col)%size)

                colourMapsY.append(self.chunkMap[(startChunkZ + row)%size][(startChunkX + col)%size].colourMap)
                innerMapsY.append(self.chunkMap[(startChunkZ + row)%size][(startChunkX + col)%size].innerTileMap)
            
            if(len(colourMapsY)>1):
                colourMapsX.append(np.concatenate(colourMapsY, axis = 1))
                innerMapsX.append(np.concatenate(innerMapsY, axis = 1))
            else:
                colourMapsX = colourMapsY
                innerMapsX = innerMapsY
        if len(colourMapsX)>1:
            colourMap = np.concatenate(colourMapsX, axis = 0)
            innerMap = np.concatenate(innerMapsX, axis = 0)
        else:
            colourMap = colourMapsX
            innerMap = innerMapsX
        
        return TileMap(innerMap, colourMap, origin)
            
class Chunk:
    
    tileMapDict = {
    "water" : 0,
    "grassland" : 1,
    "forest" : 2,
    "mountains" : 3,
    "beach" : 4,
    "desert" : 5
    }
    
    textureSprites = {
    "grassland1" : Sprite.Pickle2Sprite(Sprite.Sprite.spriteFolder + "\\grassland1.pickle")
    }
    
    def __init__(self, parent, chunkMapPos, chunkSize, heights):
        
        self.chunkMapPos = chunkMapPos
        self.size = chunkSize
        self.heights = heights
        self.parent = parent
        # x1, x2, z1, z2
        worldBounds = [chunkMapPos[0]*chunkSize, (chunkMapPos[0]+1)*chunkSize, chunkMapPos[1]*chunkSize, (chunkMapPos[1]+1)*chunkSize]
        x1,x2,z1,z2 = worldBounds
        self.innerBiomeMap = parent.biomeMap[x1:x2, z1:z2, :]

        self.innerheights = (np.matmul(np.diag(np.linspace((self.heights[2]+self.heights[0])/2,(self.heights[1]+self.heights[0])/2,num = chunkSize)), np.ones((chunkSize,chunkSize))) + np.transpose(np.matmul(np.diag(np.linspace((self.heights[4]+self.heights[0])/2,(self.heights[3]+self.heights[0])/2,num = chunkSize)), np.ones((chunkSize,chunkSize)))))/2
        
        self.innerTileMap = np.empty((chunkSize, chunkSize))
        self.innerTileMap[:,:] = self.tileMapDict["grassland"]
        self.innerTileMap[(self.innerBiomeMap[:,:,0] > 200) and (self.innerheights<100)] = self.tileMapDict["tropics"]
        self.innerTileMap[((parent.seaLevel+10)>self.innerheights) & (self.innerheights>parent.seaLevel)] = self.tileMapDict["beach"]
        self.innerTileMap[(self.innerheights>parent.mountainLevel)] = self.tileMapDict["mountains"]
        
        self.colourMap = np.empty((chunkSize,chunkSize,3))
        for i in range(3):            
            self.colourMap[:,:,i] = np.where(self.innerTileMap == self.tileMapDict["grassland"], self.innerheights*((i==1)), self.colourMap[:,:,i])
            self.colourMap[:,:,i] = np.where(self.innerTileMap == self.tileMapDict["water"], 255*(i==2), self.colourMap[:,:,i])
            self.colourMap[:,:,i] = np.where(self.innerTileMap == self.tileMapDict["beach"], self.innerheights*((i==1)or(i==0)), self.colourMap[:,:,i])
            self.colourMap[:,:,i] = np.where(self.innerTileMap == self.tileMapDict["mountains"], (self.innerheights-parent.mountainLevel)*((i == 1) or (i == 0))+140*(i == 0) +190*(i == 1)+ 210*(i == 2), self.colourMap[:,:,i])
        
class TileMap:
    
    
    def __init__(self, innerMap, colourMap, origin):
        self.origin = origin
        self.innerMap = innerMap
        self.colourMap = colourMap
        self.width = self.innerMap.shape[0]
        self.height = self.innerMap.shape[1]
        self.colourMap[int(self.width/2), int(self.height/2)] = [255,0,0]

def Main():

    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock() 
    
    myTerrain = Terrain()
    running = True
    
    gen = True
    
    while running:     
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False   
                    
        screen.fill("grey")
        pygame.display.flip()
        counter += 1
        clock.tick(2)
    

if __name__ == "__main__":
    Main()        