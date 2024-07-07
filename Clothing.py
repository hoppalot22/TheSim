import Sprite
import pygame
import numpy as np
import Colors
import random

class Shoes:
	
    def __init__(self, colour = (255,255,255)):
        self.colour = colour
        self.thickness = 2
        self.width, self.height = 24, 16
        self.ChangeColour(colour)
        self.speedMod = max(1,np.random.normal(loc = 2))
        self.armourValue = max(0,np.random.normal(loc = 2))


    def ChangeColour(self, colour, randomLace = False):
    
        if randomLace:            
            laceColour = np.random.rand(1,1,3)*255            
        else:    
            laceColour = [min(colour[x]+20, 255) for x in range(3)]    
        self.colour = colour
        imgArray = np.concatenate([np.ones((self.width,self.height,1))*[0,0,0][i] for i in range(3)], axis = 2)
        imgArray[self.thickness:self.width-self.thickness, self.thickness:self.height-self.thickness,:] = colour
        
        imgArray[2+int(1*(self.width - self.thickness)/8):1+int(7*(self.width - self.thickness)/8), int(self.thickness*2):int(3*self.height/4):2  ,:] = laceColour
        imgArray[int(self.width/2-3):int(self.width/2+3),self.thickness:self.height - self.thickness,:] = colour
        imgArray[int(self.width/2-self.thickness/2):int(self.width/2+self.thickness/2), :  ,:] = (0,0,0)
        imgArray[1+int(1*(self.width - self.thickness)/8):int(self.width/2):6, int(self.thickness*2):int(3*self.height/4):2  ,:] = (0,0,0)
        imgArray[int(1*(self.width - self.thickness)/8) + int(self.width/2):int(self.width):6, int(self.thickness*2):int(3*self.height/4):2  ,:] = (0,0,0)
        
        self.sprite = Sprite.Sprite(pygame.surfarray.make_surface(imgArray))
        

class Pants:
    def __init__(self):
        self.colour = np.random.rand(1,1,3)*255 
    
class Shirt:
    def __init__(self):
        self.colour = np.random.rand(1,1,3)*255 

class Hat:
    def __init__(self):
        self.colour = np.random.rand(1,1,3)*255 

class Belt:
    def __init__(self):
        self.colour = np.random.rand(1,1,3)*255 
        

def Main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    shoes = Shoes(colour = (139,69,19))
    
    
    clock = pygame.time.Clock()
    colors = iter(list(Colors.THECOLORS.values()))
    while(True):
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
    
        screen.fill("grey")
        shoes.ChangeColour([*next(colors)[0:3]], randomLace = True)
        img = shoes.sprite.img
        scaledImg = pygame.transform.scale(img, (640, int(640*shoes.height/shoes.width)))
        screen.blit(scaledImg, (int(640/2),int(360/4)))
        screen.blit(img, (0,0))
        pygame.display.flip()
        clock.tick(5)
        
if __name__ == "__main__":
    Main()