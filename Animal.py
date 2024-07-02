import GameObject
import GameTools
from GameTools import Vector3, Vector2
import math
from abc import abstractmethod
import random
import Sprite
from collections import namedtuple
import pygame
import numpy as np

class Goal:    
    def __init__(self, func, params, priority):
        self.func = func
        self.params = params
        self.priority = priority
        
        self.parent = None


    def Achieved(self):
        self.parent.RemoveGoal(self)
            

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
        
    def __repr__(self):
        return str([self.func.__name__, *self.params, self.priority])

class Goals:   
    
    def __init__(self):
        self.goalList = []
        self.func = None
        self.params = None
        self.priority = None
    
    def AddGoal(self, goal):
        for myGoal in self.goalList:
            if goal == myGoal:
                return
        self.goalList.append(goal)
        goal.parent = self
        self.goalList.sort(key=lambda x: x.priority) 

    def RemoveGoal(self, goal):
        for i, _goal in enumerate(self.goalList):
            if goal == _goal:
                del self.goalList[i]

    def TopGoal(self):

        if len(self.goalList)>0:
            return self.goalList[0]
        else:
            return None  
            
    def BottomGoal(self):
        if len(self.goalList)>0:
            return self.goalList[-1]
        else:
            return None  

    def __repr__(self):
        return str(self.goalList)

class Animal(GameObject.GameObject):

    def __init__(self, health = 1000, maxSpeed = 1000, size = 1000, intelligence = 1000):
    
        super().__init__()
        self.health = health
        self.maxSpeed = maxSpeed
        self.intelligence = intelligence
        
        self.confidence = 1000
        self.speed = 1
        
        self.goals = Goals()
        self.target = None
        self.home = self.position
        self.directionBias = Vector3(0,0,0)
        
        self.activities = dict()
    
    def Update(self):
        self.DoGoal()
        self.Random()
        self.Move()
        #self.Die()        
        self.SpecUpdate()
        self.UpdateSprite()
        
        #print(f"{self.name} (ID: {self.id}) is facing {self.forward}")
    
    def SetSpeed(self, speed):
        self.speed = min(speed, self.maxSpeed)
    
    def Idle(self):
        self.CheckSurroundings()
    
    def Move(self):        
        self.position += self.forward*self.speed/100
        self.SpecMove()
    
    def FaceDirection(self, vec):
        self.forward = Vector3.Norm(vec)
        self.angle = math.atan2(self.forward.x, self.forward.z)-math.pi/2    
        
    def Meander(self, propensity):
        
        homeBias = (self.home-self.position).iNorm() #random.randint(-25, 25) * (1 - (self.forward.DotProduct(GameTools.Vector3.Norm(self.home-self.position))+1)/2)
        self.directionBias = Vector3(*[random.randint(-100, 100), 0, random.randint(-100, 100)]).iNorm()
        resultantMeander = (self.forward*10 + self.directionBias*2 + homeBias*2).iNorm()
        self.FaceDirection(resultantMeander)
        #self.RotateBy(math.radians(changeAmount), 1)
    
    def Die(self):
        self.Stop()
        img = self.sprite.img
        w, h = img.get_size()
        whiteBG = np.zeros((w, h, 3), dtype = np.uint8)
        blackCross = np.array([[[(abs(i-j)<4 | abs(i-j)>w-4)*255 for z in range(3)] for i in range(w)] for j in range(h)])
        deathMark = pygame.surfarray.make_surface(whiteBG ).convert_alpha()
        self.sprite.img.blit(deathMark, (0,0))
    
    def Stop(self):
        self.speed = 0
    
    def DoGoal(self):    
        
        goal = self.goals.TopGoal()
        if goal is None:
            self.Idle()
            return            
        
        if(goal.func(*goal.params)):
            goal.Achieved()
        
        self.SpecGoal()
    
    def CheckSurroundings(self):
        pass
        
    def TriggerEvent(self, signal):
        if (signal.properties['type'] == "noise"):
            self.NoiseHandler(signal)
            
    @abstractmethod
    def NoiseHandler():
        pass
    
    @abstractmethod
    def Random():
        pass
        
    def UpdateSprite(self):
        self.sprite.Rotate(self.angle)
        
class Cat(Animal):
        
        def __init__(self, breed = "Tabby"):       
            super().__init__()
            
            self.breed = breed
        
        def SpecUpdate(self):
           self.Meow()
        
        def SpecMove(self):
            pass
            
        def SpecGoal(self):
            pass
        
        def Meow(self):
            #self.Stop()
            self.EmitNoise(volume = 200, friendliness = 1000, onomat = "Meow")
        
        def Flee(self, gameObject):
        
            flee = self.Flee.__name__            
            if flee not in self.activities.keys():
                self.activities[flee] = dict()
        
            self.speed = self.maxSpeed
            self.FaceDirection(self.position - gameObject.position)
            
            if (gameObject.position-self.position).Mag()>800:
                self.activities[flee]["achieved"] = True
            else:
                if "time" not in self.activities[flee].keys():
                    self.activities[flee]["time"] = 1
                else:
                    self.activities[flee]["time"] += 1
            return self.activities[flee]
        
        
        
        def NoiseHandler(self, signal):
            if (signal.properties['friendliness']<300) and (signal.properties['gameObject'] is not self):
                self.goals.AddGoal(Goal(self.Flee, [signal.properties['gameObject']], 100))
        
        def Random(self):
            #5% chance to stop and Meow
            if random.randint(0,99)>=95:
                self.Meow()
            
            #20% chance to alter forward direction
            if random.randint(0,9)>=8:
                self.Meander(0.5)

            #20% chance to alter speed
            if random.randint(0,99)>=80:
                self.SetSpeed(random.randint(200,1000))                
                
                
class Dog(Animal):
        
        def __init__(self, breed = "German Shepard"):
            super().__init__()
            
            self.breed = breed
            self.sprite = Sprite.Sprite().Square(size = 25, colour = [200,200,100,255])
            self.maxSpeed = 400
            
            

        def SpecUpdate(self):
            self.Woof()
        
        def SpecMove(self):
            pass
            
        def SpecGoal(Self):
            pass
        
        def Woof(self):
            #self.Stop()
            self.EmitNoise(volume = 150, friendliness = 200, onomat = "Woof")
        
        def Chase(self, gameObject):
            
            chase = self.Chase.__name__
            
            if chase not in self.activities.keys():
                self.activities[chase] = dict()
            
            self.speed = self.maxSpeed
            self.FaceDirection(gameObject.position-self.position)
            
            if (gameObject.position-self.position).Mag()>500:
                self.activities[chase]["achieved"] = False
            else:
                if "time" not in self.activities[chase].keys():
                    self.activities[chase]["time"] = 1
                else:
                    self.activities[chase]["time"] += 1
            return self.activities[chase]
        
        
        def NoiseHandler(self, signal):        
            if (signal.properties['friendliness'] > 500) and (signal.properties['gameObject'] is not self):
                self.goals.AddGoal(Goal(self.Chase,[signal.properties['gameObject']], 100))
                
        
        def Random(self):
            #5% chance to stop and Meow
            if random.randint(0,99)>=95:
                self.Woof()
            
            #20% chance to alter forward direction
            if random.randint(0,9)>=8:
                self.Meander(0.5)

            #20% chance to alter speed
            if random.randint(0,99)>=80:
                self.SetSpeed(random.randint(20,self.maxSpeed)) 

class Human(Animal):
    def __init__(self, name = "John Smith"):
        super().__init__()
        
        self.name = name.split(' ')
        self.sprite = Sprite.Sprite().Square(size = 25, colour = [200,200,100,255])
        self.maxSpeed = 1200
                
def Main():
    print(dir(Cat))
                
if __name__ == "__main__":
    Main()        