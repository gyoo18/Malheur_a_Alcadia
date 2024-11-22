from typing_extensions import Self
from math import sqrt

class Vec3:
    x : float
    y : float
    z : float

    def __init__(self, x = None, y = None, z = None, xyz = 0, vec3 = None):
        if vec3 == None and xyz == 0 and not (x == None or y == None or z == None) and ((type(x) and type(y) and type(z)) == int or float ):
            self.x = x
            self.y = y
            self.z = z
        elif (x == None or y == None or z == None) and vec3 == None and xyz != None and (type(xyz) == int or float):
            self.x = xyz
            self.y = xyz
            self.z = xyz
        elif (x == None or y == None or z == None) and xyz == None and vec3 != None and type(vec3) == Self:
            self.x = vec3.x
            self.y = vec3.y
            self.z = vec3.z
        elif (x == None or y == None or z == None) and xyz == None and vec3 == None:
            self.x = 0
            self.y = 0
            self.z = 0
        else:
            raise ValueError("Les paramètre d'entrés de Vec3 ne sont pas valides")
        
    def copie(self):
        return Vec3(vec3=self)
    
    def __eq__(a : Self,b : Self):
        if type(b) != Self:
            return False
        return a.x == b.x and a.y == b.y and a.z == b.z
    
    def __neq__(a : Self, b : Self):
        if type(b) != Self:
            return True
        return a.x != b.x or a.y != b.y or a.z != b.z
    
    def __neg__(a : Self):
        return Vec3(-a.x,-a.y,-a.z)
    
    def __abs__(a : Self):
        return Vec3(abs(a.x),abs(a.y),abs(a.z))
    
    def distance(self, b : Self):
        if type(b) != Self:
            raise TypeError("Vec3.distance(b : Vec3) n'accepte pas d'argument de type " + str(type(b)) + ", seulement de type Vec3.")
        return Vec3.distance(self,b)
    
    def distance(a : Self, b : Self):
        if type(a) != Self:
            raise TypeError("Vec3.distance(a : Vec3, b: Vec3) n'accepte pas d'arguement de type a : " + str(type(a)) + ", seulement de type Vec3.")
        if type(b) != Self:
            raise TypeError("Vec3.distance(a : Vec3, b: Vec3) n'accepte pas d'arguement de type b : " + str(type(b)) + ", seulement de type Vec3.")
        return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y) + (a.z-b.z)*(a.z-b.z))
    
    def __add__(a : Self,b : Self):
        if type(b) == Self:
            return Vec3(a.x+b.x, a.y+b.y, a.z+b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x + b, a.y + b, a.z + b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __sub__(a : Self, b : Self):
        if type(b) == Self:
            return Vec3(a.x-b.x, a.y-b.y, a.z-b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x - b, a.y - b, a.z - b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __mul__(a : Self, b):
        if type(b) == Self:
            return Vec3(a.x*b.x, a.y*b.y, a.z*b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x * b, a.y * b, a.z * b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __div__(a : Self, b):
        if type(b) == Self:
            return Vec3(a.x/b.x, a.y/b.y, a.z/b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x / b, a.y / b, a.z / b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __floordiv__(a : Self, b):
        if type(b) == Self:
            return Vec3(a.x//b.x, a.y//b.y, a.z//b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x // b, a.y // b, a.z // b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __matmul__(a : Self, b : Self):
        if type(b) != Self:
            raise TypeError("b doit être de type Vec3, pas " + str(type(b)) + ".")
        return a.x*b.x + a.y*b.y + a.z*b.z
    
    def __mod__(a : Self, b):
        if type(b) == Self:
            return Vec3(a.x%b.x, a.y%b.y, a.z%b.z)
        elif type(b) == float or type(b) == int:
            return Vec3(a.x%b, a.y%b, a.z%b)
        else:
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __pow__(a : Self, b : Self):
        if type(b) != Self:
            raise TypeError("b doit être de type Vec3, pas " + str(type(b)) + ".")
        return Vec3(a.y*b.z - a.z*b.y, a.x*b.z - a.z*b.x, a.x*b.y - a.y*b.x)
    
    def __len__(a : Self):
        return sqrt(a.x * a.x + a.y * a.y + a.z * a.z)
    
    def len(self):
        return len(self)