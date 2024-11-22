from typing_extensions import Self
from math import sqrt

class Vec2:
    x : float
    y : float

    def __init__(self, x = None, y = None, xy = 0, vec2 = None):
        if vec2 == None and xy == 0 and not (x == None or y == None) and ((type(x) and type(y)) == int or float ):
            self.x = x
            self.y = y
        elif (x == None or y == None) and vec2 == None and xy != None and (type(xy) == int or float):
            self.x = xy
            self.y = xy
        elif (x == None or y == None) and xy == None and vec2 != None and type(vec2) == Self:
            self.x = vec2.x
            self.y = vec2.y
        elif (x == None or y == None) and xy == None and vec2 == None:
            self.x = 0
            self.y = 0
        else:
            raise ValueError("Les paramètre d'entrés de Vec2 ne sont pas valides")
        
    def copie(self):
        return Vec2(vec2=self)
    
    def __eq__(a : Self,b : Self):
        if type(b) != Self:
            return False
        return a.x == b.x and a.y == b.y
    
    def __neq__(a : Self, b : Self):
        if type(b) != Self:
            return True
        return a.x != b.x or a.y != b.y
    
    def __neg__(a : Self):
        return Vec2(-a.x,-a.y)
    
    def __abs__(a : Self):
        return Vec2(abs(a.x),abs(a.y))
    
    def __invert__(a : Self):
        return Vec2(a.y,a.x)
    
    def distance(self, b : Self):
        if type(b) != Self:
            raise TypeError("Vec2.distance(b : Vec2) n'accepte pas d'argument de type " + str(type(b)) + ", seulement de type Vec2.")
        return Vec2.distance(self,b)
    
    def distance(a : Self, b : Self):
        if type(a) != Self:
            raise TypeError("Vec2.distance(a : Vec2, b: Vec2) n'accepte pas d'arguement de type a : " + str(type(a)) + ", seulement de type Vec2.")
        if type(b) != Self:
            raise TypeError("Vec2.distance(a : Vec2, b: Vec2) n'accepte pas d'arguement de type b : " + str(type(b)) + ", seulement de type Vec2.")
        return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y))
    
    def __add__(a : Self,b : Self):
        if type(b) == Self:
            return Vec2(a.x+b.x, a.y+b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x + b, a.y + b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __sub__(a : Self, b : Self):
        if type(b) == Self:
            return Vec2(a.x-b.x, a.y-b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x - b, a.y - b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __mul__(a : Self, b):
        if type(b) == Self:
            return Vec2(a.x*b.x, a.y*b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x * b, a.y * b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __div__(a : Self, b):
        if type(b) == Self:
            return Vec2(a.x/b.x, a.y/b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x / b, a.y / b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __floordiv__(a : Self, b):
        if type(b) == Self:
            return Vec2(a.x//b.x, a.y//b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x // b, a.y // b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __matmul__(a : Self, b : Self):
        if type(b) != Self:
            raise TypeError("b doit être de type Vec2, pas " + str(type(b)) + ".")
        return a.x*b.x + a.y*b.y
    
    def __mod__(a : Self, b):
        if type(b) == Self:
            return Vec2(a.x%b.x, a.y%b.y)
        elif type(b) == float or type(b) == int:
            return Vec2(a.x%b, a.y%b)
        else:
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __pow__(a : Self, b : Self):
        if type(b) != Self:
            raise TypeError("b doit être de type Vec2, pas " + str(type(b)) + ".")
        return a.x*b.y - a.y*b.x
    
    def __len__(a : Self):
        return sqrt(a.x * a.x + a.y * a.y)
    
    def len(self):
        return len(self)