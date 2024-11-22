from typing_extensions import Self
from math import sqrt

class Vec4:
    x : float
    y : float
    z : float
    w : float

    def __init__(self, x = None, y = None, z = None, w = None, xyzw = 0, vec4 = None):
        if vec4 == None and xyzw == 0 and not (x == None or y == None or z == None or w == None) and ((type(x) and type(y) and type(z) and type(w)) == int or float ):
            self.x = x
            self.y = y
            self.z = z
            self.w = w
        elif (x == None or y == None or z == None or w == None) and vec4 == None and xyzw != None and (type(xyzw) == int or float):
            self.x = xyzw
            self.y = xyzw
            self.z = xyzw
            self.w = xyzw
        elif (x == None or y == None or z == None or w == None) and xyzw == None and vec4 != None and type(vec4) == Self:
            self.x = vec4.x
            self.y = vec4.y
            self.z = vec4.z
            self.w = vec4.w
        elif (x == None or y == None or z == None or w == None) and xyzw == None and vec4 == None:
            self.x = 0
            self.y = 0
            self.z = 0
            self.w = 0
        else:
            raise ValueError("Les paramètre d'entrés de vec4 ne sont pas valides")
        
    def copie(self):
        return Vec4(vec4=self)
    
    def __eq__(a : Self,b : Self):
        if type(b) != Self:
            return False
        return a.x == b.x and a.y == b.y and a.z == b.z and a.w == b.w
    
    def __neq__(a : Self, b : Self):
        if type(b) != Self:
            return True
        return a.x != b.x or a.y != b.y or a.z != b.z or a.w != b.w
    
    def __neg__(a : Self):
        return Vec4(-a.x,-a.y,-a.z, -a.w)
    
    def __abs__(a : Self):
        return Vec4(abs(a.x),abs(a.y),abs(a.z), abs(a.w))
    
    def distance(self, b : Self):
        if type(b) != Self:
            raise TypeError("vec4.distance(b : vec4) n'accepte pas d'argument de type " + str(type(b)) + ", seulement de type vec4.")
        return Vec4.distance(self,b)
    
    def distance(a : Self, b : Self):
        if type(a) != Self:
            raise TypeError("vec4.distance(a : vec4, b: vec4) n'accepte pas d'arguement de type a : " + str(type(a)) + ", seulement de type vec4.")
        if type(b) != Self:
            raise TypeError("vec4.distance(a : vec4, b: vec4) n'accepte pas d'arguement de type b : " + str(type(b)) + ", seulement de type vec4.")
        return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y) + (a.z-b.z)*(a.z-b.z) + (a.w-b.w)*(a.w-b.w))
    
    def __add__(a : Self,b : Self):
        if type(b) == Self:
            return Vec4(a.x+b.x, a.y+b.y, a.z+b.z, a.w+b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x + b, a.y + b, a.z + b, a.w + b)
        else :
            raise TypeError("b doit être de type Vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __sub__(a : Self, b : Self):
        if type(b) == Self:
            return Vec4(a.x-b.x, a.y-b.y, a.z-b.z, a.w-b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x - b, a.y - b, a.z - b, a.w - b)
        else :
            raise TypeError("b doit être de type Vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __mul__(a : Self, b):
        if type(b) == Self:
            return Vec4(a.x*b.x, a.y*b.y, a.z*b.z, a.w*b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x * b, a.y * b, a.z * b, a.w * b)
        else :
            raise TypeError("b doit être de type vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __div__(a : Self, b):
        if type(b) == Self:
            return Vec4(a.x/b.x, a.y/b.y, a.z/b.z, a.w/b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x / b, a.y / b, a.z / b, a.w / b)
        else :
            raise TypeError("b doit être de type vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __floordiv__(a : Self, b):
        if type(b) == Self:
            return Vec4(a.x//b.x, a.y//b.y, a.z//b.z, a.w//b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x // b, a.y // b, a.z // b, a.w//b)
        else :
            raise TypeError("b doit être de type vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __matmul__(a : Self, b : Self):
        if type(b) != Self:
            raise TypeError("b doit être de type Vec4, pas " + str(type(b)) + ".")
        return a.x*b.x + a.y*b.y + a.z*b.z + a.w*b.w
    
    def __mod__(a : Self, b):
        if type(b) == Self:
            return Vec4(a.x%b.x, a.y%b.y, a.z%b.z, a.w%b.w)
        elif type(b) == float or type(b) == int:
            return Vec4(a.x%b, a.y%b, a.z%b, a.w%b)
        else:
            raise TypeError("b doit être de type vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __pow__(a : Self, b):
        if type(b) == Self:
            return Vec4(a.x**b.x,a.y**b.y,a.z**b.z,a.w**b.w)
        elif type(b) == float or type(b) == int:
            return Vec4(a.x ** b,a.y ** b,a.z ** b,a.w ** b)
        else : 
            raise TypeError("b doit être de type Vec2, pas " + str(type(b)) + ".")
        
    def __len__(a : Self):
        return sqrt(a.x * a.x + a.y * a.y + a.z * a.z + a.w * a.w)
    
    def len(self):
        return len(self)