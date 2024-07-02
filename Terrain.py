import math
import numpy as np

class Terrain:

    def __init__(self, maxSize=128):
        
        initialChunkNum = 4
        self.maxSize = maxSize
        
        self.offset = int((maxSize - initialChunkNum)/2)
        
        self.chunkMap = [[None for j in range(maxSize)]for i in range(maxSize)]
        
        for i in range(initialChunkNum):
            for j in range(initialChunkNum):
                self.AddChunk(self.offset+i,self.offset+j)
    
    #def __repr__(self):
     #   return str(self.chunkMap)
    
    def AddChunk(self, x, y):
        #List of Columns
        self.chunkMap[x][y] = Chunk([x,y])
        
    def BuildTileMap(self, chunkBounds):        
        
        xRange, yRange = chunkBounds[2] - chunkBounds[0], chunkBounds[3] - chunkBounds[1]
        
        tileMapsX = []
        for col in range(xRange):
            tileMapsY = []
            for row in range(yRange):
                if (self.chunkMap[row][col] == None):
                    self.AddChunk(row, col)
                tileMapsY.append(self.chunkMap[row][col].tileMap)
            tileMapsX.append(np.concatenate(tileMapsY, axis = 0))
                    
        tileMap = np.concatenate(tileMapsX, axis = 1)
        return tileMap
            
        
        
class Chunk:
    
    def __init__(self, chunkMapPos):
        self.chunkMapPos = chunkMapPos
        self.tileMap = np.where(np.random.rand(32,32)<.5, int(0), int(1))
        