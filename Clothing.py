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
        self.sprite = Sprite.Pickle2Sprite(Sprite.Sprite.spriteFolder + "\\shoes.pickle")
        self.ChangeColour(colour)
        self.speedMod = max(1,np.random.normal(loc = 2))
        self.armourValue = max(0,np.random.normal(loc = 2))


    def ChangeColour(self, colour):    
        pass
        

class Pants:
    def __init__(self):
        self.colour = np.random.rand(1,1,3)*255 
        
    
class Shirt:
    def __init__(self):
        self.colour = np.random.rand(1,1,3)*255
        self.sprite = Sprite.Pickle2Sprite(Sprite.Sprite.spriteFolder + "\\tshirt.pickle")        

class Hat:
    def __init__(self):
        self.colour = np.random.rand(1,1,3)*255 
        self.sprite = Sprite.Pickle2Sprite(Sprite.Sprite.spriteFolder + "\\cap.pickle")

class Belt:
    def __init__(self):
        self.colour = np.random.rand(1,1,3)*255 
        

def Main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    shoes = Shoes()
    shirt = Shirt()
    hat = Hat()
    
    clock = pygame.time.Clock()
    colors = iter(list(Colors.THECOLORS.values()))
    while(True):
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
    
        screen.fill("grey")
        img = pygame.Surface((16,16))
        img.fill("grey")
        img.blit(shoes.sprite.img, [0,0])
        img.blit(shirt.sprite.img, [0,0])
        img.blit(hat.sprite.img, [0,0])
        scaledImg = pygame.transform.scale(img, (640, int(640*shoes.height/shoes.width)))
        screen.blit(scaledImg, (int(640/2),int(360/4)))
        screen.blit(img, (0,0))
        pygame.display.flip()
        clock.tick(5)
        
if __name__ == "__main__":
    Main()