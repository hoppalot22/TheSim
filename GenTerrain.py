import numpy as np
import math
import pickle
import Perlin
import opensimplex as simplex
import os
from PIL import Image

class NoiseMap:

    def __init__(self, width: int, height: int, power: int = 1, frequency: int = 16):
        self.width = width
        self.height  = height
        self.frequency = frequency
        self.power = power
        self.map = self.GenerateMap()

    def GenerateMap(self):
        
        w = self.width
        h = self.height

        simplex.random_seed()

        w_norm = 2*math.pi/w
        h_norm = 2*math.pi/h

        map = np.empty((w, h))
        for col in range(w):
            for row in range(h):
                map[row, col] = simplex.noise4(math.cos(row*h_norm)*self.frequency, math.sin(row*h_norm)*self.frequency, math.cos(col*w_norm)*self.frequency, math.sin(col*w_norm)*self.frequency)
        map += 1
        map = ((map - np.min(map))/(np.max(map) - np.min(map)))**self.power*255
        
        return map

class BiomeMap:
    
    def __init__(self, width: int, height: int):
        
        self.width = width
        self.height = height

        self.map = self.GenerateBase()

    def GenerateBase(self):

        width = self.width
        height = self.height

        self.humidityMap = NoiseMap(width, height, frequency = 1, power = 2).map
        self.tempMap = NoiseMap(width, height, frequency = 1, power = 2).map
        self.holyMap = NoiseMap(width, height, frequency = 2, power = 3).map
        self.evilMap = NoiseMap(width, height, frequency = 2, power = 3).map

        hMap = np.where(self.humidityMap > 204, 255, self.humidityMap)
        hMap = np.where(self.humidityMap < 48, 0, self.humidityMap)
        tMap = np.where(self.tempMap > 204, 255, self.tempMap)
        tMap = np.where(self.tempMap < 48, 0, self.tempMap)
        bMap = np.where(self.holyMap > 204, 255, self.holyMap)
        eMap = np.where(self.evilMap > 204, 255, self.evilMap)

        map = np.dstack([hMap, tMap, bMap, eMap])
        
        return ((map)).astype(np.uint8)


class HeightMap:

    def __init__(self, width: int, height: int, ampMods = [1,1,1,1,1]):
        
        self.width = width
        self.height = height

        gain = 2
        self.octaves = [ampMods[x]/gain**x for x in range(len(ampMods))]
        self.map = self.GenerateMap()

    def GenerateMap(self):
        map = np.zeros((self.width, self.height))
        for octave in self.octaves:
            noiseArray = NoiseMap(self.width, self.height, frequency=1/octave)
            map += octave*noiseArray.map
        map /= sum(self.octaves)
        return map


def Main():

    wd = os.path.dirname(__file__)
    savePath = wd+"\\maps"

    heightMapPath = savePath + "\\heightMap.pickle"
    biomeMapPath = savePath + "\\biomeMap.pickle"

    counter = 0

    while os.path.isfile(heightMapPath):
        counter += 1
        heightMapPath = savePath + f"\\heightMap{counter}.pickle"    
    
    counter = 0
    while os.path.isfile(biomeMapPath):
        counter += 1
        biomeMapPath = savePath + f"\\biomeMap{counter}.pickle"
    
    myHeightMap = HeightMap(128, 128)
    heightImg = Image.fromarray(myHeightMap.map)
    heightImg = heightImg.resize([256,256])
    heightImg.show()

    myBiomeMap = BiomeMap(64,64)
    resizsedBiomeMaps = []
    for i in range(myBiomeMap.map.shape[2]):
        biomeImg = Image.fromarray(myBiomeMap.map[:,:,i])
        biomeImg = biomeImg.resize([256,256])
        resizsedBiomeMaps.append(np.array(biomeImg))
        biomeImg.show()

    myHeightMap = np.array(heightImg)
    myBiomeMap = np.dstack(resizsedBiomeMaps)

    with open(heightMapPath, "wb") as file:
        pickle.dump(myHeightMap, file)    
    
    with open(biomeMapPath, "wb") as file:
        pickle.dump(myBiomeMap ,file)


if __name__ == "__main__":
    Main()        

