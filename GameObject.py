from GameTools import Vector2, Vector3
import math
import Sprite
import Signal
import pygame
import enum

class GameObjectState(enum.Enum):
    
    idle = 0
    walk = 1
    run = 2
    stop = 3
    rest = 4
    talk = 5
    threaten = 6
    scared = 7

class Feeling:
    
    outerFeelings = {
    "affinity" : 0,
    "positive" : 0,
    "love" : 0,
    "respect" : 0,
    "fear" : 0,
    "wariness" : 0,
    "rivalry" : 0,
    "comfortableness" : 0,
    "disgust" : 0,
    "trust" : 0,
    "jealousy" : 0,
    "admiration" : 0}
    
    innerFeelings = {
    "pride" : 0,
    "self worth" : 0,
    "confidence" : 0
    }
    
    def __init__(self, feelings, outer):
        self.Add(feelings, outer)
    
    def Add(self, feelings, outer):
        Nkeys = feelings.keys()       
        Okeys = self.outerFeelings.keys()
        Ikeys = self.innerFeelings.keys()
        for k in Nkeys:
            if k in Okeys:
                self.outerFeelings[k] += feelings[k]
            elif k in Ikeys:
                self.innerFeelings[k] += feelings[k]
            elif outer:
                self.outerFeelings[k] = feelings[k]     
            else:
                self.innerFeelings[k] = feelings[k]

    
class Memory:
    
    interactions = []
    
    def __init__(self, parent):
        self.parent = parent
        self.Add(Interaction(parent, parent, Feeling({"ego": 1}, outer = False)))

    def Add(self, interaction):
        self.interactions.append(interaction)

            
class Interaction:
    
    def __init__(self, me, you, feelings):
    
        self.me = me
        self.you = you
        self.feelings = feelings
        self.position = me.position



class GameObject:

    def __init__(self, name = "Nemo", position = Vector3(0,0,0), forward = Vector3(1,0,0), size = 1000):        

        self.position = position
        self.forward = forward
        self.initRotation = self.forward
        self.angle = 0
        self.name = name
        
        self.size = size
        
        self.memory = Memory(self)
        self.parent = None
        self.sprite = Sprite.Sprite().Square(size = 25, colour = [255,255,255,255])
    
    def RotateBy(self, angle, axis):
        
        R = [[Vector3(1,0,0),Vector3(0, math.cos(angle), -math.sin(angle)),Vector3(0, math.sin(angle), math.cos(angle))],
        [Vector3(math.cos(angle),0,math.sin(angle)),Vector3(0, 1, 0),Vector3(-math.sin(angle), 0, math.cos(angle))],
        [Vector3(math.cos(angle),-math.sin(angle),0),Vector3(math.sin(angle),math.cos(angle), 0),Vector3(0,0,1)]][axis]  
        
        newForward = Vector3(R[0].DotProduct(self.forward), R[1].DotProduct(self.forward), R[2].DotProduct(self.forward))
        #print(newForward)
        self.forward = newForward
        self.angle+=angle
    
    def EmitNoise(self, volume = 100, friendliness = 1000, onomat = "", draw = False):
        signal = Signal.Signal(self)
        signal.properties = {
        "source": self,
        "gameObject": self,
        "position": self.position,
        "type": "noise",
        "friendliness": friendliness,
        "onomat": onomat,
        }
        
        self.RequestDraw(pygame.draw.circle, [(int(255*(1-friendliness/1000)),int(255*friendliness/1000),0,64), [*Vector2(self.position.x, self.position.z)], volume])
        
        for gameObject in self.world.gameObjectList:
            relDist = Vector3.Mag(self.position - gameObject.position)
            if ((relDist) <= volume) and (gameObject is not self):
                signal.properties["relVolume"] = volume - relDist
                gameObject.TriggerEvent(signal)

    def AddInteraction(self, interaction):
        self.memory.Add(interaction)
        
    def Update(self):
        pass
    
    def SetSprite(self, sprite):
        self.sprite = sprite
    
    def GenerateSprite(self):
        pass
    
    def RequestDraw(self, drawFunc, params):
        self.world.parent.HandleDrawRequest(drawFunc, params)
    
    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

def Main():
    myObject = GameObject(Vector2(3,6), 45)    
    print(myObject.sprite.img)
    print(myObject.sprite.bounds)
        
if __name__ == "__main__":
    Main()        