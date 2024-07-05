from GameTools import Vector2, Vector3, PrintNpArray
import math
import numpy as np
import pygame

class Sprite():

    def __init__(self, img = None):
        self.baseImg = img
        self.img = img
        self.offset = Vector2(0,0)
        if not (img is None):
            self.shape = img.get_size()
        else:
            self.shape = [1,1]
        self.bounds = self.GetBounds()

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


def Main():
    mySquare = Sprite().Square()
    myRect = Sprite().Rect()
    print(mySquare.img)
    print(myRect.img)
    #PrintNpArray(mySprite.img)

if __name__ == "__main__":
    Main()