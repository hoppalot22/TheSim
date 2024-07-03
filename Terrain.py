import math
import numpy as np
from GameTools import Vector3

class Terrain:

    def __init__(self, maxSize=128):
        
        initialChunkNum = 4
        self.maxSize = maxSize
        self.originIndicies = [int(maxSize/2), int(maxSize/2)]
        
        self.offset = int((maxSize - initialChunkNum)/2)
        
        self.chunkMap = [[None for j in range(maxSize)]for i in range(maxSize)]
        
        for i in range(initialChunkNum):
            for j in range(initialChunkNum):
                self.AddChunk(self.offset+i,self.offset+j)
    
    def __repr__(self):
        return str(self.chunkMap)               
    
    def AddChunk(self, x, y):
        #List of Columns
        self.chunkMap[x][y] = Chunk([x,y])
        #print("Added chunks")
        
    def BuildTileMap(self, chunkBounds):

        origin = Vector3((chunkBounds[2] + chunkBounds[0])/2, 0, (chunkBounds[3] + chunkBounds[1])/2)
        
        xRange, yRange = chunkBounds[2] - chunkBounds[0], chunkBounds[3] - chunkBounds[1]
        
        #print(f"rendering chunks \nx: {chunkBounds[0]} to {chunkBounds[2]} \ny:{chunkBounds[1]} to {chunkBounds[3]} at location {origin}")
        
        startChunkX = self.originIndicies[0] + chunkBounds[0]
        startChunkY = self.originIndicies[1] + chunkBounds[1]
        
        tileMapsX = []
        for col in range(xRange):
        
            tileMapsY = []
            for row in range(yRange):
                if (self.chunkMap[startChunkY + row][startChunkX + col] == None):
                    self.AddChunk(startChunkY + row, startChunkX + col)

                tileMapsY.append(self.chunkMap[startChunkY + row][startChunkX + col].innerTileMap)
            
            if(len(tileMapsY)>1):
                tileMapsX.append(np.concatenate(tileMapsY, axis = 1))
            else:
                tileMapsX = tileMapsY
        if len(tileMapsX)>1:
            tileMap = np.concatenate(tileMapsX, axis = 0)
        else:
            tileMap = tileMapsX
        
        return TileMap(tileMap, origin)
            
class Chunk:
    
    def __init__(self, chunkMapPos):
        #bias = np.kron(np.linspace(1,8,num = 4).reshape(2,2,1),np.ones((16,16,1)))*100
        self.chunkMapPos = chunkMapPos
        self.innerTileMap = np.random.rand(1,1,3) * np.matmul(np.diag(np.linspace(0,255,num = 32)), np.ones((32,32,1)))# + bias
        
class TileMap:
    
    def __init__(self, map, origin):
        self.origin = origin
        self.map = map
        self.width = self.map.shape[0]
        self.height = self.map.shape[1]
        self.map[int(self.width/2), int(self.height/2)] = [255,0,0]
        