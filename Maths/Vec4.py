from typing_extensions import Self
from math import sqrt

class Vec4:

    def __init__(self, x = None, y = None, z = None, w = None):
        self.x : float = 0
        self.y : float = 0
        self.z : float = 0
        self.w : float = 0
        if (type(x) == float or type(x) == int) and (type(y) == float or type(y) == int) and (type(z) == float or type(z) == int) and (type(w) == float or type(w) == int):
            self.x = x
            self.y = y
            self.z = z
            self.w = w
        elif (type(x) == int or type(x) ==float) and y == None and z == None and w == None:
            self.x = x
            self.y = x
            self.z = x
            self.w = w
        elif type(x) == Vec4 and y == None and z == None and w == None:
            self.x = x.x
            self.y = x.y
            self.z = x.z
            self.w = x.w
        elif type(x) == None and y == None and z == None and w == None:
            self.x = 0
            self.y = 0
            self.z = 0
            self.w = 0
        else:
            raise ValueError("Les paramètre d'entrés de Vec4 ne sont pas valides")
        
    def copie(self):
        return Vec4(vec4=self)
    
    def __eq__(a : Self,b : Self):
        if type(b) != Vec4:
            return False
        return a.x == b.x and a.y == b.y and a.z == b.z and a.w == b.w
    
    def __neq__(a : Self, b : Self):
        if type(b) != Vec4:
            return True
        return a.x != b.x or a.y != b.y or a.z != b.z or a.w != b.w
    
    def __neg__(a : Self):
        return Vec4(-a.x,-a.y,-a.z, -a.w)
    
    def __abs__(a : Self):
        return Vec4(abs(a.x),abs(a.y),abs(a.z), abs(a.w))
    
    def distance(self, b : Self):
        if type(b) != Vec4:
            raise TypeError("vec4.distance(b : vec4) n'accepte pas d'argument de type " + str(type(b)) + ", seulement de type vec4.")
        return distance(self,b)
    
    def __add__(a : Self,b : Self):
        if type(b) == Vec4:
            return Vec4(a.x+b.x, a.y+b.y, a.z+b.z, a.w+b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x + b, a.y + b, a.z + b, a.w + b)
        else :
            raise TypeError("b doit être de type Vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __sub__(a : Self, b : Self):
        if type(b) == Vec4:
            return Vec4(a.x-b.x, a.y-b.y, a.z-b.z, a.w-b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x - b, a.y - b, a.z - b, a.w - b)
        else :
            raise TypeError("b doit être de type Vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __mul__(a : Self, b):
        if type(b) == Vec4:
            return Vec4(a.x*b.x, a.y*b.y, a.z*b.z, a.w*b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x * b, a.y * b, a.z * b, a.w * b)
        else :
            raise TypeError("b doit être de type vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __div__(a : Self, b):
        if type(b) == Vec4:
            return Vec4(a.x/b.x, a.y/b.y, a.z/b.z, a.w/b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x / b, a.y / b, a.z / b, a.w / b)
        else :
            raise TypeError("b doit être de type vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __floordiv__(a : Self, b):
        if type(b) == Vec4:
            return Vec4(a.x//b.x, a.y//b.y, a.z//b.z, a.w//b.w)
        elif type(b) == int or type(b) == float :
            return Vec4(a.x // b, a.y // b, a.z // b, a.w//b)
        else :
            raise TypeError("b doit être de type vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __matmul__(a : Self, b : Self):
        if type(b) != Vec4:
            raise TypeError("b doit être de type Vec4, pas " + str(type(b)) + ".")
        return a.x*b.x + a.y*b.y + a.z*b.z + a.w*b.w
    
    def __mod__(a : Self, b):
        if type(b) == Vec4:
            return Vec4(a.x%b.x, a.y%b.y, a.z%b.z, a.w%b.w)
        elif type(b) == float or type(b) == int:
            return Vec4(a.x%b, a.y%b, a.z%b, a.w%b)
        else:
            raise TypeError("b doit être de type vec4, float ou int, pas " + str(type(b)) + ".")
    
    def __pow__(a : Self, b):
        if type(b) == Vec4:
            return Vec4(a.x**b.x,a.y**b.y,a.z**b.z,a.w**b.w)
        elif type(b) == float or type(b) == int:
            return Vec4(a.x ** b,a.y ** b,a.z ** b,a.w ** b)
        else : 
            raise TypeError("b doit être de type Vec2, pas " + str(type(b)) + ".")
        
    def __len__(a : Self):
        return sqrt(a.x * a.x + a.y * a.y + a.z * a.z + a.w * a.w)
    
    def len(self):
        return len(self)
    
    def norm(self):
        l = self.len()
        self.x /= l
        self.y /= l
        self.z /= l
        self.w /= l
        return self
    
    def __iadd__(self, b : Self):
        if type(b) == Vec4:
            self.x += b.x
            self.y += b.y
            self.z += b.z
            self.w += b.w
        elif type(b) == float or type(b) == int:
            self.x += b
            self.y += b
            self.z += b
            self.w += b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération +=")
    
    def __isub__(self, b : Self):
        if type(b) == Vec4:
            self.x -= b.x
            self.y -= b.y
            self.z -= b.z
            self.w -= b.w
        elif type(b) == float or type(b) == int:
            self.x -= b
            self.y -= b
            self.z -= b
            self.w -= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération -=")
    
    def __imatmul__(self, b : Self):
        if type(b) == Vec4:
            self.x @= b.x
            self.y @= b.y
            self.z @= b.z
            self.w @= b.w
        elif type(b) == float or type(b) == int:
            self.x @= b
            self.y @= b
            self.z @= b
            self.w @= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération @=")

    def __imult__(self, b : Self):
        if type(b) == Vec4:
            self.x *= b.x
            self.y *= b.y
            self.z *= b.z
            self.w *= b.w
        elif type(b) == float or type(b) == int:
            self.x *= b
            self.y *= b
            self.z *= b
            self.w *= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération *=")

    def __itruediv__(self, b : Self):
        if type(b) == Vec4:
            self.x /= b.x
            self.y /= b.y
            self.z /= b.z
            self.w /= b.w
        elif type(b) == float or type(b) == int:
            self.x /= b
            self.y /= b
            self.z /= b
            self.w /= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération /=")
    
    def __ifloordiv__(self, b : Self):
        if type(b) == Vec4:
            self.x //= b.x
            self.y //= b.y
            self.z //= b.z
            self.w //= b.w
        elif type(b) == float or type(b) == int:
            self.x //= b
            self.y //= b
            self.z //= b
            self.w //= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération //=")
    
    def __imod__(self, b : Self):
        if type(b) == Vec4:
            self.x %= b.x
            self.y %= b.y
            self.z %= b.z
            self.w %= b.w
        elif type(b) == float or type(b) == int:
            self.x %= b
            self.y %= b
            self.z %= b
            self.w %= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération %=")
    
    def __ipow__(self, b : Self):
        if type(b) == Vec4:
            self.x **= b.x
            self.y **= b.y
            self.z **= b.z
            self.w **= b.w
        elif type(b) == float or type(b) == int:
            self.x **= b
            self.y **= b
            self.z **= b
            self.w **= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération **=")
    
    def norm(a : Self):
        return a.copie().norm()

        
    def distance(a : Self, b : Self):
        if type(a) != Vec4:
            raise TypeError("vec4.distance(a : vec4, b: vec4) n'accepte pas d'arguement de type a : " + str(type(a)) + ", seulement de type vec4.")
        if type(b) != Vec4:
            raise TypeError("vec4.distance(a : vec4, b: vec4) n'accepte pas d'arguement de type b : " + str(type(b)) + ", seulement de type vec4.")
        return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y) + (a.z-b.z)*(a.z-b.z) + (a.w-b.w)*(a.w-b.w))