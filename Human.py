from dataclasses import dataclass
import *Clothing
import Animal

class Human(Animal):

    def __init__(self, name = "John Smith"):
        super().__init__()
        
        self.name = name.split(' ')
        self.baseSprite = Sprite.Sprite().Square(size = 25, colour = [255,192,203,255])
        self.maxSpeed = 1200
        
        self.outfit = Outfit()
        
        self.GenerateSprite()
        
    def GenerateSprite(self):
        
    
    

@dataclass        
class Outfit:

    shoes: Shoes = Shoes()
    pants: Pants = Pants()
    shirt: Shirt = Shirt()
    hat: Hat = Hat()
    belt: Belt = Belt()
    
    def __iter__(self):
        return iter([self.shoes, self.pants, self.shirt, self.hat, self.belt])
        
    def GetSpriteList(self):
        return [x for x in *self if x.sprite is not None]