from dataclasses import dataclass
import Clothing
import Animal
import Sprite
from GameTools import Vector3, Vector2
import pygame

class Human(Animal.Animal):

    def __init__(self, name = "John Smith", forward = Vector3(1,0,1)):
        super().__init__(forward = forward)
        
        self.name = name
        self.names = name.split(" ")
        self.sprite = Sprite.Sprite()
        self.maxSpeed = 1200
        self.speed = self.maxSpeed/2
        
        self.shoes = Clothing.Shoes()
        self.shirt = Clothing.Shirt()
        self.hat = Clothing.Hat()
        
        #self.outfit = Outfit()
        
        self.sprite.baseImg = self.GenerateSprite()
        self.sprite.img = self.GenerateSprite()

    def SpecMove(self):
        self.RotateBy(1/100, 1)
        pass    
        
    def SpecUpdate(self):
        pass

    def NoiseHandler(self, signal):
        pass
    

    def Random(self):
        pass


    
    def GenerateSprite(self):
        img = pygame.Surface((16,16))
        img.fill((1,1,1))
        img.set_colorkey((1,1,1))
        img.blit(self.shoes.sprite.img, [0,0])
        img.blit(self.shirt.sprite.img, [0,0])
        img.blit(self.hat.sprite.img, [0,0])
        return img
    
    

# @dataclass        
# class Outfit:

    # shoes: Shoes = Shoes()
    # pants: Pants = Pants()
    # shirt: Shirt = Shirt()
    # hat: Hat = Hat()
    # belt: Belt = Belt()
    
    # def __iter__(self):
        # return iter([self.shoes, self.pants, self.shirt, self.hat, self.belt])
        
    # def GetSpriteList(self):
        # return [x for x in self if x.sprite is not None]