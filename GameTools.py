from functools import singledispatchmethod
import pygame
import sys
import math

class Vector2:
    
    def __init__(self,x,y):
        self.x = float(x)
        self.y = float(y)
        
        self.vecList = [x,y]

    def SumProduct(self, vec2):
        assert(type(vec2) == Vector2)
        return self.x*vec2.x + self.y*vec2.y
        
    def __repr__(self):
        return str([self.x, self.y])
        
    def DistTo(self, other):
        assert(type(other) == Vector2)
        diff = other-self
        return math.sqrt(diff.x**2 + diff.y**2)
        
    def __getitem__(self,i):
        return self.vecList[i]
        
    @classmethod
    def Mag(cls, vec):
        assert(type(vec) == Vector2)
        return cls(math.sqrt(vec.x**2 + vec.y**2))    
        
    @classmethod
    def Norm(cls, vec):
        mag = Vector2.Mag(vec)
        if mag == 0:
            raise Exception("Divide by 0 error")
        return cls(vec / mag)

@singledispatchmethod
def __add__(self, construct):
    raise Exception(f"No overload method for '+' between Vector2 and {type(construct)}")
    
@__add__.register
def _(self, construct: Vector2):
    return Vector2(self.x + construct.x, self.y + construct.y)
    
@__add__.register
def _(self, construct: int):
    return Vector2(self.x + construct, self.y + construct)

@__add__.register
def _(self, construct: float):
    return Vector2(self.x + construct, self.y + construct)    

@singledispatchmethod
def __sub__(self, construct):
    raise Exception(f"No overload method for '-' between Vector2 and {type(construct)}")

@__sub__.register    
def _(self, construct: Vector2):
    return Vector2(self.x - construct.x, self.y - construct.y)

@__sub__.register
def _(self, construct: int):
    return Vector2(self.x - construct, self.y - construct)    

@__sub__.register
def _(self, construct: float):
    return Vector2(self.x - construct, self.y - construct)
    
@singledispatchmethod
def __mul__(self, construct):
    raise Exception(f"No overload method for '*' between Vector2 and {type(construct)}")

@__mul__.register    
def _(self, construct: Vector2):
    return Vector2(self.x * construct.x, self.y * construct.y)

@__mul__.register
def _(self, construct: int):
    return Vector2(self.x * construct, self.y * construct)    

@__mul__.register
def _(self, construct: float):
    return Vector2(self.x * construct, self.y * construct)

@singledispatchmethod
def __truediv__(self, construct):
    raise Exception(f"No overload method for '/' between Vector2 and {type(construct)}")

@__truediv__.register
def _(self, construct: int):
    if (construct == 0):
        raise Exception("Divide by 0 error")
    return Vector2(self.x / construct, self.y / construct)
    
@__truediv__.register
def _(self, construct: float):
    if (construct == 0):
        raise Exception("Divide by 0 error")
    return Vector2(self.x / construct, self.y / construct)    

Vector2.__add__ = __add__
Vector2.__sub__ = __sub__
Vector2.__mul__ = __mul__
Vector2.__truediv__ = __truediv__

class Vector3:
    
    def __init__(self,x,y,z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
        self.vecList = [x,y,z]

    def DotProduct(self, vec3):
        assert(type(vec3) == Vector3)
        return self.x*vec3.x + self.y*vec3.y + self.z*vec3.z
        
    def __repr__(self):
        return str([self.x, self.y, self.z])
        
    def DistTo(self, other):
        assert(type(other) == Vector3)
        diff = other-self
        return math.sqrt(diff.x**2 + diff.y**2 + diff.z**2)
    
    def __getitem__(self,i):
        return self.vecList[i]
    
    def Mag(vec):
        assert(type(vec) == Vector3)
        return math.sqrt(vec.x**2 + vec.y**2 + vec.z**2)
     
    def iNorm(self):
        mag = Vector3.Mag(self)
        if mag == 0:
            return self
        return self/mag
     
    @classmethod
    def Norm(cls, vec):
        mag = Vector3.Mag(vec)
        if mag == 0:
            return cls(vec.x, vec.y, vec.z)
        return cls(vec.x/mag, vec.y/mag, vec.z/mag)
        

@singledispatchmethod
def __add__(self, construct):
    raise Exception(f"No overload method for '+' between Vector3 and {type(construct)}")
    
@__add__.register
def _(self, construct: Vector3):
    return Vector3(self.x + construct.x, self.y + construct.y, self.z + construct.z)
    
@__add__.register
def _(self, construct: int):
    return Vector3(self.x + construct, self.y + construct, self.z + construct)

@__add__.register
def _(self, construct: float):
    return Vector3(self.x + construct, self.y + construct, self.z + construct)    

@singledispatchmethod
def __sub__(self, construct):
    raise Exception(f"No overload method for '-' between Vector3 and {type(construct)}")

@__sub__.register    
def _(self, construct: Vector3):
    return Vector3(self.x - construct.x, self.y - construct.y, self.z - construct.z)

@__sub__.register
def _(self, construct: int):
    return Vector3(self.x - construct, self.y - construct, self.z - construct)    

@__sub__.register
def _(self, construct: float):
    return Vector3(self.x - construct, self.y - construct, self.z - construct)
    
@singledispatchmethod
def __mul__(self, construct):
    raise Exception(f"No overload method for '*' between Vector3 and {type(construct)}")

@__mul__.register    
def _(self, construct: Vector3):
    return Vector3(self.x * construct.x, self.y * construct.y, self.z * construct.z)

@__mul__.register
def _(self, construct: int):
    return Vector3(self.x * construct, self.y * construct, self.z * construct)
    
@__mul__.register
def _(self, construct: float):
    return Vector3(self.x * construct, self.y * construct, self.z * construct)
    
@singledispatchmethod
def __truediv__(self, construct):
    raise Exception(f"No overload method for '/' between Vector3 and {type(construct)}")

@__truediv__.register
def _(self, construct: int):
    if (construct == 0):
        raise Exception("Divide by 0 error")
    return Vector3(self.x / construct, self.y / construct, self.z / construct)
    
@__truediv__.register
def _(self, construct: float):
    if (construct == 0):
        raise Exception("Divide by 0 error")
    return Vector3(self.x / construct, self.y / construct, self.z / construct)
    
Vector3.__add__ = __add__
Vector3.__sub__ = __sub__
Vector3.__mul__ = __mul__
Vector3.__truediv__ = __truediv__
 
def PrintNpArray(arr):
    if arr.ndim == 3:
        print(arr.transpose(2, 0, 1))
    else:
        print(arr)

def ArrayToSurf(nparray):
    return pygame.surfarray.make_surface(nparray).convert_alpha()

def GetInstanceSubStructure(instance, depth = 0):
    
    depth+=1
    print (depth)
    
    structure = []
    if depth >100:
        return structure, depth

    
    if (type(instance) == type(list())):
        if len(instance) == 0:
            return None
        else:
            instance = instance[0]
    
    if hasattr(instance, "__dict__"):
        #print(arg.__dict__)
        for k, v in vars(instance).items():
            if (not(k == "parent")):
                next = GetInstanceSubStructure(v, depth)
                if not(next is None):
                    structure.append([k, depth])
                    structure.append(next)
                
        #print("\n")
        return structure, depth
    #print("\n")
    return structure, depth

def PointInRect(point, rect):
    #print(point, rect, ((rect[0].x <= point.x <= rect[1].x)and(rect[0].y <= point.y <= rect[1].y)))
    return ((rect[0].x <= point.x <= rect[1].x)and(rect[0].y <= point.y <= rect[1].y))
    
def Main():
    
    vec1 = Vector3(3,5, 12)
    vec2 = Vector3(1,7, 4)
    scalar = int(2)
        
    print(vec1 + vec2)
    print(vec1 - vec2)
    print(vec1 * vec2)
    print(vec1 + scalar)
    print(vec1 - scalar)
    print(vec1 * scalar)
    print(vec1.DotProduct(vec2))
        
if __name__ == "__main__":
    Main()