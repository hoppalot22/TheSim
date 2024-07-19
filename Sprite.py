from GameTools import Vector2, Vector3, PrintNpArray
import math
import numpy as np
import pygame
import pickle
import os

class Sprite:

    spriteFolder = r"C:\Users\alexm\OneDrive\Documents\python scripts\TheSim\sprites"

    def __init__(self, img = None):
        self.baseImg = img
        self.img = img
        self.offset = Vector2(0,0)
        if not (img is None):
            self.shape = img.get_size()
        else:
            self.shape = [1,1]
        self.bounds = self.GetBounds()
        self.namedSections = []

    def GetBounds(self):
        return [[-int(self.shape[0]/2)+self.offset[0],-int(self.shape[0]/2)+self.offset[1]], [int((self.shape[1]-1)/2)+self.offset[0], int((self.shape[1]-1)/2)+self.offset[1]]]
    
    
    def Rotate(self, angle):
        self.img = pygame.transform.rotate(self.baseImg, angle*180/math.pi)
    
    @classmethod
    def Square(cls, size = 10, colour = [255,255,255,255], forwardArrow = True):
        myImg = np.array([
        np.ones((size,size), dtype=np.uint8)*colour[0], 
        np.ones((size,size), dtype=np.uint8)*colour[1], 
        np.ones((size,size), dtype=np.uint8)*colour[2]])
        
        myImg = myImg.transpose(1,2,0)
        
        if forwardArrow:
            half = int(size/2)
            myImg[half:, half-2:half+2, 1:3] = 0
            
        surf = pygame.surfarray.make_surface(myImg).convert_alpha()    
        surf.set_alpha(colour[3])
        
        return cls(img = surf)
        
    @classmethod
    def Rect(cls, size = [10,20], colour = [255,255,255,255], forwardArrow = True):
        myImg = np.array([
        np.ones(size, dtype=np.uint8)*colour[0], 
        np.ones(size, dtype=np.uint8)*colour[1], 
        np.ones(size, dtype=np.uint8)*colour[2]])
        
        myImg = myImg.transpose(1,2,0)
        
        if forwardArrow:
            half = int(size/2)
            myImg[half:, half-2:half+2, 1:3] = 0

        surf = pygame.surfarray.make_surface(myImg).convert_alpha()
        surf.set_alpha(colour[3])
        
        return cls(img = surf)

class NamedSection:
    def __init__(self, parent, coords, name = "sprite", colour = None):
        self.parent = parent
        if name in [section.name for section in self.parent.namedSections]:
            self.name = str(name + "_2")
        else:
            self.name = name
        self.colour = colour
        self.coords = coords
        self.parent.namedSections.append(self)

def Sprite2Pickle(sprite, name = "sprite"):
    array = pygame.surfarray.array3d(sprite.baseImg)
    namedSections = sprite.namedSections
    for section in namedSections:
        section.parent = None
    offset = sprite.offset
    pickleDict =  {
    "array" : array,
    "namedSections" : namedSections,
    "offset" : offset
    }    
    wdir = os.path.dirname(__file__)
    num = 1
    while(os.path.exists(f"{wdir}\\sprites\\{name}{num}.pickle")):
        num+=1
    savePath = f"{wdir}\\sprites\\{name}{num}.pickle"
    
    with open(savePath, "wb") as outfile:
        pickle.dump(pickleDict, outfile)
    
def Pickle2Sprite(path):
    with open(path, "rb") as file:
        pickleDict = pickle.load(file)
    surf = pygame.surfarray.make_surface(pickleDict["array"])
    surf.set_colorkey((1,1,1))
    sprite = Sprite(img = surf)
    sprite.offset = pickleDict["offset"]
    sprite.namedSections = pickleDict["namedSections"]
    for section in sprite.namedSections:
        section.parent = sprite
    return sprite

def Main():


    folder = r"C:\Users\alexm\OneDrive\Documents\python scripts\TheSim\sprites"
    sprites = []

    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    counter = 0
    for file in os.listdir(folder):
        if file.split(".")[-1] == "pickle":
            sprites.append(Pickle2Sprite(f"{folder}\\{file}"))
    while True:
        events = pygame.event.get()
        screen.fill("grey")
        screen.blit(pygame.transform.scale(sprites[counter%len(sprites)].img.convert_alpha(), [400,400]), [0,0])
        pygame.display.flip()
        clock.tick(2)
        counter += 1
    

if __name__ == "__main__":
    Main()