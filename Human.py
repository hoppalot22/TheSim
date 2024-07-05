import Animal

class Human(Animal):
    def __init__(self, name = "John Smith"):
        super().__init__()
        
        self.name = name.split(' ')
        self.sprite = Sprite.Sprite().Square(size = 25, colour = [200,200,100,255])
        self.maxSpeed = 1200