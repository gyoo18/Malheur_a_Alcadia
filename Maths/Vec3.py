from typing_extensions import Self
from math import sqrt

class Vec3:

    def __init__(self, x = None, y = None, z = None):
        self.x : float = 0
        self.y : float = 0
        self.z : float = 0
        if (type(x) == float or type(x) == int) and (type(y) == float or type(y) == int) and (type(z) == float or type(z) == int):
            self.x = x
            self.y = y
            self.z = z
        elif (type(x) == int or type(x) ==float) and y == None and z == None:
            self.x = x
            self.y = x
            self.z = x
        elif type(x) == Vec3 and y == None and z == None:
            self.x = x.x
            self.y = x.y
            self.z = x.z
        elif type(x) == None and y == None and z == None:
            self.x = 0
            self.y = 0
            self.z = 0
        else:
            raise ValueError("Les paramètre d'entrés de Vec3 ne sont pas valides")
        
    def copie(self):
        return Vec3(vec3=self)
    
    def __eq__(a : Self,b : Self):
        if type(b) != Vec3:
            return False
        return a.x == b.x and a.y == b.y and a.z == b.z
    
    def __neq__(a : Self, b : Self):
        if type(b) != Vec3:
            return True
        return a.x != b.x or a.y != b.y or a.z != b.z
    
    def __neg__(a : Self):
        return Vec3(-a.x,-a.y,-a.z)
    
    def __abs__(a : Self):
        return Vec3(abs(a.x),abs(a.y),abs(a.z))
    
    def distance(self, b : Self):
        if type(b) != Vec3:
            raise TypeError("Vec3.distance(b : Vec3) n'accepte pas d'argument de type " + str(type(b)) + ", seulement de type Vec3.")
        return Vec3.distance(self,b)
    
    def __add__(a : Self,b : Self):
        if type(b) == Self:
            return Vec3(a.x+b.x, a.y+b.y, a.z+b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x + b, a.y + b, a.z + b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __sub__(a : Self, b : Self):
        if type(b) == Vec3:
            return Vec3(a.x-b.x, a.y-b.y, a.z-b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x - b, a.y - b, a.z - b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __mul__(a : Self, b):
        if type(b) == Vec3:
            return Vec3(a.x*b.x, a.y*b.y, a.z*b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x * b, a.y * b, a.z * b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __div__(a : Self, b):
        if type(b) == Vec3:
            return Vec3(a.x/b.x, a.y/b.y, a.z/b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x / b, a.y / b, a.z / b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __floordiv__(a : Self, b):
        if type(b) == Vec3:
            return Vec3(a.x//b.x, a.y//b.y, a.z//b.z)
        elif type(b) == int or type(b) == float :
            return Vec3(a.x // b, a.y // b, a.z // b)
        else :
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __matmul__(a : Self, b : Self):
        if type(b) != Vec3:
            raise TypeError("b doit être de type Vec3, pas " + str(type(b)) + ".")
        return a.x*b.x + a.y*b.y + a.z*b.z
    
    def __mod__(a : Self, b):
        if type(b) == Vec3:
            return Vec3(a.x%b.x, a.y%b.y, a.z%b.z)
        elif type(b) == float or type(b) == int:
            return Vec3(a.x%b, a.y%b, a.z%b)
        else:
            raise TypeError("b doit être de type Vec3, float ou int, pas " + str(type(b)) + ".")
    
    def __pow__(a : Self, b : Self):
        if type(b) != Vec3:
            raise TypeError("b doit être de type Vec3, pas " + str(type(b)) + ".")
        return Vec3(a.y*b.z - a.z*b.y, a.x*b.z - a.z*b.x, a.x*b.y - a.y*b.x)
    
    def __len__(a : Self):
        return sqrt(a.x * a.x + a.y * a.y + a.z * a.z)
    
    def len(self):
        return len(self)

    def norm(self):
        l = self.len()
        self.x /= l
        self.y /= l
        self.z /= l
        return self
    
    def __iadd__(self, b : Self):
        if type(b) == Vec3:
            self.x += b.x
            self.y += b.y
            self.z += b.z
        elif type(b) == float or type(b) == int:
            self.x += b
            self.y += b
            self.z += b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération +=")
    
    def __isub__(self, b : Self):
        if type(b) == Vec3:
            self.x -= b.x
            self.y -= b.y
            self.z -= b.z
        elif type(b) == float or type(b) == int:
            self.x -= b
            self.y -= b
            self.z -= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération -=")
    
    def __imatmul__(self, b : Self):
        if type(b) == Vec3:
            self.x @= b.x
            self.y @= b.y
            self.z @= b.z
        elif type(b) == float or type(b) == int:
            self.x @= b
            self.y @= b
            self.z @= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération @=")

    def __imult__(self, b : Self):
        if type(b) == Vec3:
            self.x *= b.x
            self.y *= b.y
            self.z *= b.z
        elif type(b) == float or type(b) == int:
            self.x *= b
            self.y *= b
            self.z *= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération *=")

    def __itruediv__(self, b : Self):
        if type(b) == Vec3:
            self.x /= b.x
            self.y /= b.y
            self.z /= b.z
        elif type(b) == float or type(b) == int:
            self.x /= b
            self.y /= b
            self.z /= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération /=")
    
    def __ifloordiv__(self, b : Self):
        if type(b) == Vec3:
            self.x //= b.x
            self.y //= b.y
            self.z //= b.z
        elif type(b) == float or type(b) == int:
            self.x //= b
            self.y //= b
            self.z //= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération //=")
    
    def __imod__(self, b : Self):
        if type(b) == Vec3:
            self.x %= b.x
            self.y %= b.y
            self.z %= b.z
        elif type(b) == float or type(b) == int:
            self.x %= b
            self.y %= b
            self.z %= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération %=")
    
    def __ipow__(self, b : Self):
        if type(b) == Vec3:
            self.x **= b.x
            self.y **= b.y
            self.z **= b.z
        elif type(b) == float or type(b) == int:
            self.x **= b
            self.y **= b
            self.z **= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération **=")
    
    def norm(a : Self):
        return a.copie().norm()

    def distance(a : Self, b : Self):
        if type(a) != Vec3:
            raise TypeError("Vec3.distance(a : Vec3, b: Vec3) n'accepte pas d'arguement de type a : " + str(type(a)) + ", seulement de type Vec3.")
        if type(b) != Vec3:
            raise TypeError("Vec3.distance(a : Vec3, b: Vec3) n'accepte pas d'arguement de type b : " + str(type(b)) + ", seulement de type Vec3.")
        return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y) + (a.z-b.z)*(a.z-b.z))